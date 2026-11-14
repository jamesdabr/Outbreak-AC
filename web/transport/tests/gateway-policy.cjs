'use strict';
const assert=require('node:assert/strict');
const {LIMITS:L,Bucket,Flow,current,deadline,overdue}=require('../gateway-limits.cjs');
module.exports=function policyTests(){
  const passed=[];function test(name,fn){fn();passed.push({name,status:'PASS',kind:'deterministic policy / fake clock, not network'});}
  test('packet_rate_before_forward',()=>{const f=new Flow(0,true);let forwarded=0;for(let i=0;i<65;i++){const r=f.reserve(2,0);if(!r.reason)forwarded++;}assert.equal(forwarded,64);assert.equal(f.pending.size,64);});
  test('udp_pending_count_and_once_release',()=>{const f=new Flow(0,true);for(let i=0;i<64;i++)assert.ok(f.reserve(2,0).id);assert.equal(f.reserve(2,250).reason,'pending_limit');assert.equal(f.release(1),true);assert.equal(f.release(1),false);assert.equal(f.pendingBytes,126);f.clear();assert.equal(f.pendingBytes,0);assert.equal(f.release(2),false);});
  test('pending_bytes_and_ws_buffered_plus_own',()=>{const f=new Flow(0,true);for(let i=0;i<32;i++)assert.ok(f.reserve(4096,0).id);assert.equal(f.reserve(2,250).reason,'pending_limit');const w=new Flow(0);assert.equal(w.reserve(2,0,L.pendingBytes-1).reason,'pending_limit');assert.equal(w.pending.size,0);});
  test('byte_bucket_boundary',()=>{const b=new Bucket(L.byteRate,L.byteBurst,0);assert.ok(b.take(131072,0));assert.equal(b.take(1,0),false);assert.ok(b.take(524,1));});
  test('wire_and_control_buckets',()=>{const wire=new Bucket(L.wireRate,L.wireBurst,0);assert.ok(wire.take(131072,0));assert.equal(wire.take(1,0),false);assert.ok(wire.take(1024,1));const control=new Bucket(4,8,0);for(let i=0;i<8;i++)assert.ok(control.take(1,0));assert.equal(control.take(1,0),false);assert.ok(control.take(1,250));});
  test('size_and_500ms_backlog',()=>{const f=new Flow(0,true);assert.equal(f.reserve(1,0).reason,'payload_size');assert.equal(f.reserve(4097,0).reason,'payload_size');assert.ok(f.reserve(2,0).id);assert.equal(f.expired(499),false);assert.equal(f.reserve(2,500).reason,'backlog_timeout');});
  test('generation_guard_stops_late_forward',()=>{const s={closed:false,generation:1};assert.ok(current(s,1));s.closed=true;s.generation++;let forwarded=0;if(current(s,1))forwarded++;assert.equal(forwarded,0);});
  test('fake_clock_deadlines',()=>{const s={born:0,lastData:0,nextPing:5000,pingAt:null,toUDP:new Flow(0,true),toWS:new Flow(0),controlOldest:Infinity};assert.equal(deadline(s),5000);assert.equal(overdue(s,29999),null);assert.equal(overdue(s,30000),'application_idle');s.lastData=L.sessionMs-1;assert.equal(overdue(s,L.sessionMs),'session_timeout');s.lastData=0;s.pingAt=5000;assert.equal(overdue(s,14999),null);assert.equal(overdue(s,15000),'pong_timeout');});
  return passed;
};
