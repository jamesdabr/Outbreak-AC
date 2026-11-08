'use strict';
// FIXTURE_ONLY. All document/clock/rAF/heap/Page/input behavior is fake. actual_browser:false.
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),crypto=require('node:crypto');
const root=__dirname+'/../../../..',out=__dirname+'/prep-1';
assert(!fs.existsSync(out),'Once-only preparation receipt already exists');
fs.mkdirSync(out);
const source=fs.readFileSync(root+'/source/src/main.cpp','utf8');
const hash=s=>crypto.createHash('sha256').update(s).digest('hex');
assert.equal(hash(source),'5f51c53b5a6f2be1180252c7aee972ab754bf0abc91d8a3d0f276153a38834f1');
const extract=(text,name)=>{const m=[...text.matchAll(/EM_JS\(void, (\w+), \((.*?)\), \{(.*?)\n\}\);/gs)].find(x=>x[1]===name);assert(m,name);return {args:m[2].split(',').map(x=>x.trim().split(/\s+/).at(-1).replace(/^\*/,'')),body:m[3]};};
const definitions={foundation:extract(source,'browserfoundationmetrics'),diagnostics:extract(source,'browserpublishjs'),timing:extract(source,'browsernetworktiming'),model:extract(source,'browsermodelpublish'),
    network:extract(fs.readFileSync(root+'/source/src/client.cpp','utf8'),'bn_publish_json'),audio:extract(fs.readFileSync(root+'/source/src/audiomanager.cpp','utf8'),'browserproofsnapshot')};
