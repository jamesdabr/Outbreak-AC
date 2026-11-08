'use strict';
// FIXTURE_ONLY: built-in EventEmitter, fake sockets/clock/timers. No dgram import.
const assert=require('node:assert/strict'),{EventEmitter}=require('node:events');
const {install,PRESET}=require('./shaper.cjs');
let checks=0;function check(fn){fn();checks++;}
function fixture(){
 let at=0,id=0;const timers=new Map(),sent=[],received=[],held=[];
 const clock={now:()=>at,setTimer:(fn,ms)=>{const n=++id;timers.set(n,{fn,at:at+ms});return n;},clearTimer:n=>timers.delete(n),to(target,late=false){
  if(late)at=target;
  while(true){const row=[...timers].sort((a,b)=>a[1].at-b[1].at||a[0]-b[0]).find(x=>x[1].at<=target);if(!row)break;timers.delete(row[0]);if(!late)at=row[1].at;row[1].fn();}
  at=target;
 },early(target){at=target;const row=[...timers][0];timers.delete(row[0]);row[1].fn();}};
 class Socket extends EventEmitter{
  send(bytes,cb){sent.push({at,bytes:Buffer.from(bytes)});if(this.defer)held.push(cb);else cb(this.sendError||null);}
  close(cb){this.emit('close');if(cb)cb();return this;}
  address(){return {address:'127.0.0.1',family:'IPv4',port:12345};}
  connect(){return this;}bind(){return this;}
 }
 const dgram={createSocket:(kind)=>{assert.equal(kind,'udp4');return new Socket();}},original=dgram.createSocket;
 const control=install({dgram,now:clock.now,setTimer:clock.setTimer,clearTimer:clock.clearTimer});
 const sockets=[dgram.createSocket('udp4'),dgram.createSocket('udp4')];
 sockets.forEach(s=>s.on('message',(b,i)=>received.push({at,bytes:Buffer.from(b),info:{...i}})));
 function message(s,b){s.emit('message',b,{address:'127.0.0.1',port:29863,family:'IPv4',size:b.length});}
 function close(){sockets.forEach(s=>s.close());const r=control.close();assert.equal(timers.size,0);assert.equal(dgram.createSocket,original);return r;}
 return {clock,timers,dgram,original,sockets,control,sent,received,held,message,close};
}
let profile;
check(()=>{
 const f=fixture();let callbacks=0;const expected=[];
 for(let i=1;i<=100;i++){
  f.clock.to(i);const b=Buffer.from([i,255]),s=f.sockets[(i-1)%2];
  s.send(b,error=>{assert.equal(error,null);callbacks++;});f.message(s,b);b.fill(0);
  if(i%50)expected.push([i,255]);
 }
 f.clock.to(160);assert.deepEqual(f.sent.map(x=>[...x.bytes]),expected);assert.deepEqual(f.received.map(x=>[...x.bytes]),expected);assert.equal(callbacks,100);
 profile=f.close();for(const direction of ['up','down']){const d=profile.directions[direction];assert.equal(d.observed,100);assert.equal(d.dropped,2);assert.equal(d.delivered,98);assert.equal(d.delay_min_ms,40);assert.equal(d.delay_max_ms,40);}
 assert.deepEqual(profile.events.map(e=>[e.direction,e.ordinal,e.socket]),[['up',50,2],['down',50,2],['up',100,2],['down',100,2]]);assert.deepEqual(profile.faults,[]);assert.equal(f.control.close().cleanup.restored,true);
});
check(()=>{const f=fixture();let n=0;f.sockets[0].send(Buffer.from([9,8]),()=>n++);f.clock.early(39);assert.equal(f.sent.length,0);assert.equal(n,0);f.clock.to(40);assert.equal(f.sent[0].at,40);assert.equal(n,1);f.close();});
check(()=>{const f=fixture();let n=0;f.sockets[0].send(Buffer.from([9,8]),e=>{assert(e);n++;});f.clock.to(600,true);assert.equal(n,1);assert.equal(f.sent.length,0);assert(f.control.snapshot().faults.includes('pending_deadline'));f.close();});
check(()=>{const f=fixture();let n=0;f.sockets[0].defer=true;f.sockets[0].send(Buffer.from([9,8]),e=>{assert(e);n++;});f.clock.to(40);f.sockets[0].close();assert.equal(n,1);f.held[0](null);assert.equal(n,1);assert.equal(f.control.snapshot().directions.up.late_callbacks,1);assert.deepEqual(f.control.snapshot().faults,[]);f.close();});
check(()=>{const f=fixture();let n=0;f.sockets[0].sendError=Error('fixture native error');f.sockets[0].send(Buffer.from([9,8]),e=>{assert(e);n++;});f.clock.to(40);assert.equal(n,1);assert(f.control.snapshot().faults.includes('native_send_error'));f.close();});
check(()=>{const f=fixture();let n=0;for(let i=0;i<66;i++)f.sockets[0].send(Buffer.from([1,2]),()=>n++);assert(f.control.snapshot().faults.includes('queue_overflow'));assert.equal(f.control.snapshot().directions.up.peak_datagrams,64);f.close();assert.equal(n,66);});
check(()=>{const f=fixture();for(let i=0;i<33;i++)f.sockets[0].send(Buffer.alloc(4096),()=>{});assert(f.control.snapshot().faults.includes('queue_overflow'));assert.equal(f.control.snapshot().directions.up.peak_bytes,131072);f.close();});
check(()=>{const f=fixture();assert.throws(()=>f.dgram.createSocket('udp4'));assert.throws(()=>f.sockets[0].send(Buffer.alloc(2),0,2,()=>{}));assert.throws(()=>f.sockets[0].send(Buffer.alloc(4097),()=>{}));assert.throws(()=>f.sockets[0].emit('message',Buffer.alloc(2),{address:'elsewhere',port:29863,family:'IPv4',size:2}));f.close();});
check(()=>{const f=fixture();const error=Error('fixture UDP error');let received;f.sockets[0].on('error',e=>received=e);f.sockets[0].emit('error',error);assert.equal(received,error);assert(f.control.snapshot().faults.includes('native_socket_error'));f.close();});
check(()=>{const f=fixture();let n=0;f.sockets[0].defer=true;f.sockets[0].send(Buffer.alloc(2),()=>n++);f.clock.to(40);f.held[0](null);f.held[0](null);assert.equal(n,1);assert(f.control.snapshot().faults.includes('native_duplicate_callback'));f.close();});
check(()=>{const f=fixture();f.sockets.forEach(s=>s.close());const replacement=()=>{};f.dgram.createSocket=replacement;const r=f.control.close();assert.equal(f.dgram.createSocket,replacement);assert.equal(r.cleanup.restored,false);assert(r.faults.includes('factory_replaced'));assert.equal(f.timers.size,0);});
check(()=>{const f=fixture();const bytes=Buffer.alloc(4096,173),info={address:'127.0.0.1',port:29863,family:'IPv4',size:4096};f.sockets[0].send(bytes,()=>{});f.sockets[1].emit('message',bytes,info);bytes.fill(0);info.address='mutated fixture metadata';f.clock.to(40);assert.equal(f.sent[0].bytes.length,4096);assert(f.sent[0].bytes.every(n=>n===173));assert(f.received[0].bytes.every(n=>n===173));assert.equal(f.received[0].info.address,'127.0.0.1');f.close();});
check(()=>{const f=fixture();let n=0;f.sockets[0].send(Buffer.alloc(2),e=>{assert(e);n++;});f.message(f.sockets[1],Buffer.alloc(2));f.sockets.forEach(s=>s.close());const r=f.control.close();f.clock.to(600);assert.equal(n,1);assert.equal(f.sent.length,0);assert.equal(f.received.length,0);assert.equal(r.directions.up.canceled,1);assert.equal(r.directions.down.canceled,1);assert.equal(r.cleanup.buffers,0);assert.equal(r.cleanup.pending_bytes,0);assert.equal(f.timers.size,0);});
check(()=>{const f=fixture();f.sockets[0].send(Buffer.alloc(2),()=>{});f.clock.to(75,true);f.sockets[0].send(Buffer.alloc(2),()=>{});f.clock.to(195,true);const c=f.control.snapshot().directions.up;assert.equal(c.delay_min_ms,75);assert.equal(c.delay_max_ms,120);assert.deepEqual(c.histogram,{'40_49':0,'50_99':1,'100_499':1});f.close();});
const result={kind:'FIXTURE_ONLY_FAKE_FACTORY_CLOCK_TIMERS',checks,actual_sockets:0,game_result:'NOT_RUN',preset:PRESET,profile_receipt:profile};
if(process.argv[2])require('node:fs').writeFileSync(process.argv[2],JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({kind:result.kind,checks,actual_sockets:0,status:'PASS_FIXTURES'}));
