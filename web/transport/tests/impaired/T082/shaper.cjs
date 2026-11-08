'use strict';
// Actual child-only I/O instrumentation; no socket is created on import.
// Fixtures inject their own factory/monotonic clock/timers, never real dgram.
const PRESET=Object.freeze({schema_version:1,profile:'delay40_drop50_v1',delay_ms:40,drop_every:50,queue_datagrams:64,queue_bytes:131072,max_pending_ms:500});
function install({dgram,now,setTimer,clearTimer}){
 const originalFactory=dgram.createSocket,sockets=[],events=[],faults=[];
 let restored=false,closed=false,serial=0;
 const counts=()=>({observed:0,bytes:0,dropped:0,scheduled:0,delivered:0,canceled:0,errors:0,pending:0,pending_bytes:0,peak_datagrams:0,peak_bytes:0,callback_calls:0,callback_errors:0,late_callbacks:0,delay_count:0,delay_min_ms:null,delay_max_ms:null,histogram:{'40_49':0,'50_99':0,'100_499':0}});
 const dirs=Object.fromEntries(['up','down'].map(name=>[name,{name,stats:counts(),jobs:new Map(),timer:null,pumping:false}]));
 function fault(code){if(faults.length<512)faults.push(code);else if(!faults.includes('fault_overflow'))faults[511]='fault_overflow';}
 function event(value){if(events.length<512)events.push(value);else fault('event_overflow');}
 function refuse(code){fault(code);throw Error('T082 '+code);}
 function bump(d,s,key,n=1){d.stats[key]+=n;s.stats[d.name][key]+=n;}
 function callback(d,s,fn,error){if(!fn)return;bump(d,s,'callback_calls');if(error)bump(d,s,'callback_errors');try{fn(error||null);}catch(_){fault('user_callback_throw');}}
 function finish(d,j,outcome,error){
  if(!d.jobs.has(j.id)){if(j.cb)bump(d,j.s,'late_callbacks');return;}
  d.jobs.delete(j.id);bump(d,j.s,'pending',-1);bump(d,j.s,'pending_bytes',-j.size);bump(d,j.s,outcome);
  if(outcome==='delivered'){
   for(const c of [d.stats,j.s.stats[d.name]]){c.delay_count++;c.delay_min_ms=c.delay_min_ms===null?j.delay:Math.min(c.delay_min_ms,j.delay);c.delay_max_ms=c.delay_max_ms===null?j.delay:Math.max(c.delay_max_ms,j.delay);c.histogram[j.delay<50?'40_49':j.delay<100?'50_99':'100_499']++;}
  }
  j.outcome=outcome;j.bytes=null;callback(d,j.s,j.cb,error);j.cb=null;arm(d);
 }
 function arm(d){
  if(d.pumping)return;
  if(d.timer!==null){clearTimer(d.timer);d.timer=null;}
  if(closed||!d.jobs.size)return;
  let deadline=Infinity;
  for(const j of d.jobs.values())deadline=Math.min(deadline,j.created+500,j.state==='waiting'?j.created+40:Infinity);
  d.timer=setTimer(()=>{d.timer=null;pump(d);},Math.max(0,deadline-now()));
 }
 function pump(d){
  d.pumping=true;
  try{
   for(const j of [...d.jobs.values()]){
    if(!d.jobs.has(j.id))continue;
    const age=now()-j.created;
    if(age>=500){fault('pending_deadline');finish(d,j,'errors',Error('T082 pending deadline'));continue;}
    if(j.state!=='waiting'||age<40)continue;
    j.state='inflight';j.delay=age;
    try{
     if(d.name==='up')j.s.send.call(j.s.socket,j.bytes,error=>{
      if(!d.jobs.has(j.id)){bump(d,j.s,'late_callbacks');if(j.outcome!=='canceled')fault('native_duplicate_callback');return;}
      if(error){fault('native_send_error');finish(d,j,'errors',error);}else finish(d,j,'delivered');
     });
     else {const bytes=j.bytes,info=j.info;finish(d,j,'delivered');j.s.emit.call(j.s.socket,'message',bytes,info);}
    }catch(error){fault('delivery_throw');finish(d,j,'errors',error);}
   }
  }finally{d.pumping=false;arm(d);}
 }
 function enqueue(d,s,bytes,cb,info){
  if(closed||s.closed)return refuse('closed_socket_io');
  if(!Buffer.isBuffer(bytes)||bytes.length<2||bytes.length>4096)return refuse('raw_length_type');
  const copy=Buffer.from(bytes),size=copy.length; // Copy before asynchronous scheduling.
  bump(d,s,'observed');bump(d,s,'bytes',size);const ordinal=d.stats.observed;
  if(ordinal%50===0){bump(d,s,'dropped');event({kind:'profile_drop',direction:d.name,ordinal,socket:s.id});callback(d,s,cb);return;}
  bump(d,s,'scheduled');
  if(d.stats.pending>=64||d.stats.pending_bytes+size>131072){bump(d,s,'errors');fault('queue_overflow');callback(d,s,cb,Error('T082 queue overflow'));return;}
  const j={id:++serial,s,size,bytes:copy,cb,info:info?{...info}:null,created:now(),state:'waiting'};d.jobs.set(j.id,j);bump(d,s,'pending');bump(d,s,'pending_bytes',size);
  for(const c of [d.stats,s.stats[d.name]]){c.peak_datagrams=Math.max(c.peak_datagrams,c.pending);c.peak_bytes=Math.max(c.peak_bytes,c.pending_bytes);}
  arm(d);
 }
 function cancelSocket(s){for(const d of Object.values(dirs))for(const j of [...d.jobs.values()])if(j.s===s)finish(d,j,'canceled',j.cb?Error('T082 owned socket close'):null);}
 function factory(...args){
  if(closed||args.length!==1||args[0]!=='udp4'||sockets.length>=2)return refuse('unknown_socket_factory');
  const socket=originalFactory.apply(dgram,args),s={id:sockets.length+1,socket,send:socket.send,emit:socket.emit,close:socket.close,closed:false,stats:{up:counts(),down:counts()}};sockets.push(s);
  socket.send=function(...sendArgs){if(sendArgs.length!==2||typeof sendArgs[1]!=='function')return refuse('unknown_send_signature');enqueue(dirs.up,s,sendArgs[0],sendArgs[1]);};
  socket.emit=function(name,...values){
   if(name==='message'){
    const [bytes,info]=values;
    if(values.length!==2||!info||info.address!=='127.0.0.1'||info.port!==29863||info.family!=='IPv4'||info.size!==bytes?.length)return refuse('unknown_message_signature');
    enqueue(dirs.down,s,bytes,null,info);return true;
   }
   if(name==='close'){s.closed=true;cancelSocket(s);}
   if(name==='error')fault('native_socket_error');
   return s.emit.call(socket,name,...values);
  };
  socket.close=function(...closeArgs){cancelSocket(s);return s.close.apply(socket,closeArgs);};
  return socket;
 }
 dgram.createSocket=factory;
 function snapshot(){return JSON.parse(JSON.stringify({schema_version:1,profile:PRESET.profile,preset:PRESET,status:faults.length?'FAIL':closed?'CLOSED':'RUNNING',directions:Object.fromEntries(Object.entries(dirs).map(([n,d])=>[n,d.stats])),sockets:sockets.map(s=>({id:s.id,closed:s.closed,up:s.stats.up,down:s.stats.down})),events,faults,cleanup:{closed,restored,open_sockets:sockets.filter(s=>!s.closed).length,timers:Object.values(dirs).filter(d=>d.timer!==null).length,buffers:Object.values(dirs).reduce((n,d)=>n+d.jobs.size,0),pending_bytes:Object.values(dirs).reduce((n,d)=>n+d.stats.pending_bytes,0)}}));}
 function close(){
  if(closed)return snapshot();closed=true;
  for(const s of sockets)cancelSocket(s);
  for(const d of Object.values(dirs))if(d.timer!==null){clearTimer(d.timer);d.timer=null;}
  if(dgram.createSocket===factory){dgram.createSocket=originalFactory;restored=true;}else fault('factory_replaced');
  for(const s of sockets){s.socket.send=s.send;s.socket.emit=s.emit;s.socket.close=s.close;}
  return snapshot();
 }
 return {snapshot,close};
}
module.exports={PRESET,install};
