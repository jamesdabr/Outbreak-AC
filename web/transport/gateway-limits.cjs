'use strict';
// Frozen T057 / EXPERIMENTAL_TRANSPORT 0.1 policy. No I/O or timers on import.
const LIMITS = Object.freeze({active:2,retired:4,udpTotal:6,pendingTCP:4,headerMs:2000,attempts:8,
  minPayload:2,maxPayload:4096,packetRate:256,packetBurst:64,byteRate:524288,byteBurst:131072,
  udpPending:64,pendingBytes:131072,backlogMs:500,wireRate:1048576,wireBurst:131072,
  controlRate:4,controlBurst:8,pingMs:5000,pongMs:10000,idleMs:30000,sessionMs:150000,runMs:180000,
  retireMs:60000,diagnostics:512,outputBytes:8388608});
class Bucket {
  constructor(rate,burst,now){this.rate=rate;this.burst=burst;this.tokens=burst;this.at=now;}
  available(n,now){this.tokens=Math.min(this.burst,this.tokens+Math.max(0,now-this.at)*this.rate/1000);this.at=now;return n<=this.tokens;}
  take(n,now){if(!this.available(n,now))return false;this.tokens-=n;return true;}
}
class Flow {
  constructor(now,udp=false){this.packets=new Bucket(LIMITS.packetRate,LIMITS.packetBurst,now);this.bytes=new Bucket(LIMITS.byteRate,LIMITS.byteBurst,now);this.udp=udp;this.pending=new Map();this.pendingBytes=0;this.serial=0;}
  reserve(size,now,buffered=0){
    if(size<LIMITS.minPayload||size>LIMITS.maxPayload)return {reason:'payload_size'};
    if(!this.packets.available(1,now)||!this.bytes.available(size,now))return {reason:'direction_rate'};
    if((this.udp&&this.pending.size>=LIMITS.udpPending)||buffered+this.pendingBytes+size>LIMITS.pendingBytes)return {reason:'pending_limit'};
    if(this.expired(now))return {reason:'backlog_timeout'};
    this.packets.take(1,now);this.bytes.take(size,now);
    const id=++this.serial;this.pending.set(id,{size,at:now});this.pendingBytes+=size;return {id};
  }
  release(id){const item=this.pending.get(id);if(!item)return false;this.pending.delete(id);this.pendingBytes-=item.size;return true;}
  clear(){this.pending.clear();this.pendingBytes=0;}
  oldest(){return this.pending.size?this.pending.values().next().value.at:Infinity;}
  expired(now){return now-this.oldest()>=LIMITS.backlogMs;}
  snapshot(){return {pending_sends:this.pending.size,pending_bytes:this.pendingBytes};}
}
const current=(session,generation)=>!session.closed&&session.generation===generation;
function deadline(s){
  return Math.min(s.born+LIMITS.sessionMs,s.lastData+LIMITS.idleMs,s.nextPing,
    s.pingAt===null?Infinity:s.pingAt+LIMITS.pongMs,
    s.toUDP.oldest()+LIMITS.backlogMs,s.toWS.oldest()+LIMITS.backlogMs,s.controlOldest+LIMITS.backlogMs);
}
function overdue(s,now){
  if(now>=s.born+LIMITS.sessionMs)return 'session_timeout';
  if(now>=s.lastData+LIMITS.idleMs)return 'application_idle';
  if(s.pingAt!==null&&now>=s.pingAt+LIMITS.pongMs)return 'pong_timeout';
  if(s.toUDP.expired(now)||s.toWS.expired(now)||now-s.controlOldest>=LIMITS.backlogMs)return 'backlog_timeout';
  return null;
}
module.exports={LIMITS,Bucket,Flow,current,deadline,overdue};