const moduleSource=fs.readFileSync(__dirname+'/measure.cjs','utf8');
assert(!/require\s*\(|\bimport\b|\bfetch\s*\(|\bModule\b|dispatchEvent|addInitScript|\.goto\(/.test(moduleSource),'forbidden dependency/action surface');
const sandbox={module:{exports:{}}};vm.runInNewContext(moduleSource,sandbox,{filename:'measure.cjs'});
assert.deepEqual(Object.keys(sandbox.module.exports),['measureFoundation']);
const measureFoundation=sandbox.module.exports.measureFoundation;
const plain=v=>JSON.parse(JSON.stringify(v));

class FakePage {
    constructor(mode='positive') {
        this.mode=mode;this.now=1000;this.frame=100;this.rendered=96;this.yaw=359;this.pitch=0;this.position=[10,20,30];
        this.held=new Set();this.button=false;this.focused=true;this.visibility='visible';this.locked=false;this.captureCount=0;
        this.actions=[];this.probes=[];this.rafCount=0;this.timerCount=0;this.callbacks=new Map();this.timers=new Map();this.closed=false;
        this.canvas={width:1280,height:720,getBoundingClientRect:()=>({x:0,y:0,width:1280,height:720})};
        const self=this;
        this.world={window:{addEventListener:()=>{}},document:{hasFocus:()=>self.focused,get visibilityState(){return self.visibility;},get pointerLockElement(){return self.locked?self.canvas:null;},querySelector:selector=>{assert.equal(selector,'#canvas');return self.canvas;}},
            location:{origin:'http://127.0.0.1:29866',href:'http://127.0.0.1:29866/index.html'},innerWidth:1280,innerHeight:720,devicePixelRatio:1,URL,
            HEAPU8:{buffer:{byteLength:67108864}},UTF8ToString:v=>v,
            AL:{contexts:{1:{audioCtx:{state:'running'}}}},
            performance:{now:()=>self.now,memory:{usedJSHeapSize:12345678},getEntriesByType:type=>[{name:'http://127.0.0.1:29866/'+(type==='navigation'?'index.html':'index.wasm'),startTime:0,duration:100,decodedBodySize:1000,encodedBodySize:800,transferSize:900}]},
            requestAnimationFrame:cb=>{const id=++self.rafCount;self.callbacks.set(id,cb);queueMicrotask(()=>{if(!self.callbacks.has(id))return;self.callbacks.delete(id);self.step(self.mode==='overflow'?.1:1000/60,true);cb(self.now);});return id;},
            cancelAnimationFrame:id=>self.callbacks.delete(id),
            setTimeout:(cb,ms)=>{const id=++self.timerCount;self.timers.set(id,{at:self.now+ms,cb});return id;},clearTimeout:id=>self.timers.delete(id)};
        this.contextVM=vm.createContext(this.world);
        this.publishers=Object.fromEntries(Object.entries(definitions).map(([name,d])=>[name,vm.runInContext('(function('+d.args.join(',')+'){'+d.body+'\n})',this.contextVM)]));
        this.keyboard={down:async k=>{this.actions.push('down:'+k);this.held.add(k);},up:async k=>{this.actions.push('up:'+k);if(this.mode==='cleanup-fail')throw Error('fixture key release refused');this.held.delete(k);},press:async k=>{assert.equal(k,'Escape');this.actions.push('Escape');this.locked=false;if(this.mode!=='release-fail'){this.held.clear();this.button=false;}}};
        this.mouse={move:async(x,y)=>{this.actions.push(['mouse',x,y]);if(x===672&&this.mode!=='no-mouse'){this.yaw=(this.yaw+3)%360;this.pitch-=2;}},down:async()=>{this.actions.push('LMB-down');this.button=true;},up:async()=>{this.actions.push('LMB-up');this.button=false;}};
        if(mode==='viewport')this.world.innerWidth=800;
        if(mode==='origin')this.world.location.origin='https://wrong.invalid';
        if(mode==='transfer-unavailable')delete this.world.performance.getEntriesByType;
        if(mode==='js-heap-unavailable')delete this.world.performance.memory;
        if(mode==='transfer-overflow')this.world.performance.getEntriesByType=()=>Array.from({length:513},()=>({}));
    }
    step(ms,steady=false){
        this.now+=ms;if(this.mode!=='stale'){this.frame+=steady?(this.mode==='duplicate'&&this.rafCount%100===0?0:1):Math.max(1,Math.round(ms/(1000/60)));this.rendered=this.frame-4;}
        if(steady&&this.mode==='gap'&&this.rafCount===100)this.frame+=2;
        if(steady&&this.mode==='regression'&&this.rafCount===100)this.frame-=2;
        if(this.held.has('w')&&this.mode!=='no-movement')this.position[1]+=ms*.012;
        if(steady&&this.mode==='wasm')this.world.HEAPU8.buffer.byteLength=600*1024*1024;
        for(const [id,t]of this.timers)if(this.now>=t.at){this.timers.delete(id);t.cb();}
        this.publish(steady);
    }
    publish(steady=false){
        const held=this.held.has('w')?1:0,jump=this.held.has('Space');
        const terminal=this.visibility==='hidden'&&this.mode!=='hidden-unobserved';
        const error=terminal?(this.mode==='unrelated-terminal'?7:15):0;
        const n={schema_version:1,profile:'network-client',state:terminal?'BN_FAILED':'BN_ACTIVE',error,map_name:'dev_outbreak_browser',map_revision:2,
            own:{cn:1,life:2,state:terminal?5:0,position:this.position.slice()},remotes:[],
            counters:{spawn_acknowledgments:1},coverage:'FIXTURE_ONLY',events:[1,2,3,4].map(milestone=>({kind:1,milestone,cn:1,life:2,error:0,at_ms:1}))};
        if(terminal)n.events.push({kind:2,milestone:0,cn:-1,life:-1,error,at_ms:this.now});
        if(this.mode==='event-overflow')n.events=Array(513).fill({kind:0});
        this.publishers.network(JSON.stringify(n));
        this.publishers.diagnostics('running',this.frame,this.rendered,'dev_outbreak_browser',...this.position,+this.locked,0);
        this.publishers.timing(this.mode==='p95-tail'&&steady&&this.rafCount%10===0?40:1000/60,1000/60,this.frame-1,terminal?6:4);
        this.publishers.model(1,1,1);this.publishers.audio('playing',this.captureCount,1,1,4114,0,1);
        this.publishers.foundation(this.frame,this.rendered,1,this.yaw,this.pitch,held,0,+this.button,+jump,+jump,0,1280,720);
        const mutate=fn=>{const copy=plain(this.world.window.OUTBREAK_FOUNDATION_METRICS);fn(copy);Object.defineProperty(this.world.window,'OUTBREAK_FOUNDATION_METRICS',{value:Object.freeze(copy),writable:false,enumerable:true,configurable:true});};
        if(this.mode==='missing')delete this.world.window.OUTBREAK_FOUNDATION_METRICS;
        if(this.mode==='extra')mutate(v=>{v.extra=1;});
        if(this.mode==='wrong-type')mutate(v=>{v.frame_count='100';});
        if(this.mode==='invalid-angle')mutate(v=>{v.yaw_degrees=NaN;});
        if(this.mode==='absent-actor')this.publishers.foundation(this.frame,this.rendered,0,0,0,0,0,0,0,0,0,1280,720);
        if(this.mode==='missing-model')delete this.world.window.OUTBREAK_MODEL_DIAGNOSTICS;
        if(this.mode==='mutable')mutate(()=>{}); // nested objects deliberately not frozen
        if(this.mode==='wrong-map'){n.map_revision=1;this.publishers.network(JSON.stringify(n));}
        if(this.mode==='dead'){n.own.state=1;this.publishers.network(JSON.stringify(n));}
        if(this.mode==='global-error')this.publishers.diagnostics('running',this.frame,this.rendered,'dev_outbreak_browser',...this.position,+this.locked,'fixture global error');
        if(this.mode==='audio-error')this.publishers.audio('error',1,1,1,4114,'fixture audio error',1);
        if(steady&&this.mode==='steady-schema'&&this.rafCount===100)mutate(v=>{v.extra=1;});
    }
    async evaluate(fn,collect){
        if(!collect)this.step(1000/60);
        return plain(await vm.runInContext('('+fn.toString()+')('+JSON.stringify(collect)+')',this.contextVM));
    }
    async waitForTimeout(ms){assert([25,50,100,250,3000].includes(ms));this.step(ms);}
    async bringToFront(){this.actions.push('front');this.focused=true;}
    locator(selector){assert.equal(selector,'#canvas');return {click:async()=>{this.actions.push('canvas-click');this.captureCount++;if(this.mode==='recapture-fail'&&this.captureCount===2)return;this.locked=true;this.held.clear();this.button=false;}};}
    context(){return {newPage:async()=>{
        if(this.mode==='probe-is-original')return this;
        assert.equal(this.probes.length,0);const probe={closed:false,url:()=> 'about:blank',bringToFront:async()=>{this.actions.push('probe-front');this.focused=false;if(this.mode!=='hidden-unobserved')this.visibility='hidden';this.locked=false;this.held.clear();this.button=false;},close:async()=>{probe.closed=true;this.actions.push('probe-close');if(this.mode==='probe-close-fail')throw Error('fixture probe close refused');}};
        this.probes.push(probe);return probe;
    }};}
}

const results=[];
async function test(name,mode,check){
    const page=new FakePage(mode),report=await measureFoundation(page);
    try {check(report,page);assert.equal(page.closed,false);assert.equal(page.callbacks.size,0);assert.equal(page.timers.size,0);
        results.push({name,classification:'FIXTURE_ONLY',actual_browser:false,status:'PASS',component_error:report.error||null});
        if(mode==='positive')fs.writeFileSync(out+'/positive-fixture-report.json',JSON.stringify({classification:'FIXTURE_ONLY',actual_browser:false,report},null,2)+'\n');
    }catch(e){fs.writeFileSync(out+'/FAILED-'+mode+'.json',JSON.stringify({classification:'FIXTURE_ONLY',actual_browser:false,report,actions:page.actions,error:String(e.stack)},null,2));throw e;}
}
async function main(){
    await test('fixed sequence, real extracted publisher schemas, wrap and owned cleanup','positive',(r,p)=>{
        assert.equal(r.kind,'FOUNDATION_COMPONENT_OBSERVATIONS');assert.equal(r.error,undefined);assert.equal(r.input.mouse.status,'PASS');assert.equal(r.input.mouse.yaw_delta_wrapped,3);
        assert.equal(r.frames.status,'PASS');assert(r.frames.elapsed_ms>=60000);assert(r.frames.game_intervals>=3500);assert.equal(r.expected_terminal.classification,'EXPECTED_HIDDEN_BNE_VISIBILITY15');
        assert.equal(r.checks.cleanup,'PASS');assert.equal(p.probes.length,1);assert.equal(p.probes[0].closed,true);assert(r.pending_external.length>=5);assert.equal(r.status,undefined);
    });
    for(const mode of ['missing','extra','wrong-type','invalid-angle','absent-actor','missing-model','mutable','viewport','origin','wrong-map','dead','global-error','audio-error','event-overflow','transfer-overflow','stale','no-mouse','no-movement','release-fail','recapture-fail','gap','regression','wasm','p95-tail','overflow','steady-schema','unrelated-terminal','probe-is-original']){
        await test('negative '+mode,mode,r=>{assert.equal(r.checks.component_sequence,'FAIL');assert(r.error);assert(r.cleanup);if(!['missing','event-overflow','transfer-overflow'].includes(mode))assert(r.last);});
    }
    await test('transfer unavailable remains unavailable, not fabricated zero','transfer-unavailable',r=>{assert.equal(r.error,undefined);assert.equal(r.load.status,'NOT_OBSERVED');assert.equal(r.load.bytes,null);});
    await test('optional JS heap unavailable stays null, separate from actual Wasm','js-heap-unavailable',r=>{assert.equal(r.error,undefined);assert.equal(r.frames.js_heap.available,false);assert.equal(r.frames.js_heap.peak_bytes,null);assert.equal(r.frames.wasm_peak_bytes,67108864);});
    await test('duplicate rAF observations labeled separately from all actual game intervals','duplicate',r=>{assert.equal(r.error,undefined);assert.equal(r.frames.status,'PASS');assert(r.frames.duplicate_observer_samples>0);assert.equal(r.frames.game_intervals+r.frames.duplicate_observer_samples+1,r.frames.observer_samples);});
    await test('no actual hidden transition is NOT_OBSERVED','hidden-unobserved',r=>{assert.equal(r.error,undefined);assert.equal(r.expected_terminal.status,'NOT_OBSERVED');assert.equal(r.expected_terminal.hidden_observed,false);});
    await test('owned probe close failure retained','probe-close-fail',r=>{assert.equal(r.checks.cleanup,'FAIL');assert.equal(r.cleanup.probe_closed,false);assert(r.cleanup.errors.length);});
    await test('key cleanup failure retained','cleanup-fail',r=>{assert.equal(r.checks.cleanup,'FAIL');assert.equal(r.cleanup.keys_released,false);assert(r.cleanup.errors.length);});
    const optionsPage=new FakePage();const refused=await measureFoundation(optionsPage,{hook:()=>{throw Error('must not call');}});
    assert.equal(refused.checks.component_sequence,'FAIL');assert.match(refused.error,/no options\/hooks/);assert.equal(optionsPage.actions.length,0);
    results.push({name:'reject arbitrary options/hooks before actions',classification:'FIXTURE_ONLY',actual_browser:false,status:'PASS'});
    const receipt={classification:'FIXTURE_ONLY',actual_browser:false,fake_60s_is_not_benchmark:true,source_sha256:hash(source),component_sha256:hash(moduleSource),publisher_sources:Object.fromEntries(Object.entries(definitions).map(([k,v])=>[k,hash(v.body)])),tests:results};
    fs.writeFileSync(out+'/receipt.json',JSON.stringify(receipt,null,2)+'\n');
    console.log(JSON.stringify({classification:'FIXTURE_ONLY',actual_browser:false,passed:results.length}));
}
main().catch(e=>{fs.writeFileSync(out+'/failure.txt',String(e.stack)+'\n');console.error(e);process.exitCode=1;});
