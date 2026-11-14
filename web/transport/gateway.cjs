'use strict';
const http=require('node:http');
const dgram=require('node:dgram');
const crypto=require('node:crypto');
const {performance}=require('node:perf_hooks');
const WS=require('./vendor/ws-8.21.0/index.js');
const {LIMITS:L,Bucket,Flow,current,deadline,overdue}=require('./gateway-limits.cjs');
const now=()=>performance.now();
const HOST='127.0.0.1',FRONTEND_HOST='outbreak.localhost',PORT=29865,UPSTREAM=29863,ORIGIN='http://outbreak.localhost:29866',PROTOCOL='outbreak-enet-dgram.v1';
const STANDARD_OFFER='permessage-deflate; client_max_window_bits';
function firstFailedAdmissionHeader(req,h,seen){
  if(req.method!=='GET')return 'method';
  if(h.host!==`${FRONTEND_HOST}:${PORT}`)return 'host';
  if(h.origin!==ORIGIN)return 'origin';
  if(h['sec-websocket-version']!=='13')return 'version';
  if(h['sec-websocket-protocol']!==PROTOCOL)return 'protocol';
  if(h.upgrade?.toLowerCase()!=='websocket')return 'upgrade';
  if(!h.connection?.toLowerCase().split(/\s*,\s*/).includes('upgrade'))return 'connection';
  if(!h['sec-websocket-key'])return 'key';
  if(seen.has('sec-websocket-extensions')&&h['sec-websocket-extensions']!==STANDARD_OFFER)return 'extensions';
  if(seen.has('cookie'))return 'cookie';
  if(seen.has('authorization'))return 'authorization';
  if(seen.has('proxy-authorization'))return 'proxy_authorization';
  return null;
}
function configValues(config){
  if(!config||Object.getPrototypeOf(config)!==Object.prototype)throw Error('invalid_config');
  const descriptors=Object.getOwnPropertyDescriptors(config),keys=Reflect.ownKeys(descriptors);
  if(keys.length!==3||!['schema_version','run_id','capability_sha256'].every(k=>Object.hasOwn(descriptors,k)&&Object.hasOwn(descriptors[k],'value')))throw Error('invalid_config');
  const {schema_version,run_id,capability_sha256:caps}=config;
  if(schema_version!==1||typeof run_id!=='string'||!(/^[0-9a-f]{32}$/).test(run_id)||!Array.isArray(caps)||Object.getPrototypeOf(caps)!==Array.prototype||caps.length!==2||Reflect.ownKeys(caps).length!==3)throw Error('invalid_config');
  if(![0,1].every(i=>Object.hasOwn(Object.getOwnPropertyDescriptor(caps,String(i))||{},'value')&&typeof caps[i]==='string'&&(/^[0-9a-f]{64}$/).test(caps[i]))||caps[0]===caps[1])throw Error('invalid_config');
  return {run_id,hashes:caps.map(c=>Buffer.from(c,'hex'))};
}
async function startGateway(config){
  const {run_id,hashes}=configValues(config); // Never consult implicit configuration/environment.
  const used=[false,false],sessions=[],tcp=new Map(),udp=new Set(),timers=new Set(),diagnostics=[];
  const counters={tcp_accepted:0,tcp_rejected:0,upgrade_attempts:0,admitted:0,rejected:0,udp_allocated:0,
    to_udp_datagrams:0,to_udp_bytes:0,to_ws_datagrams:0,to_ws_bytes:0,retired_discarded:0,
    send_errors:0,late_callbacks:0,wire_bytes:0,control_received:0,diagnostic_overflow:0,peak_active:0,peak_pending_tcp:0,peak_retired:0,peak_udp:0};
  let closed=false,closing=null,runTimer,serial=0,failure=null;
  const cleanup={state:'starting',http_closed:false,ws_closed:false};
  const active=()=>sessions.filter(s=>!s.closed).length;
  const retired=()=>sessions.filter(s=>s.retired&&s.udp&&!s.udpClosed).length;
  const timer=(fn,ms)=>{const t=setTimeout(()=>{timers.delete(t);fn();},Math.max(0,ms));timers.add(t);return t;};
  const cancel=t=>{clearTimeout(t);timers.delete(t);};
  function record(reason,s){
    if(diagnostics.length>=L.diagnostics||(s&&s.records.length>=L.diagnostics)){
      counters.diagnostic_overflow++;failure='diagnostic_overflow';void close('diagnostic_overflow');return;
    }
    const entry={reason,session_id:s?s.id:null};diagnostics.push(entry);if(s)s.records.push({...entry});
  }
  const wss=new WS.WebSocketServer({noServer:true,maxPayload:L.maxPayload,maxFragments:16,maxBufferedChunks:32,
    perMessageDeflate:false,skipUTF8Validation:false,autoPong:false,closeTimeout:1000,
    handleProtocols:protocols=>protocols.has(PROTOCOL)?PROTOCOL:false});
  const server=http.createServer({maxHeaderSize:8192,headersTimeout:L.headerMs,requestTimeout:L.headerMs},(req,res)=>{
    const t=tcp.get(req.socket);if(t)reject(t,'ordinary_http');else req.socket.destroy();
  });
  function reject(t,reason){
    if(t.blocked)return;t.blocked=true;counters.rejected++;record(reason);
    if(t.session)finish(t.session,reason,1008);
    // Constant response only; no raw URL/header/error is ever reflected.
    if(!t.socket.destroyed)t.socket.end('HTTP/1.1 403 Forbidden\r\nConnection: close\r\nContent-Length: 0\r\n\r\n');
    cancel(t.deadline);t.deadline=timer(()=>t.socket.destroy(),50);
  }
  function closeUDP(s){
    if(!s.udp||s.udpClosed||s.udpClosing)return;
    s.udpClosing=true;
    if(s.udpBinding){s.udpClosing=false;s.closeRequested=true;return;}
    try{s.udp.close();}catch(e){if(e.code==='ERR_SOCKET_DGRAM_NOT_RUNNING'){s.udpClosed=true;udp.delete(s.udp);s.resolveUDP();}else{failure='udp_close_error';}}
  }
  function finish(s,reason,code=1008){
    if(s.closed)return;
    s.closed=true;s.generation++;s.reason=reason;record(reason,s);cancel(s.maintenance);
    s.toUDP.clear();s.toWS.clear();s.controlPending.clear();s.controlBytes=0;s.controlOldest=Infinity;
    s.pings=[];s.pingAt=null;
    if(s.ws&&s.ws.readyState!==WS.CLOSED){
      try{s.ws.close(code,'gateway policy');}catch{s.ws.terminate();}
    }
    if(s.udp&&!s.udpClosed){
      s.retired=true;s.retireAt=now()+L.retireMs;counters.peak_retired=Math.max(counters.peak_retired,retired());
      if(closed)closeUDP(s);else s.retirement=timer(()=>closeUDP(s),L.retireMs);
    }
  }
  function schedule(s){
    cancel(s.maintenance);if(s.closed||closed)return;
    s.maintenance=timer(()=>{
      if(s.closed||closed)return;
      const at=now(),reason=overdue(s,at);
      if(reason){finish(s,reason);return;}
      if(at>=s.nextPing){
        s.nextPing=at+L.pingMs;
        const nonce=crypto.randomBytes(8);s.pings.push({nonce,at});
        s.pingAt=s.pings[0].at;controlSend(s,'ping',nonce);
      }
      schedule(s);
    },deadline(s)-now());
  }
  function controlSend(s,method,data){
    if(s.closed||closed||!s.ws||s.ws.readyState!==WS.OPEN)return;
    const size=data.length;
    if(s.ws.bufferedAmount+s.toWS.pendingBytes+s.controlBytes+size>L.pendingBytes){finish(s,'pending_limit');return;}
    const id=++s.controlSerial,g=s.generation;
    s.controlPending.set(id,{at:now(),size});s.controlBytes+=size;
    s.controlOldest=s.controlPending.values().next().value.at;
    const callback=error=>{
      if(!current(s,g)||closed){counters.late_callbacks++;return;}
      const item=s.controlPending.get(id);
      if(item&&now()-item.at>=L.backlogMs){finish(s,'backlog_timeout');return;}
      if(item){s.controlPending.delete(id);s.controlBytes-=item.size;}
      s.controlOldest=s.controlPending.size?s.controlPending.values().next().value.at:Infinity;
      if(error){counters.send_errors++;finish(s,'ws_control_send_error',1011);}else schedule(s);
    };
    try{s.ws[method](data,false,callback);}catch{callback(true);}
    schedule(s);
  }
  function forward(s,direction,data){
    const g=s.generation;
    if(!current(s,g)||closed)return;
    const toUDP=direction==='udp',flow=toUDP?s.toUDP:s.toWS;
    if(!s.connected||!s.ws||s.ws.readyState!==WS.OPEN){finish(s,'upstream_not_ready',1011);return;}
    const reserve=flow.reserve(data.length,now(),toUDP?0:s.ws.bufferedAmount+s.controlBytes);
    if(reserve.reason){finish(s,reserve.reason,reserve.reason==='payload_size'&&data.length>L.maxPayload?1009:1008);return;}
    // Own copy only after admission, directional rate and pending limits.
    const payload=Buffer.from(data);
    s.lastData=now();
    const callback=error=>{
      if(!current(s,g)||closed){counters.late_callbacks++;return;}
      if(flow.expired(now())){finish(s,'backlog_timeout');return;}
      if(!flow.release(reserve.id))return;
      if(error){counters.send_errors++;finish(s,toUDP?'udp_send_error':'ws_send_error',1011);return;}
      counters[toUDP?'to_udp_datagrams':'to_ws_datagrams']++;
      counters[toUDP?'to_udp_bytes':'to_ws_bytes']+=payload.length;
      s.counters[toUDP?'to_udp_datagrams':'to_ws_datagrams']++;
      s.counters[toUDP?'to_udp_bytes':'to_ws_bytes']+=payload.length;
      schedule(s);
    };
    try{if(toUDP)s.udp.send(payload,callback);else s.ws.send(payload,{binary:true,compress:false},callback);}catch{callback(true);}
    schedule(s);
  }
  function connectSession(s,ws){
    if(s.closed||closed){ws.terminate();return;}
    s.ws=ws;ws.pause(); // No application queue while the owned UDP tuple binds/connects.
    ws.on('error',error=>{
      s.parserError=['WS_ERR_UNSUPPORTED_MESSAGE_LENGTH','WS_ERR_TOO_MANY_BUFFERED_PARTS','WS_ERR_INVALID_UTF8','WS_ERR_EXPECTED_MASK','WS_ERR_UNEXPECTED_RSV_1'].includes(error.code)?error.code:'ws_error';
      finish(s,'ws_error',1011);
    });
    ws.on('close',code=>{s.closeCode=code;finish(s,'ws_closed');});
    ws.on('message',(data,binary)=>{if(s.closed||closed)return;if(!binary){finish(s,'text_rejected',1003);return;}forward(s,'udp',data);});
    for(const type of ['ping','pong'])ws.on(type,data=>{
      if(s.closed||closed)return;
      counters.control_received++;
      if(!s.control.take(1,now())){finish(s,'control_rate');return;}
      if(type==='ping')controlSend(s,'pong',data);
      else{
        const index=s.pings.findIndex(p=>data.length===p.nonce.length&&crypto.timingSafeEqual(data,p.nonce));
        if(index>=0){s.pings.splice(index,1);s.pingAt=s.pings.length?s.pings[0].at:null;schedule(s);}
      }
    });
    const socket=dgram.createSocket('udp4');s.udp=socket;udp.add(socket);counters.udp_allocated++;counters.peak_udp=Math.max(counters.peak_udp,udp.size);
    s.udpDone=new Promise(resolve=>s.resolveUDP=resolve);
    socket.on('error',()=>{const binding=s.udpBinding;s.udpBinding=false;if(!s.closed)finish(s,'udp_error',1011);if(binding)closeUDP(s);});
    socket.on('close',()=>{s.udpClosed=true;udp.delete(socket);s.resolveUDP();});
    socket.on('message',(data,info)=>{
      if(s.closed||closed){counters.retired_discarded++;return;}
      if(info.address!==HOST||info.port!==UPSTREAM){finish(s,'udp_source_mismatch');return;}
      forward(s,'ws',data);
    });
    const g=s.generation;
    s.udpBinding=true;
    socket.bind(0,HOST,()=>{
      s.udpBinding=false;
      const a=socket.address();s.tuple={address:a.address,port:a.port,family:a.family};
      if(!current(s,g)||closed){if(closed||s.closeRequested)closeUDP(s);return;}
      try{socket.connect(UPSTREAM,HOST,()=>{
        if(!current(s,g)||closed)return;
        s.connected=true;ws.resume();schedule(s);
      });}catch{finish(s,'udp_connect_error',1011);}
    });
    schedule(s);
  }
  server.on('connection',socket=>{
    if(closed||[...tcp.values()].filter(t=>!t.session).length>=L.pendingTCP){counters.tcp_rejected++;socket.destroy();return;}
    const t={socket,session:null,blocked:false,wire:new Bucket(L.wireRate,L.wireBurst,now()),deadline:null};tcp.set(socket,t);counters.tcp_accepted++;
    counters.peak_pending_tcp=Math.max(counters.peak_pending_tcp,[...tcp.values()].filter(t=>!t.session).length);
    t.deadline=timer(()=>reject(t,'header_timeout'),L.headerMs);
    // Prepend ahead of Node HTTP / ws data listeners. Raw chunks include upgrade
    // head once; never charge head again after handleUpgrade/unshift.
    const wire=data=>{
      if(t.blocked)return;
      // Node may coalesce/copy an unshifted head. Its exact prefix length was
      // already charged in the original raw chunk; skip accounting only, not
      // data delivery, and charge any new bytes in the same re-emitted chunk.
      const replay=Math.min(t.replayedBytes||0,data.length);
      t.replayedBytes=(t.replayedBytes||0)-replay;
      const fresh=data.length-replay;counters.wire_bytes+=fresh;
      if(!t.wire.take(fresh,now())){if(t.session)finish(t.session,'wire_rate');else reject(t,'wire_rate');socket.destroy();}
    };
    socket.prependListener('data',wire);
    socket.on('error',()=>{if(t.session)finish(t.session,'tcp_error',1011);});
    socket.on('close',()=>{cancel(t.deadline);tcp.delete(socket);if(t.session)finish(t.session,'tcp_closed');});
  });
  server.on('clientError',(_,socket)=>{const t=tcp.get(socket);if(t)reject(t,'http_parse_error');else socket.destroy();});
  server.on('upgrade',(req,socket,head)=>{
    const t=tcp.get(socket);if(!t||t.blocked||closed){socket.destroy();return;}
    counters.upgrade_attempts++;
    if(counters.upgrade_attempts>L.attempts){reject(t,'upgrade_limit');return;}
    const seen=new Set();
    for(let i=0;i<req.rawHeaders.length;i+=2){const k=req.rawHeaders[i].toLowerCase();if(seen.has(k)){reject(t,'duplicate_header');return;}seen.add(k);}
    const h=req.headers;
    if(req.method!=='GET'||h.host!==`${FRONTEND_HOST}:${PORT}`||h.origin!==ORIGIN||h['sec-websocket-version']!=='13'||h['sec-websocket-protocol']!==PROTOCOL||h.upgrade?.toLowerCase()!=='websocket'||!h.connection?.toLowerCase().split(/\s*,\s*/).includes('upgrade')||!h['sec-websocket-key']||(seen.has('sec-websocket-extensions')&&h['sec-websocket-extensions']!==STANDARD_OFFER)||seen.has('cookie')||seen.has('authorization')||seen.has('proxy-authorization')){record('admission_header_'+firstFailedAdmissionHeader(req,h,seen));reject(t,'admission_headers');return;}
    const match=/^\/enet\?cap=([A-Za-z0-9_-]{21}[AQgw])$/.exec(req.url);
    if(!match){reject(t,'admission_route');return;}
    const token=match[1],decoded=Buffer.from(token,'base64url');
    if(decoded.length!==16||decoded.toString('base64url')!==token){reject(t,'admission_capability');return;}
    const digest=crypto.createHash('sha256').update(token,'utf8').digest();
    // Evaluate both fixed-size comparisons, independent of which token matches.
    const matches=hashes.map(h=>crypto.timingSafeEqual(h,digest));const index=matches[0]?0:matches[1]?1:-1;
    if(index<0){reject(t,'admission_capability');return;}
    if(active()>=L.active){reject(t,'active_limit');return;}
    if(used[index]){reject(t,'capability_replay');return;}
    if(retired()+active()>=L.retired||udp.size>=L.udpTotal){reject(t,'retirement_capacity');return;}
    // Synchronous reservation and token consumption before any later I/O.
    used[index]=true;const at=now();
    const s={id:`s${++serial}`,generation:1,closed:false,reason:null,records:[],ws:null,udp:null,udpClosed:false,udpClosing:false,retired:false,tuple:null,connected:false,
      born:at,lastData:at,nextPing:at+L.pingMs,pingAt:null,pings:[],control:new Bucket(L.controlRate,L.controlBurst,at),
      toUDP:new Flow(at,true),toWS:new Flow(at),controlPending:new Map(),controlBytes:0,controlSerial:0,controlOldest:Infinity,
      counters:{to_udp_datagrams:0,to_udp_bytes:0,to_ws_datagrams:0,to_ws_bytes:0}};
    sessions.push(s);t.session=s;counters.admitted++;counters.peak_active=Math.max(counters.peak_active,active());record('admitted',s);
    t.replayedBytes=head.length;
    try{wss.handleUpgrade(req,socket,head,ws=>{cancel(t.deadline);connectSession(s,ws);});}catch{finish(s,'upgrade_error',1011);socket.destroy();}
  });
  wss.on('error',()=>{failure='ws_server_error';void close('ws_server_error');});
  server.on('error',()=>{failure='http_server_error';if(cleanup.state==='running')void close('http_server_error');});
  function snapshot(){
    const value={schema_version:1,run_id,address:{address:HOST,port:PORT,family:'IPv4'},counters:{...counters},
      active:active(),pending_tcp:[...tcp.values()].filter(t=>!t.session).length,retired:retired(),udp_total:udp.size,
      sessions:sessions.map(s=>({session_id:s.id,generation:s.generation,state:s.closed?(s.retired&&!s.udpClosed?'retired':'closed'):'active',reason:s.reason,upstream_connected:s.connected,udp_tuple:s.tuple?{...s.tuple}:null,
        close_code:s.closeCode??null,parser_error:s.parserError??null,counters:{...s.counters},to_udp:s.toUDP.snapshot(),to_ws:s.toWS.snapshot(),control_pending_bytes:s.controlBytes,records:s.records.map(r=>({...r}))})),
      diagnostics:diagnostics.map(r=>({...r})),failure,cleanup:{...cleanup,timers:timers.size,tcp_handles:tcp.size,udp_handles:udp.size}};
    // Explicit bound on public diagnostic serialization; no payloads or credentials.
    if(Buffer.byteLength(JSON.stringify(value))>L.outputBytes)throw Error('snapshot_output_limit');
    return value;
  }
  function close(reason='owner_close'){
    if(closing)return closing;
    closed=true;cleanup.state='closing';
    cleanup.reason=['run_timeout','diagnostic_overflow','ws_server_error','http_server_error','listen_error'].includes(reason)?reason:'owner_close';
    closing=(async()=>{
    // Publish the idempotent close promise before callbacks/overflow can reenter.
    await Promise.resolve();
    // Reason is caller-controlled: retain a fixed diagnostic, never reflect it.
    if(diagnostics.length<L.diagnostics)record('component_close');
    for(const t of [...timers])cancel(t);
    for(const s of sessions){finish(s,'component_close',1001);closeUDP(s);}
      const httpDone=new Promise(resolve=>{server.close(()=>{cleanup.http_closed=true;resolve();});});
      const wsDone=new Promise(resolve=>wss.close(()=>{cleanup.ws_closed=true;resolve();}));
      for(const t of tcp.values())if(!t.session)t.socket.destroy();
      const force=timer(()=>{for(const s of sessions)if(s.ws&&s.ws.readyState!==WS.CLOSED)s.ws.terminate();for(const t of tcp.values())t.socket.destroy();},1000);
      await Promise.all([httpDone,wsDone,...sessions.filter(s=>s.udpDone).map(s=>s.udpDone)]);
      await Promise.all([...tcp.values()].map(t=>new Promise(resolve=>{t.socket.once('close',resolve);t.socket.destroy();})));
      cancel(force);for(const t of [...timers])cancel(t);
      cleanup.state='closed';
    })();
    return closing;
  }
  try{await new Promise((resolve,reject)=>{server.once('error',reject);server.listen(PORT,HOST,resolve);});}
  catch{await close('listen_error');throw Error('gateway_listen_failed');}
  cleanup.state='running';runTimer=timer(()=>void close('run_timeout'),L.runMs);
  return {address:{address:HOST,port:PORT,family:'IPv4'},snapshot,close};
}
module.exports={startGateway};
