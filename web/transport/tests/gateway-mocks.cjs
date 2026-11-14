'use strict';
// Executes the actual component with explicit mock sockets and fake time.
// These assertions are NOT real transport, parser, UDP or game evidence.
const vm=require('node:vm'),fs=require('node:fs'),path=require('node:path');
const {EventEmitter}=require('node:events'),crypto=require('node:crypto'),assert=require('node:assert/strict');
module.exports=async function mockTests(){
 const results=[];
 async function environment(){
  let clock=0,next=0,server;const tasks=new Map(),udps=[],peers=[];
  const set=(fn,ms)=>{const id=++next;tasks.set(id,{at:clock+ms,fn});return id;};
  async function advance(ms){const end=clock+ms;for(let i=0;i<1000;i++){const entry=[...tasks].sort((a,b)=>a[1].at-b[1].at)[0];if(!entry||entry[1].at>end)break;clock=entry[1].at;tasks.delete(entry[0]);entry[1].fn();await Promise.resolve();}clock=end;await Promise.resolve();}
  class Socket extends EventEmitter{constructor(){super();this.destroyed=false;}end(){this.destroy();}destroy(){if(this.destroyed)return;this.destroyed=true;this.emit('close');}}
  class Peer extends EventEmitter{
   constructor(){super();this.readyState=1;this.bufferedAmount=0;this.out=[];peers.push(this);}
   pause(){}resume(){}close(code){this.readyState=3;this.emit('close',code);}terminate(){this.close(1006);}
   send(bytes,options,callback){this.out.push({bytes:Buffer.from(bytes),callback});}
   ping(bytes,mask,callback){this.pingBytes=Buffer.from(bytes);this.pingCount=(this.pingCount||0)+1;callback();}pong(bytes,mask,callback){this.pongs=(this.pongs||0)+1;callback();}
  }
  class WSS extends EventEmitter{constructor(){super();this.peers=[];}handleUpgrade(req,socket,head,cb){const p=new Peer();this.peers.push(p);cb(p);}close(cb){cb();}}
  const WS={WebSocketServer:WSS,OPEN:1,CLOSED:3};
  class UDP extends EventEmitter{
   constructor(){super();this.port=40000+udps.length;this.pending=[];udps.push(this);}
   bind(port,host,cb){this.boundCallback=cb;if(!env.delayBind){this.bound=true;cb();}}
   connect(port,host,cb){assert.equal(port,29863);assert.equal(host,'127.0.0.1');cb();}
   address(){return {address:'127.0.0.1',port:this.port,family:'IPv4'};}
   send(bytes,cb){this.pending.push({bytes:Buffer.from(bytes),cb});}
   close(){this.closed=true;this.emit('close');}
  }
  const env={delayBind:false,udps,peers,advance,elapseWithoutTasks:ms=>{clock+=ms;}};
  const sandbox={Object,Array,Buffer,Promise,Set,Map,setTimeout:set,clearTimeout:id=>tasks.delete(id),module:{exports:{}},
   require:name=>{
    if(name==='node:http')return {createServer:()=>{server=new EventEmitter();server.listen=(port,host,cb)=>{assert.equal(port,29865);assert.equal(host,'127.0.0.1');cb();};server.close=cb=>cb();return server;}};
    if(name==='node:dgram')return {createSocket:()=>new UDP()};
    if(name==='node:crypto')return crypto;
    if(name==='node:perf_hooks')return {performance:{now:()=>clock}};
    if(name.includes('vendor'))return WS;
    if(name==='./gateway-limits.cjs')return require('../gateway-limits.cjs');
    throw Error('unexpected_mock_import');
   }};
  vm.runInNewContext(fs.readFileSync(path.join(__dirname,'../gateway.cjs'),'utf8'),sandbox,{filename:'T057-actual-gateway-with-MOCKS.cjs',timeout:1000});
  const caps=[crypto.randomBytes(16).toString('base64url'),crypto.randomBytes(16).toString('base64url')];
  env.gateway=await sandbox.module.exports.startGateway({schema_version:1,run_id:'a'.repeat(32),capability_sha256:caps.map(c=>crypto.createHash('sha256').update(c).digest('hex'))});
  env.admit=()=>{
   const socket=new Socket();server.emit('connection',socket);
   const headers={host:'outbreak.localhost:29865',origin:'http://outbreak.localhost:29866','sec-websocket-version':'13','sec-websocket-protocol':'outbreak-enet-dgram.v1',upgrade:'websocket',connection:'Upgrade','sec-websocket-key':'mock-library-owns-RFC-validation'};
   server.emit('upgrade',{method:'GET',url:`/enet?cap=${caps[peers.length]}`,headers,rawHeaders:Object.entries(headers).flat()},socket,Buffer.alloc(0));
   peers.at(-1).socket=socket;return peers.at(-1);
  };
  env.reject=()=>{const socket=new Socket();server.emit('connection',socket);server.emit('upgrade',{method:'GET',headers:{},rawHeaders:[],url:'/invalid'},socket,Buffer.alloc(0));};
  env.tasks=tasks;return env;
 }
 async function test(name,fn){await fn();results.push({name,status:'PASS',kind:'ACTUAL COMPONENT WITH MOCK SOCKETS / FAKE CLOCK; not real networking'});}
 await test('late_send_callback_retirement_and_60_second_hold',async()=>{
  const e=await environment(),p=e.admit();p.emit('message',Buffer.from([1,2]),true);assert.equal(e.udps[0].pending.length,1);
  p.emit('message',Buffer.from('text'),false);const before=e.gateway.snapshot();assert.equal(before.sessions[0].reason,'text_rejected');assert.equal(before.retired,1);
  e.udps[0].pending[0].cb();e.udps[0].emit('message',Buffer.from([3,4]),{address:'127.0.0.1',port:29863});
  const after=e.gateway.snapshot();assert.equal(after.counters.to_udp_datagrams,0);assert.equal(after.counters.late_callbacks,1);assert.equal(after.counters.retired_discarded,1);assert.equal(after.sessions[0].to_udp.pending_bytes,0);assert.equal(p.out.length,0);
  await e.advance(59999);assert.equal(e.udps[0].closed,undefined);await e.advance(1);assert.equal(e.udps[0].closed,true);await e.gateway.close();assert.equal(e.tasks.size,0);
 });
 await test('udp_callback_failure_never_counts_delivery',async()=>{const e=await environment(),p=e.admit();p.emit('message',Buffer.from([1,2]),true);e.udps[0].pending[0].cb(Error('mock'));const s=e.gateway.snapshot();assert.equal(s.counters.to_udp_datagrams,0);assert.equal(s.sessions[0].reason,'udp_send_error');assert.equal(s.sessions[0].to_udp.pending_bytes,0);await e.gateway.close();});
 await test('ws_callback_failure_and_backlog_release',async()=>{const e=await environment(),p=e.admit();e.udps[0].emit('message',Buffer.from([1,2]),{address:'127.0.0.1',port:29863});assert.equal(p.out.length,1);p.out[0].callback(Error('mock'));const s=e.gateway.snapshot();assert.equal(s.counters.to_ws_datagrams,0);assert.equal(s.sessions[0].reason,'ws_send_error');assert.equal(s.sessions[0].to_ws.pending_bytes,0);await e.gateway.close();});
 await test('500ms_pending_send_terminates_component_session',async()=>{const e=await environment(),p=e.admit();p.emit('message',Buffer.from([1,2]),true);await e.advance(499);assert.equal(e.gateway.snapshot().active,1);await e.advance(1);assert.equal(e.gateway.snapshot().sessions[0].reason,'backlog_timeout');await e.gateway.close();});
 await test('heartbeat_every_5s_and_newer_pong_does_not_forgive_missing_older',async()=>{const e=await environment(),p=e.admit();await e.advance(5000);assert.equal(p.pingBytes.length,8);p.emit('pong',Buffer.alloc(8,0));await e.advance(5000);assert.equal(p.pingCount,2);p.emit('pong',p.pingBytes);await e.advance(4999);assert.equal(e.gateway.snapshot().active,1);await e.advance(1);assert.equal(e.gateway.snapshot().sessions[0].reason,'pong_timeout');await e.gateway.close();});
 await test('matching_pong_and_30_second_application_idle',async()=>{const e=await environment(),p=e.admit();for(let i=0;i<5;i++){await e.advance(5000);p.emit('pong',p.pingBytes);}await e.advance(5000);assert.equal(e.gateway.snapshot().sessions[0].reason,'application_idle');await e.gateway.close();});
 await test('close_during_bind_waits_and_never_connects_or_forwards',async()=>{const e=await environment();e.delayBind=true;e.admit();let resolved=false;const done=e.gateway.close().then(()=>resolved=true);await Promise.resolve();assert.equal(resolved,false);e.udps[0].bound=true;e.udps[0].boundCallback();await done;assert.equal(e.udps[0].closed,true);assert.equal(e.gateway.snapshot().udp_total,0);assert.equal(e.tasks.size,0);});
 await test('absolute_run_30_minutes_closes_all_handles',async()=>{const e=await environment();await e.advance(1800000);await e.gateway.close();assert.equal(e.gateway.snapshot().cleanup.reason,'run_timeout');assert.equal(e.tasks.size,0);});
 await test('ws_backpressure_stops_before_copy_forward',async()=>{const e=await environment(),p=e.admit();p.bufferedAmount=131071;e.udps[0].emit('message',Buffer.from([1,2]),{address:'127.0.0.1',port:29863});assert.equal(p.out.length,0);assert.equal(e.gateway.snapshot().sessions[0].reason,'pending_limit');await e.gateway.close();});
 await test('direction_packet_burst_stops_65th_udp_send',async()=>{const e=await environment(),p=e.admit();for(let i=0;i<65;i++)p.emit('message',Buffer.from([1,2]),true);assert.equal(e.udps[0].pending.length,64);assert.equal(e.gateway.snapshot().sessions[0].reason,'direction_rate');for(const item of e.udps[0].pending)item.cb();assert.equal(e.gateway.snapshot().sessions[0].to_udp.pending_bytes,0);await e.gateway.close();});
 await test('manual_pong_burst_bound',async()=>{const e=await environment(),p=e.admit();for(let i=0;i<9;i++)p.emit('ping',Buffer.alloc(1));assert.equal(p.pongs,8);assert.equal(e.gateway.snapshot().sessions[0].reason,'control_rate');await e.gateway.close();});
 await test('diagnostic_overflow_fails_and_stops_instead_of_dropping',async()=>{const e=await environment();for(let i=0;i<513;i++)e.reject();await e.gateway.close();const s=e.gateway.snapshot();assert.equal(s.failure,'diagnostic_overflow');assert.equal(s.diagnostics.length,512);assert.ok(s.counters.diagnostic_overflow>=1);assert.equal(s.cleanup.timers,0);});
 await test('raw_wire_limit_stops_later_message_forward',async()=>{const e=await environment(),p=e.admit();p.socket.emit('data',Buffer.alloc(131073));p.emit('message',Buffer.from([1,2]),true);assert.equal(e.udps[0].pending.length,0);assert.equal(e.gateway.snapshot().sessions[0].reason,'wire_rate');await e.gateway.close();});
 await test('late_callback_checks_500ms_even_before_timer_dispatch',async()=>{const e=await environment(),p=e.admit();p.emit('message',Buffer.from([1,2]),true);e.elapseWithoutTasks(500);e.udps[0].pending[0].cb();assert.equal(e.gateway.snapshot().sessions[0].reason,'backlog_timeout');assert.equal(e.gateway.snapshot().counters.to_udp_datagrams,0);await e.gateway.close();});
 await test('30_minute_run_absolute_despite_application_and_pongs',async()=>{const e=await environment(),p=e.admit();for(let i=0;i<359;i++){await e.advance(5000);p.emit('pong',p.pingBytes);p.emit('message',Buffer.from([1,2]),true);e.udps[0].pending.at(-1).cb();}await e.advance(4999);assert.equal(e.gateway.snapshot().active,1);await e.advance(1);assert.equal(e.gateway.snapshot().cleanup.reason,'run_timeout');await e.gateway.close();});
 return results;
};
