// T067 PREPARED SOURCE ONLY. Never invoked under preparation.
// Reads published diagnostics; only game input is ordinary canvas/mouse/keyboard.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const planPath=process.argv[2];assert(planPath,'validated future MAIN plan required before package import');
const p=JSON.parse(fs.readFileSync(planPath,'utf8'));
const impaired=p.case_kind==='impaired40_drop50';
assert((p.case_kind===undefined||impaired)&&p.ticket===(impaired?'T082':'T067')&&p.status==='RELEASED'&&p.authority.owner==='MAIN'&&p.execution_release===(impaired?'EXPLICIT_IMPAIRED_TWO_CLIENT_NATIVE_GAME_EXECUTION':'EXPLICIT_TWO_CLIENT_NATIVE_GAME_EXECUTION')&&p.scope.role===(impaired?'full-cpp-two-browser-native-game-impaired':'full-cpp-two-browser-native-game'));
assert(path.resolve(planPath)===path.join(p.result,'validated-plan.json'));
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
assert(p.pins_path&&p.pins_sha&&path.dirname(p.pins_path)===path.join(p.root,'notes/decisions')&&hash(fs.readFileSync(p.pins_path))===p.pins_sha,'original authority receipt');
for(const [name,row]of Object.entries(p.files))assert(hash(fs.readFileSync(path.isAbsolute(name)?name:path.join(p.root,name)))===row.sha256,'changed approved input');
// All side-effect-capable component imports occur after the authority/file gate.
const http=require('node:http');let shaper=null;
if(impaired){
 const fixed=require(path.join(p.root,'web/transport/tests/impaired/T082/shaper.cjs'));
 assert.deepEqual(p.impairment,fixed.PRESET);assert(p.accepted_dependencies.T082==='ACCEPTED'&&p.accepted_dependencies.T079==='ACCEPTED');
 shaper=fixed.install({dgram:require('node:dgram'),now:()=>performance.now(),setTimer:setTimeout,clearTimer:clearTimeout});
}
const {startGateway}=require(path.join(p.root,'web/transport/gateway.cjs'));
const pw=require(p.tools.playwright);
const caps=[crypto.randomBytes(16).toString('base64url'),crypto.randomBytes(16).toString('base64url')];
function safe(value){if(typeof value==='string'){for(const c of caps)value=value.replaceAll(c,'[redacted]');return value.replace(/([?&](?:cap|token|capability)=)[^\s&"<>]+/gi,'$1[redacted]').slice(0,2048);}if(Array.isArray(value))return value.map(safe);if(value&&typeof value==='object')return Object.fromEntries(Object.entries(value).map(([k,v])=>[k,/^(token|capability|private_key|password)$/i.test(k)?'[redacted]':safe(v)]));return value;}
const report={kind:'ACTUAL full C++ two-client published-state evidence',status:'FAIL',errors:[],compatibility:[],trace:[],observations:{},sample_faults:{},active:[],moves:[],cleanup:{},unproven:['native internal clientsequence/cache','authoritative movement/damage','audibility','correct pixels/animation','reconnect/impairment','P0/P1/MVP']};
if(impaired)report.kind='ACTUAL_IMPAIRED_TWO_GAME_CLIENT';
function trace(event){assert(report.trace.length<512,'512 trace overflow');report.trace.push(safe(event));}
function fail(message){throw Error(message);}
const clients=[],tcp=new Set();let gateway,server,timer;const start=performance.now();
function bounded(promise,ms,why){let t;return Promise.race([promise,new Promise((_,reject)=>t=setTimeout(()=>reject(Error(why)),ms))]).finally(()=>clearTimeout(t));}
function errors(){if(report.errors.length)fail(report.errors[0]);}
// Source-derived identity: main.cpp first frame0 -> engine frame_count1,
// no draw yet; client.cpp has exactly one published frame/WS advance.
const FIRST_FRAME_IDENTITY = {"timing":{"frame_id":0,"prediction_elapsed_ms":0,"embedded_server_path_compiled":false},"diagnostics":{"frame_count":1,"rendered_frame_count":0,"phase":"loading","map_name":"dev_outbreak_browser"},"counters":{"begin_calls":1,"repeated_begin":0,"frame_calls":1,"frame_advances":1,"ws_frames":1,"milestones":0,"map_receipts":0,"spawn_acknowledgments":0,"teardowns":0}};
function classifyTiming(s){
 const n=s.network,d=s.diagnostics,t=s.timing,b=s.browser;
 if((n&&(n.error!==0||['BN_FAILED','BN_CLOSING'].includes(n.state)))||(d&&(['error','stopped'].includes(d.phase)||!Array.isArray(d.runtime_errors)||d.runtime_errors.length)))fail('published lifecycle/global error');
 if(b.visibility!=='visible')fail('actual visibility failure');
 if(!t)return 'WAITING';
 if(t.schema_version!==1||!Number.isInteger(t.frame_id)||t.frame_id<0||!Number.isFinite(t.raw_elapsed_ms)||t.raw_elapsed_ms<0||!Number.isFinite(t.prediction_elapsed_ms)||t.prediction_elapsed_ms<0||t.prediction_elapsed_ms>50||t.embedded_server_path_compiled!==false||!b.timing_frozen)fail('invalid published timing');
 if(t.frame_id>0){if(t.raw_elapsed_ms>1000)fail('later main-frame interval exceeds1000ms; backend cause unproven');return 'LATER_FRAME';}
 if(!n||!d||n.schema_version!==1||n.profile!=='network-client'||d.schema_version!==1||d.profile!=='network-client'||!b.network_frozen)fail('ambiguous frame0 identity');
 const counters=n.counters;
 if(!counters||Object.keys(counters).sort().join()!==[...p.diagnostic_contract.counter_keys].sort().join()||!Object.values(counters).every(v=>Number.isInteger(v)&&v>=0))fail('ambiguous frame0 counters');
 for(const [section,actual]of [['timing',t],['diagnostics',d],['counters',counters]])if(!Object.entries(FIRST_FRAME_IDENTITY[section]).every(([k,v])=>actual[k]===v))fail('ambiguous frame0 identity');
 const states=['BN_IDLE','BN_OPENING','BN_OPEN','BN_JOINING','BN_ACTIVE','BN_CLOSING','BN_FAILED'];
 if(!['BN_OPENING','BN_JOINING'].includes(n.state)||t.lifecycle_state!==states.indexOf(n.state))fail('ambiguous frame0 lifecycle');
 if(n.map_name!==''||n.map_revision!==0||n.own?.cn!==-1||n.own?.life!==-1)fail('ambiguous frame0 lifecycle');
 if(counters.owned_local_attempts||counters.join_timeouts||counters.send_rejected)fail('owned client error/local attempt');
 if(!Array.isArray(n.events)||n.events.length!==(n.state==='BN_OPENING'?1:2)||!n.events.every(e=>e&&e.kind===0&&e.milestone===0&&e.cn===-1&&e.life===-1&&e.error===0&&Number.isFinite(e.at_ms)&&e.at_ms>=0)||!n.events.every((e,i)=>i===0||e.at_ms>=n.events[i-1].at_ms))fail('ambiguous frame0 events');
 return 'STARTUP_FRAME0'; // Observation only; never readiness or join success.
}
function retain(c,slot,s){
 try{
  assert(['A','B'].includes(c.name)&&Object.keys(report.observations).length<=2,'unbounded client evidence');
  assert(!s.network||(Array.isArray(s.network.events)&&s.network.events.length<=512&&Array.isArray(s.network.remotes)&&s.network.remotes.length<=256),'unbounded network sample');
  assert(!s.diagnostics||(Array.isArray(s.diagnostics.runtime_errors)&&s.diagnostics.runtime_errors.length<=512),'unbounded runtime errors');
  assert(!s.model||(Array.isArray(s.model.preloads)&&s.model.preloads.length<=3),'unbounded model sample');
  assert(Buffer.byteLength(JSON.stringify(s))<=1024*1024,'full sample byte bound');
  const candidate={...report.observations,[c.name]:{...report.observations[c.name],[slot]:safe(s)}};
  assert(Buffer.byteLength(JSON.stringify(candidate))<=1024*1024,'failure evidence byte bound');report.observations=candidate;
 }catch(e){report.sample_faults[c.name]=safe(e.message);throw e;}
}
const warnings=new Set([
 'WARNING: using emscripten GL emulation. This is a collection of limited workarounds, do not expect it to work.',
 'WARNING: using emscripten GL immediate mode emulation. This is very limited in what it supports'
]);
function eligible(s,active=false){
 const n=s.network,d=s.diagnostics,t=s.timing,b=s.browser;
 if(classifyTiming(s)!=='LATER_FRAME')return false;
 if(!n||!d||!t)return false;
 if(n.error||n.state==='BN_FAILED'||n.state==='BN_CLOSING'||d.phase==='error'||(d.runtime_errors||[]).length)fail('published lifecycle/global error');
 if(n.schema_version!==1||n.profile!=='network-client'||d.schema_version!==1||d.profile!=='network-client'||t.schema_version!==1)fail('wrong published schema/profile');
 const keys=p.diagnostic_contract.counter_keys;
 if(!n.counters||Object.keys(n.counters).sort().join()!==[...keys].sort().join())fail('unknown public counter schema');
 if(n.counters.owned_local_attempts||n.counters.join_timeouts||n.counters.send_rejected)fail('owned client error/local attempt');
 if(!Array.isArray(n.events)||n.events.length>512)fail('published event overflow');
 if(!b.network_frozen||!b.timing_frozen)fail('mutable public snapshot');
 const milestones=n.events.filter(e=>e.kind===1),opened=n.events.filter(e=>e.kind===0);
 if(opened.length>=2){
  const spawn=milestones.find(e=>e.milestone===4);
  if(spawn&&spawn.at_ms-opened[1].at_ms>=15000)fail('actual join exceeded15s');
  if(!spawn&&b.now_ms-opened[1].at_ms>17000)fail('no join by15s plus bounded observation settle; no late spawn accepted');
 }
 // Transitional getters may lag one another. Do not require equal frame IDs.
 if(n.map_name!=='dev_outbreak_browser'||n.map_revision!==2||n.own.cn<0||d.map_name!=='dev_outbreak_browser'||d.phase!=='running'||d.rendered_frame_count<1||!n.counters.map_receipts)return false;
 if(milestones.slice(0,3).map(e=>e.milestone).join()!=='1,2,3'||!milestones.slice(0,3).every(e=>e.cn===n.own.cn))return false;
 if(b.visibility!=='visible'||t.raw_elapsed_ms>1000||t.embedded_server_path_compiled!==false)return false;
 if(active)return n.state==='BN_ACTIVE'&&n.own.life>=0&&n.own.state===0&&milestones[3]?.milestone===4&&n.counters.spawn_acknowledgments>0&&t.lifecycle_state===4;
 return n.state==='BN_JOINING'||n.state==='BN_ACTIVE';
}
async function read(c){
 const sample=await c.page.evaluate(()=>{
  const network=typeof window.outbreakNetworkSnapshot==='function'?window.outbreakNetworkSnapshot():null;
  const timing=window.OUTBREAK_NETWORK_TIMING||null,canvas=document.querySelector('#canvas');
  return {network,diagnostics:window.OUTBREAK_DIAGNOSTICS||null,timing,model:window.OUTBREAK_MODEL_DIAGNOSTICS||null,audio:window.OUTBREAK_AUDIO_DIAGNOSTICS||null,
   browser:{now_ms:performance.now(),focused:document.hasFocus(),visibility:document.visibilityState,network_frozen:!!network&&Object.isFrozen(network),timing_frozen:!!timing&&Object.isFrozen(timing),canvas_width:canvas?.width||0,canvas_height:canvas?.height||0}};
 });
 retain(c,'last',sample); // Before any error/eligibility decision: keep full failure state.
 if(sample.network?.state==='BN_ACTIVE'&&!report.observations[c.name].first_active)retain(c,'first_active',sample);
 c.polls++;const label=[sample.network?.state,sample.network?.counters?.milestones,sample.browser.focused,sample.browser.visibility].join(':');
 if(label!==c.lastLabel){trace({client:c.name,at_ms:performance.now()-start,stage:label,frame_id:sample.timing?.frame_id,raw_elapsed:sample.timing?.raw_elapsed_ms});c.lastLabel=label;}
 const timing=classifyTiming(sample);
 if(timing==='STARTUP_FRAME0'&&!report.observations[c.name].startup){retain(c,'startup',sample);trace({client:c.name,event:'initial startup elapsed; not an inter-frame gap/readiness',frame_id:sample.timing.frame_id,raw_elapsed:sample.timing.raw_elapsed_ms});}
 errors();
 return sample;
}
async function join(c){
 const until=performance.now()+45000;let lastRequest=-Infinity;
 while(performance.now()<until){
  const s=await read(c);if(eligible(s,true)){trace({client:c.name,event:'ACTIVE',spawn_requests:s.network.counters.spawn_requests,path:s.network.counters.spawn_requests?'published ordinary request present':'native spawn without published request; internal branch unobserved'});return s;}
  if(eligible(s,false)){
   const first=s.network.events.find(e=>e.kind===1&&e.milestone===1);
   // D057: only still-JOINING clients get an ordinary request, after native age.
   if(s.network.state==='BN_JOINING'&&first&&s.browser.now_ms-first.at_ms>=2000&&performance.now()-lastRequest>=1100){
    const fresh=await read(c);
    if(fresh.network?.state==='BN_JOINING'&&eligible(fresh,false)&&fresh.browser.focused){await c.page.locator('#canvas').click();lastRequest=performance.now();trace({client:c.name,event:'ordinary eligible capture or click/release'});}
   }
  }
  await c.page.waitForTimeout(50);
 }
 fail('join/scene observer deadline');
}
async function settled(c,until){
 let previous=null;
 while(performance.now()<until){const s=await read(c);if(eligible(s,true)&&previous&&Math.hypot(s.network.own.position[0]-previous.network.own.position[0],s.network.own.position[1]-previous.network.own.position[1])<=.05)return s;previous=s;await c.page.waitForTimeout(50);}fail('settled own state deadline');
}
async function movement(a,b){
 await a.page.bringToFront();
 // Entry capture is an ordinary gesture, never a scripted spawn/action function.
 if(!(await read(a)).diagnostics?.input_locked)await a.page.locator('#canvas').click();
 const a_before=await read(a),b_before=await read(b);assert(eligible(a_before,true)&&eligible(b_before,true));
 assert(a_before.diagnostics.input_locked&&a_before.browser.focused,'ordinary input not acquired/focused');
 await a.page.keyboard.down('w');a.held=true;
 try{await a.page.waitForTimeout(250);}finally{await a.page.keyboard.up('w');a.held=false;}
 const released=performance.now(),until=released+2000,a_settled=await settled(a,until);const cn=a_settled.network.own.cn,life=a_settled.network.own.life;
 assert(Math.hypot(a_settled.network.own.position[0]-a_before.network.own.position[0],a_settled.network.own.position[1]-a_before.network.own.position[1])>=2,'W250ms did not move >=2; no alternate-axis/teleport retry');
 const old=b_before.network.remotes.find(r=>r.cn===cn&&r.life===life);assert(old,'missing initial parsed remote');
 while(performance.now()<until){const b_after=await read(b),r=b_after.network?.remotes.find(r=>r.cn===cn&&r.life===life);
  if(eligible(b_after,true)&&r&&r.parse_count>old.parse_count&&r.last_parse_ms>old.last_parse_ms&&Math.hypot(r.position[0]-a_settled.network.own.position[0],r.position[1]-a_settled.network.own.position[1])<=1){report.moves.push({mover:a.name,receiver:b.name,a_before,a_settled,b_before,b_after,elapsed_ms:performance.now()-released});return;}
  await b.page.waitForTimeout(50);
 }fail('no new matching parsed cross-client receipt within2s');
}
async function cleanup(){
 const begin=performance.now();let keys=true,contexts=true,browsers=true,profiles=true;
 for(const c of clients){
  if(c.page){try{await c.page.keyboard.up('w');await c.page.mouse.up();await c.page.keyboard.press('Escape');}catch(_){keys=false;}}
  if(c.context)try{await bounded(c.context.close(),1500,'owned context close');}catch(_){contexts=false;}
  if(c.browser)try{await bounded(c.browser.close(),1500,'owned browser close');}catch(_){browsers=false;}
  if(c.server){const child=c.server.process();try{await bounded(c.server.close(),2000,'owned browser server close');}catch(_){await c.server.kill();browsers=false;}
   browsers=browsers&&(child.exitCode!==null||child.signalCode!==null);const profile=child.spawnargs.find(x=>x.startsWith('--user-data-dir='))?.slice(16);profiles=profiles&&!!profile&&!fs.existsSync(profile);}
 }
 let gatewayClosed=false,gatewayMs=null;
 try{if(gateway){const at=performance.now();await bounded(gateway.close('owner_close'),2000,'gateway close');gatewayMs=performance.now()-at;report.gateway_final=gateway.snapshot();const g=report.gateway_final;gatewayClosed=g.cleanup.state==='closed'&&g.cleanup.timers===0&&g.cleanup.tcp_handles===0&&g.cleanup.udp_handles===0;}}
 finally{if(shaper){report.shaper=shaper.close();if(report.shaper.faults.length||report.shaper.directions.up.dropped<1||report.shaper.directions.down.dropped<1)report.errors.push('shaper fault or no actual profile loss in each direction');}}
 for(const s of tcp)s.destroy();if(server?.listening)await new Promise(resolve=>server.close(resolve));
 report.cleanup={keys_released:keys,contexts_closed:contexts,browsers_stopped:browsers,profiles_removed:profiles,gateway_closed:gatewayClosed,gateway_close_ms:gatewayMs,static_closed:!server?.listening&&tcp.size===0,elapsed_ms:performance.now()-begin,peer_shutdown:'owned context loss, not claimed normal game disconnect'};
}
(async()=>{
 timer=setTimeout(()=>{report.errors.push('180s owned baseline deadline');cleanup().finally(()=>{console.log(JSON.stringify(safe(report)));process.exit(1);});},180000);
 try{
  const runId=crypto.randomBytes(16).toString('hex');
  gateway=await startGateway({schema_version:1,run_id:runId,capability_sha256:caps.map(hash)});
  const routes=new Map([['/',p.bundle.runtime.shell],...Object.values(p.bundle.runtime).concat(p.bundle.notices).map(n=>['/'+n,n])]);
  server=http.createServer((req,res)=>{
   if(req.method==='GET'&&req.url==='/favicon.ico'){res.writeHead(204);return res.end();}
   if(req.method!=='GET'||!routes.has(req.url)){res.writeHead(404);return res.end();}
   const relative=routes.get(req.url),name=path.join(p.bundle.root,relative),full=path.join(p.root,name);assert(hash(fs.readFileSync(full))===p.files[name].sha256,'served file changed');
   res.setHeader('Content-Security-Policy',"default-src 'self'; script-src 'self' 'unsafe-inline' 'wasm-unsafe-eval'; connect-src 'self' ws://127.0.0.1:29865/enet; img-src 'self' data:; style-src 'self' 'unsafe-inline'");
   res.setHeader('Content-Type',relative.endsWith('.wasm')?'application/wasm':relative.endsWith('.js')?'text/javascript':relative.endsWith('.html')?'text/html':'application/octet-stream');res.end(fs.readFileSync(full));
  });server.on('connection',s=>{tcp.add(s);s.on('close',()=>tcp.delete(s));});await new Promise((resolve,reject)=>{server.once('error',reject);server.listen(29866,'127.0.0.1',resolve);});
  report.browser_pids=[];report.control_ports=[];
  for(let i=0;i<2;i++){
   const c={name:i?'B':'A',seenWarnings:new Set(),polls:0,held:false};clients.push(c);
   report.observations[c.name]={last:null,first_active:null,startup:null};
   const options={executablePath:p.tools.browser,headless:true,chromiumSandbox:true,host:'127.0.0.1',port:0,timeout:5000,ignoreDefaultArgs:['--disable-popup-blocking','--disable-ipc-flooding-protection','--unsafely-disable-devtools-self-xss-warnings','--enable-unsafe-swiftshader','--mute-audio','--allow-pre-commit-input','--disable-background-timer-throttling','--disable-renderer-backgrounding','--disable-backgrounding-occluded-windows']};
   c.temp=path.join(p.result,'browser-temp-'+c.name);fs.mkdirSync(c.temp);
   process.env.TMPDIR=c.temp; // Inspected Playwright profile mkdtemp uses host os.tmpdir().
   options.env={...process.env,TMPDIR:c.temp};
   // Parent independently scans the unique owned profile prefix during startup.
   c.server=await pw.chromium.launchServer(options);report.browser_pids.push(c.server.process().pid);report.control_ports.push(Number(new URL(c.server.wsEndpoint()).port));trace({client:c.name,argv:c.server.process().spawnargs});
   const ownership={schema_version:1,browser_pids:report.browser_pids,control_ports:report.control_ports,profiles:clients.filter(x=>x.server).map(x=>x.server.process().spawnargs.find(a=>a.startsWith('--user-data-dir='))?.slice(16))};
   fs.writeFileSync(path.join(p.result,'browser-ownership.tmp'),JSON.stringify(ownership));fs.renameSync(path.join(p.result,'browser-ownership.tmp'),path.join(p.result,'browser-ownership.json'));
   c.browser=await pw.chromium.connect(c.server.wsEndpoint(),{timeout:2000});c.context=await c.browser.newContext();
   await c.context.route('**/*',r=>new URL(r.request().url()).origin==='http://127.0.0.1:29866'?r.continue():r.abort());
   await c.context.addInitScript(({capability,runId})=>Object.defineProperty(window,'OUTBREAK_NETWORK_BOOT',{value:Object.freeze({schema_version:1,runId,endpoint:'ws://127.0.0.1:29865/enet',capability}),writable:false,configurable:false}),{capability:caps[i],runId});
   c.page=await c.context.newPage();c.page.on('pageerror',e=>{if(report.errors.length<512)report.errors.push(safe(e.message));else fail('error overflow');});
   c.page.on('requestfailed',r=>{assert(report.errors.length<512,'error overflow');report.errors.push(safe('network failure: '+r.failure()?.errorText));});
   c.page.on('console',m=>{if(!['error','warning'].includes(m.type()))return;const raw=m.text();if(warnings.has(raw)&&!c.seenWarnings.has(raw)){c.seenWarnings.add(raw);report.compatibility.push({client:c.name,text:raw});}else{assert(report.errors.length<512,'error overflow');report.errors.push(safe(raw));}});
   await c.page.goto('http://127.0.0.1:29866/',{timeout:30000});await c.page.bringToFront();await join(c);
   const current=gateway.snapshot();assert(current.counters.admitted===i+1&&current.sessions.length===i+1&&current.failure===null);c.gateway_session=current.sessions[i].session_id;trace({client:c.name,gateway_session:c.gateway_session,udp_tuple:current.sessions[i].udp_tuple});
  }
  const readyUntil=performance.now()+2000;
  while(true){const a=await read(clients[0]),b=await read(clients[1]);
   if(eligible(a,true)&&eligible(b,true)&&a.network.own.cn!==b.network.own.cn&&a.network.remotes.some(r=>r.cn===b.network.own.cn&&r.life===b.network.own.life)&&b.network.remotes.some(r=>r.cn===a.network.own.cn&&r.life===a.network.own.life)){report.active=[a,b];break;}
   assert(performance.now()<readyUntil,'no distinct parsed pair');await clients[0].page.waitForTimeout(50);
  }
  const g=gateway.snapshot();assert(g.sessions[0].udp_tuple.port!==g.sessions[1].udp_tuple.port&&g.counters.udp_allocated===2);report.gateway_receipt=g;
  await movement(clients[0],clients[1]);await movement(clients[1],clients[0]);report.evidence_complete=true;
 }catch(e){report.errors.push(safe(e.message));}
 finally{try{await cleanup();}catch(e){report.errors.push(safe(e.message));}clearTimeout(timer);report.elapsed_ms=performance.now()-start;report.status=report.evidence_complete&&!report.errors.length?'OBSERVATIONS_COMPLETE':'FAIL';const result=JSON.stringify(safe(report));assert(Buffer.byteLength(result)<=8*1024*1024,'8MiB output overflow');assert(!caps.some(c=>result.includes(c)),'capability disclosure');console.log(result);process.exitCode=report.status==='OBSERVATIONS_COMPLETE'?0:1;}
})();
