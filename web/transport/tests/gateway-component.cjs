'use strict';
// T057 real gateway bytes against a SYNTHETIC UDP echo, never ENet/game proof.
const assert=require('node:assert/strict'),crypto=require('node:crypto'),net=require('node:net'),dgram=require('node:dgram');
const beforeHandles=process._getActiveHandles().map(h=>h.constructor.name).sort();
const beforeRequests=process._getActiveRequests().map(h=>h.constructor.name).sort();
const fs=require('node:fs'),closeBefore=fs.close,closeSyncBefore=fs.closeSync;
const {startGateway}=require('../gateway.cjs');
assert.deepEqual(process._getActiveHandles().map(h=>h.constructor.name).sort(),beforeHandles);
assert.deepEqual(process._getActiveRequests().map(h=>h.constructor.name).sort(),beforeRequests);
assert.equal(fs.close,closeBefore);assert.equal(fs.closeSync,closeSyncBefore);
assert.equal(Object.keys(require.cache).filter(p=>p.includes('/vendor/ws-8.21.0/')).length,14);
assert.ok(!Object.keys(require.cache).some(p=>p.endsWith('.node')));
const WS=require('../vendor/ws-8.21.0/index.js');
const policy=require('./gateway-policy.cjs');
const result={kind:'T057 GATEWAY COMPONENT / SYNTHETIC UDP ONLY',game_verified:false,import_no_handles:true,cases:[],snapshots:[],cleanup:{}};
const clients=new Set(),rawClients=new Set();let gateway,upstream,upstreamCount=0,received=[];
const delay=ms=>new Promise(r=>setTimeout(r,ms));
const check=(name,detail={})=>result.cases.push({name,status:'PASS',...detail});
const digest=b=>crypto.createHash('sha256').update(b).digest('hex');
const tokens=()=>[crypto.randomBytes(16).toString('base64url'),crypto.randomBytes(16).toString('base64url')];
const allSecrets=[];
function configuration(caps){allSecrets.push(...caps);return {schema_version:1,run_id:crypto.randomBytes(16).toString('hex'),capability_sha256:caps.map(digest)};}
async function until(fn){for(let i=0;i<150;i++){if(fn())return;await delay(5);}throw Error('condition_timeout');}
async function fresh(){const caps=tokens();gateway=await startGateway(configuration(caps));return caps;}
async function connect(cap,standardOffer=false){
 const ws=new WS(`ws://127.0.0.1:29865/enet?cap=${cap}`,'outbreak-enet-dgram.v1',{headers:{Host:'outbreak.localhost:29865'},origin:'http://outbreak.localhost:29866',perMessageDeflate:standardOffer,maxPayload:4096});
 // Vendored websocket.js emits upgrade before clearing its ClientRequest.
 // IncomingMessage here has no response.req; read the inspected request then.
 ws.on('upgrade',response=>{ws.testUpgrade={request_extensions:ws._req?.getHeader('Sec-WebSocket-Extensions')??null,response_extensions:response.headers['sec-websocket-extensions']??null};});
 clients.add(ws);ws.on('error',()=>{});ws.on('close',()=>clients.delete(ws));
 await new Promise((resolve,reject)=>{ws.once('open',resolve);ws.once('error',()=>reject(Error('client_open_failed')));});
 await until(()=>gateway.snapshot().sessions.filter(s=>s.state==='active').every(s=>s.upstream_connected));return ws;
}
function closing(ws){return new Promise(resolve=>ws.once('close',code=>resolve(code)));}
async function echo(ws,payload,fragments=1){
 const msg=new Promise(resolve=>ws.once('message',(data,binary)=>resolve({data,binary})));
 if(fragments===1)ws.send(payload,{binary:true});else for(let i=0;i<fragments;i++)ws.send(payload.subarray(i*2,i*2+2),{binary:true,fin:i===fragments-1});
 const m=await msg;assert.ok(m.binary);assert.deepEqual(m.data,payload);
}
function rawRequest(cap,extra=[],route){
 return ['GET '+(route||`/enet?cap=${cap}`)+' HTTP/1.1','Host: outbreak.localhost:29865','Upgrade: websocket','Connection: Upgrade','Sec-WebSocket-Key: '+crypto.randomBytes(16).toString('base64'),'Sec-WebSocket-Version: 13','Sec-WebSocket-Protocol: outbreak-enet-dgram.v1',...extra,'',''].join('\r\n');
}
async function rejectRaw(request){
 let reply='';const s=net.createConnection({host:'127.0.0.1',port:29865});rawClients.add(s);s.on('error',()=>{});
 const done=new Promise(resolve=>s.once('close',()=>{rawClients.delete(s);resolve();}));
 s.on('data',b=>{if(reply.length<8192)reply+=b.toString('ascii');});
 s.once('connect',()=>s.write(request));await done;assert.match(reply,/^HTTP\/1.1 (403|400)/);
}
async function finishGroup(){
 const first=gateway.close('test_complete'),second=gateway.close('second_call');assert.equal(first,second);await first;
 const s=gateway.snapshot();assert.equal(s.cleanup.state,'closed');assert.equal(s.cleanup.timers,0);assert.equal(s.cleanup.tcp_handles,0);assert.equal(s.cleanup.udp_handles,0);
 for(const session of s.sessions){assert.equal(session.to_udp.pending_bytes,0);assert.equal(session.to_ws.pending_bytes,0);assert.equal(session.control_pending_bytes,0);}
 s.counters.admitted=-999;assert.notEqual(gateway.snapshot().counters.admitted,-999);
 result.snapshots.push(gateway.snapshot());gateway=null;
}
async function run(){
 result.policy_cases=policy();
 result.mock_cases=await require('./gateway-mocks.cjs')();
 for(const config of [{},{schema_version:1,run_id:'a'.repeat(32),capability_sha256:['b'.repeat(64),'b'.repeat(64)]},{schema_version:1,run_id:'a'.repeat(32),capability_sha256:['b'.repeat(64),'c'.repeat(64)],unknown:1}]){
  await assert.rejects(startGateway(config),/invalid_config/);
 }
 check('invalid_config_before_listen');
 upstream=dgram.createSocket('udp4');upstream.on('error',()=>{result.upstream_error=true;});
 upstream.on('message',(data,info)=>{upstreamCount++;if(received.length<64)received.push({port:info.port,length:data.length,sha256:digest(data)});upstream.send(data,info.port,'127.0.0.1',()=>{});});
 await new Promise((resolve,reject)=>{upstream.once('error',reject);upstream.bind(29863,'127.0.0.1',resolve);});
 let caps=await fresh();
 await rejectRaw(rawRequest(caps[0],['Origin: http://wrong.invalid']));
 await rejectRaw(rawRequest(caps[0],['Origin: http://outbreak.localhost:29866','Origin: http://outbreak.localhost:29866']));
 await rejectRaw(rawRequest(caps[0],['Origin: http://outbreak.localhost:29866'],`/enet?cap=${caps[0]}&cap=${caps[0]}`));
 assert.equal(gateway.snapshot().counters.udp_allocated,0);check('bad_duplicate_route_admission_before_udp');
 const a=await connect(caps[0]),b=await connect(caps[1]);
 for(const size of [2,1400,4096]){await echo(a,Buffer.alloc(size,0x41));await echo(b,Buffer.alloc(size,0x42));}
 const snap=gateway.snapshot(),ports=snap.sessions.map(s=>s.udp_tuple.port);
 assert.notEqual(ports[0],ports[1]);assert.equal(received.length,6);
 for(const r of received){const marker=r.sha256===digest(Buffer.alloc(r.length,0x41))?0:1;assert.equal(r.port,ports[marker]);}
 check('real_2_1400_4096_bytes_and_AB_tuple_isolation',{tuples:ports,datagrams:6});
 await rejectRaw(rawRequest(caps[0],['Origin: http://outbreak.localhost:29866']));check('third_active_session_rejected');
 const ac=closing(a);a.close();await ac;await until(()=>gateway.snapshot().active===1);
 await rejectRaw(rawRequest(caps[0],['Origin: http://outbreak.localhost:29866']));check('consumed_capability_replay_rejected');
 assert.equal(gateway.snapshot().counters.udp_allocated,2);await finishGroup();
 caps=await fresh();let x=await connect(caps[0]);let before=upstreamCount,done=closing(x);x.send('text');assert.equal(await done,1003);assert.equal(upstreamCount,before);check('text_reject_before_udp');
 x=await connect(caps[1]);before=upstreamCount;done=closing(x);x.send(Buffer.alloc(4097));assert.equal(await done,1009);assert.equal(upstreamCount,before);check('4097_parser_rejection_before_udp');await finishGroup();
 caps=await fresh();x=await connect(caps[0]);await echo(x,Buffer.alloc(32,7),16);check('sixteen_nonempty_fragment_delivery');
 before=upstreamCount;done=closing(x);for(let i=0;i<17;i++)x.send(Buffer.alloc(2,8),{binary:true,fin:i===16});assert.equal(await done,1008);assert.equal(upstreamCount,before);check('seventeen_nonempty_fragment_rejection');
 x=await connect(caps[1]);done=closing(x);x.terminate();await done;await until(()=>gateway.snapshot().active===0);assert.equal(gateway.snapshot().retired,2);check('abrupt_loss_retires_owned_tuples');await finishGroup();
 caps=await fresh();const held=[];
 for(let i=0;i<4;i++){const s=net.createConnection({host:'127.0.0.1',port:29865});held.push(s);rawClients.add(s);s.on('error',()=>{});s.on('close',()=>rawClients.delete(s));await new Promise(r=>s.once('connect',r));}
 await until(()=>gateway.snapshot().pending_tcp===4);
 const fifth=net.createConnection({host:'127.0.0.1',port:29865});rawClients.add(fifth);fifth.on('error',()=>{});await new Promise(r=>fifth.once('close',()=>{rawClients.delete(fifth);r();}));
 assert.equal(gateway.snapshot().pending_tcp,4);check('pending_tcp_four_cap');
 await delay(2100);await until(()=>gateway.snapshot().pending_tcp===0);check('two_second_header_deadline');
 for(let i=0;i<9;i++)await rejectRaw(rawRequest(caps[0],['Origin: http://wrong.invalid']));
 assert.ok(gateway.snapshot().diagnostics.some(e=>e.reason==='upgrade_limit'));check('eight_upgrade_attempt_budget');await finishGroup();
 caps=await fresh();
 const valid=()=>rawRequest(caps[0],['Origin: http://outbreak.localhost:29866']);
 const invalids=[
  valid().replace('Host: outbreak.localhost:29865','Host: localhost:29865'),
  valid().replace('Origin: http://outbreak.localhost:29866\r\n',''),
  valid().replace('Origin: http://outbreak.localhost:29866','Origin: null'),
  valid().replace('Sec-WebSocket-Protocol: outbreak-enet-dgram.v1','Sec-WebSocket-Protocol: outbreak-enet-dgram.v1, other'),
  valid().replace('Sec-WebSocket-Version: 13','Sec-WebSocket-Version: 8'),
  valid().replace('Origin:','Sec-WebSocket-Extensions: permessage-deflate\r\nOrigin:'),
  valid().replace('/enet?cap=','/enet?cap=%41'),
  valid().replace('GET /enet','POST /enet')
 ];
 for(const request of invalids)await rejectRaw(request);
 assert.equal(gateway.snapshot().counters.udp_allocated,0);assert.equal(gateway.snapshot().counters.admitted,0);check('exact_host_origin_protocol_version_extensions_encoding_method_matrix',{rejections:8});await finishGroup();
 caps=await fresh();
 await rejectRaw(rawRequest(caps[0],['Origin: http://outbreak.localhost:29866']).replace(/Sec-WebSocket-Key: [^\r]+/,'Sec-WebSocket-Key: invalid'));
 assert.equal(gateway.snapshot().counters.udp_allocated,0);
 await rejectRaw(rawRequest(caps[0],['Origin: http://outbreak.localhost:29866']));check('library_RFC_key_failure_burns_cap_without_udp');
 const header=Buffer.from(rawRequest(caps[1],['Origin: http://outbreak.localhost:29866']));
 // Public vendored frame encoder, not a gateway/test handwritten frame parser.
 const frame=Buffer.concat(WS.Sender.frame(Buffer.from([0x33,0x44]),{fin:true,opcode:2,mask:true,readOnly:true}));
 const raw=net.createConnection({host:'127.0.0.1',port:29865});rawClients.add(raw);raw.on('error',()=>{});raw.on('data',()=>{});raw.on('close',()=>rawClients.delete(raw));
 const wireBefore=gateway.snapshot().counters.wire_bytes,countBefore=upstreamCount;
 await new Promise(resolve=>raw.once('connect',()=>{raw.write(Buffer.concat([header,frame]),resolve);}));
 await until(()=>upstreamCount===countBefore+1);
 const wireAfter=gateway.snapshot().counters.wire_bytes;
 result.wire_head_observation={wire_bytes:wireAfter-wireBefore,expected:header.length+frame.length,encoded_frame_bytes:frame.length};
 assert.equal(wireAfter-wireBefore,header.length+frame.length);
 assert.equal(received.at(-1).sha256,digest(Buffer.from([0x33,0x44])));
 check('coalesced_upgrade_head_wire_bytes_counted_exactly_once',{wire_bytes:wireAfter-wireBefore,expected:header.length+frame.length});
 const rawClosed=new Promise(resolve=>raw.once('close',resolve));raw.destroy();await rawClosed;await finishGroup();
 caps=await fresh();
 for(const offer of [
  ['Sec-WebSocket-Extensions: unknown'],
  ['Sec-WebSocket-Extensions: permessage-deflate; client_max_window_bits, permessage-deflate; client_max_window_bits'],
  ['Sec-WebSocket-Extensions: permessage-deflate; client_max_window_bits','Sec-WebSocket-Extensions: permessage-deflate; client_max_window_bits'],
  ['Sec-WebSocket-Extensions: permessage-deflate; client_max_window_bits=12']
 ])await rejectRaw(rawRequest(caps[0],['Origin: http://outbreak.localhost:29866',...offer]));
 assert.equal(gateway.snapshot().counters.udp_allocated,0);assert.equal(gateway.snapshot().counters.admitted,0);check('D043_unknown_duplicate_modified_extension_offers_rejected_before_udp',{rejections:4});
 x=await connect(caps[0],true);
 assert.equal(x.testUpgrade.request_extensions,'permessage-deflate; client_max_window_bits');
 assert.equal(x.testUpgrade.response_extensions,null);assert.equal(x.extensions,'');
 await echo(x,Buffer.from([0x55,0x66]));await echo(x,Buffer.alloc(4096,0x71));
 check('D043_exact_standard_offer_admitted_without_negotiation',{...x.testUpgrade,negotiated_extensions:x.extensions,transport:'Node ws component client reproducing exact offer; NOT browser proof'});
 before=upstreamCount;done=closing(x);
 // Vendor public encoder supplies one controlled RSV1 frame. No hand parser,
 // compression negotiation, malformed ENet, flood or browser execution.
 x._socket.write(Buffer.concat(WS.Sender.frame(Buffer.from([0x77,0x88]),{fin:true,opcode:2,rsv1:true,mask:true,readOnly:true})));
 assert.equal(await done,1002);assert.equal(upstreamCount,before);
 assert.equal(gateway.snapshot().sessions[0].parser_error,'WS_ERR_UNEXPECTED_RSV_1');
 check('D043_unnegotiated_RSV1_rejected_before_udp',{client_close_code:1002,parser_error:'WS_ERR_UNEXPECTED_RSV_1'});await finishGroup();
}
let watchdog=setTimeout(()=>{for(const c of clients)c.terminate();for(const s of rawClients)s.destroy();if(gateway)void gateway.close('watchdog');},18000);
(async()=>{
 try{await run();result.status='PASS';}catch(error){result.status='FAIL';result.failure={code:error.code==='ERR_ASSERTION'?'ERR_ASSERTION':'component_socket_or_timeout',source_frames:String(error.stack).split('\n').slice(1).filter(line=>line.includes('/web/transport/')).map(line=>(line.match(/\/web\/transport\/[^ )]+:\d+:\d+/)||['redacted'])[0]).slice(0,8)};}
 finally{
  clearTimeout(watchdog);for(const c of clients)c.terminate();for(const s of rawClients)s.destroy();
  if(gateway){await gateway.close('test_failure');result.snapshots.push(gateway.snapshot());}
  if(upstream)await new Promise(resolve=>{try{upstream.close(resolve);}catch{resolve();}});
  await delay(20);
  result.cleanup.active_network_handles=process._getActiveHandles().filter(h=>['Socket','Server'].includes(h.constructor.name)&&h!==process.stdout&&h!==process.stderr).map(h=>h.constructor.name);
  result.cleanup.client_count=clients.size;result.cleanup.raw_client_count=rawClients.size;
  result.synthetic_udp_received=received;
  if(result.cleanup.active_network_handles.length||clients.size||rawClients.size||result.upstream_error)result.status='FAIL';
  let output=JSON.stringify(result);
  if(allSecrets.some(secret=>output.includes(secret))||Buffer.byteLength(output)>8388608){result.status='FAIL';output=JSON.stringify({status:'FAIL',failure:'redaction_or_output_limit'});}
  console.log(output);process.exitCode=result.status==='PASS'?0:1;
 }
})();
