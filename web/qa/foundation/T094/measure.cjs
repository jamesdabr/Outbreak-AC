'use strict';
// Preparation-only component. No imports, launches, private actions or configurable hooks.
const exact = (v, keys) => v && typeof v === 'object' && !Array.isArray(v) && Object.keys(v).sort().join() === keys.slice().sort().join();
const fail = (ok, why) => { if (!ok) throw Error(why); };
const integer = v => Number.isSafeInteger(v) && v >= 0;
const finite = Number.isFinite;
const neutral = s => Object.values(s.foundation.held).every(v => v === 0 || v === false);
const wrap = n => ((n + 180) % 360 + 360) % 360 - 180;
const bytes = v => { let n=0;for(const c of JSON.stringify(v)){const p=c.codePointAt(0);n+=p<128?1:p<2048?2:p<65536?3:4;}return n; };

// Serialized by Page.evaluate. Reads only source-defined public snapshots and DOM.
async function observe(collect) {
    function read() {
        const n = typeof window.outbreakNetworkSnapshot === 'function' ? window.outbreakNetworkSnapshot() : null;
        const f = window.OUTBREAK_FOUNDATION_METRICS, d = window.OUTBREAK_DIAGNOSTICS;
        const t = window.OUTBREAK_NETWORK_TIMING, a = window.OUTBREAK_AUDIO_DIAGNOSTICS, m = window.OUTBREAK_MODEL_DIAGNOSTICS;
        const deep = v => !v || typeof v !== 'object' || (Object.isFrozen(v) && Object.values(v).every(deep));
        const keys = (v, names) => v && Object.keys(v).sort().join() === names.split(' ').sort().join();
        if (collect && (!keys(f,'schema_version profile frame_count rendered_frame_count actor_present yaw_degrees pitch_degrees held wasm_heap_bytes logical_viewport document') ||
            !keys(f.held,'move strafe attack jump_next jump_held crouch_try') || !keys(f.logical_viewport,'width height') || !keys(f.document,'focused visibility pointer_is_canvas') ||
            f.schema_version !== 1 || f.profile !== 'network-client' || typeof f.actor_present !== 'boolean' ||
            ![f.frame_count,f.rendered_frame_count,f.wasm_heap_bytes].every(v=>Number.isSafeInteger(v)&&v>=0) ||
            !(f.actor_present ? Number.isFinite(f.yaw_degrees)&&Number.isFinite(f.pitch_degrees) : f.yaw_degrees===null&&f.pitch_degrees===null) ||
            !Number.isInteger(f.held.move) || !Number.isInteger(f.held.strafe) ||
            !['attack','jump_next','jump_held','crouch_try'].every(k=>typeof f.held[k]==='boolean'))) throw Error('foundation schema/type invariant');
        if (n && (!Array.isArray(n.events) || n.events.length > 512 || !Array.isArray(n.remotes) || n.remotes.length > 256)) throw Error('network sample overflow');
        if (d && (!Array.isArray(d.runtime_errors) || d.runtime_errors.length > 512)) throw Error('diagnostic error overflow');
        const canvas = document.querySelector('#canvas'), rect = canvas && canvas.getBoundingClientRect();
        const descriptor = Object.getOwnPropertyDescriptor(window, 'OUTBREAK_FOUNDATION_METRICS');
        const entries = type => {
            if (typeof performance.getEntriesByType !== 'function') return null;
            const rows = performance.getEntriesByType(type);
            if (rows.length > 512) throw Error('resource entry overflow');
            return rows.map(e => ({name: (() => { const u = new URL(e.name, location.href); return u.origin + u.pathname; })(),
                startTime:e.startTime,duration:e.duration,decodedBodySize:e.decodedBodySize,encodedBodySize:e.encodedBodySize,transferSize:e.transferSize}));
        };
        const sample = {now_ms:performance.now(),origin:location.origin,foundation:f || null,diagnostics:d || null,timing:t || null,network:n,
            audio:a || null,model:m || null,
            immutable:{foundation:!!f && deep(f),diagnostics:!!d && deep(d),timing:!!t && deep(t),network:!!n && deep(n),audio:!!a && deep(a),model:!!m && deep(m),
                foundation_descriptor:!!descriptor && descriptor.writable === false && descriptor.enumerable === true && descriptor.configurable === true && !descriptor.set},
            document:{focused:document.hasFocus(),visibility:document.visibilityState,pointer_is_canvas:!!canvas && document.pointerLockElement === canvas},
            viewport:{width:innerWidth,height:innerHeight,dpr:devicePixelRatio},
            canvas:canvas ? {x:rect.x,y:rect.y,width:rect.width,height:rect.height,intrinsic_width:canvas.width,intrinsic_height:canvas.height} : null,
            performance:collect ? null : {navigation:entries('navigation'),resources:entries('resource')},
            js_heap:performance.memory && Number.isFinite(performance.memory.usedJSHeapSize) ? {available:true,used_bytes:performance.memory.usedJSHeapSize} : {available:false,used_bytes:null}};
        let sampleBytes=0;for(const c of JSON.stringify(sample)){const p=c.codePointAt(0);sampleBytes+=p<128?1:p<2048?2:p<65536?3:4;}
        if (sampleBytes > 262144) throw Error('public sample byte overflow');
        return sample;
    }
    if (!collect) return read();
    // rAF observer timestamps and game raw intervals stay separate. No game tick/state writes.
    return new Promise(resolve => {
        let id=null,timer=null,start=null,last=null,bytes=0,finished=false;
        const tuples=[];
        const finish = (error, sample) => {
            if (finished) return; finished=true;
            if (id !== null) cancelAnimationFrame(id); if (timer !== null) clearTimeout(timer);
            resolve({error:error || null,tuples,last:sample || last,observer_cancelled:true});
        };
        const step = timestamp => {
            try {
                const s=read();last=s;
                if (!s.foundation || !s.timing || !s.diagnostics || !s.network) throw Error('missing steady snapshot');
                if (s.document.visibility !== 'visible' || !s.document.focused || s.network.error || s.network.state !== 'BN_ACTIVE' || s.diagnostics.runtime_errors.length || s.diagnostics.phase !== 'running' || s.audio?.error) throw Error('steady lifecycle/document/audio error');
                if (!Object.values(s.immutable).every(Boolean)) throw Error('mutable steady snapshot');
                const f=s.foundation,t=s.timing;
                if (!f.actor_present || f.document.visibility!=='visible' || !f.document.focused ||
                    f.frame_count!==s.diagnostics.frame_count || f.rendered_frame_count!==s.diagnostics.rendered_frame_count ||
                    t.frame_id+1!==f.frame_count || t.lifecycle_state!==4 || t.embedded_server_path_compiled!==false ||
                    s.network.map_revision!==2 || s.network.map_name!=='dev_outbreak_browser' || s.network.own.state!==0) throw Error('steady source/identity invariant');
                const tuple=[timestamp,s.now_ms,f.frame_count,f.rendered_frame_count,t.frame_id,t.raw_elapsed_ms,t.prediction_elapsed_ms,f.wasm_heap_bytes,s.js_heap.available?s.js_heap.used_bytes:null];
                if (tuples.length >= 32768) throw Error('32768 sample overflow');
                bytes+=JSON.stringify(tuple).length+1;if(bytes>8*1024*1024)throw Error('8MiB tuple overflow');
                tuples.push(tuple);
                if(start===null)start=timestamp;
                if(timestamp-start>=60000)return finish(null,s);
                id=requestAnimationFrame(step);
            } catch(e) { finish(String(e.message).slice(0,512),last); }
        };
        timer=setTimeout(()=>finish('steady observer deadline',last),62000);
        id=requestAnimationFrame(step);
    });
}

function validate(s, terminal=false) {
    fail(s && finite(s.now_ms) && s.origin === 'http://127.0.0.1:29866','wrong origin/missing observation');
    const f=s.foundation,d=s.diagnostics,t=s.timing,n=s.network;
    fail(exact(f,['schema_version','profile','frame_count','rendered_frame_count','actor_present','yaw_degrees','pitch_degrees','held','wasm_heap_bytes','logical_viewport','document']),'foundation schema');
    fail(f.schema_version===1 && f.profile==='network-client' && integer(f.frame_count) && integer(f.rendered_frame_count) && typeof f.actor_present==='boolean','foundation counters/profile');
    fail(f.actor_present ? finite(f.yaw_degrees)&&finite(f.pitch_degrees) : f.yaw_degrees===null&&f.pitch_degrees===null,'foundation angles');
    fail(exact(f.held,['move','strafe','attack','jump_next','jump_held','crouch_try']) && Number.isInteger(f.held.move)&&Number.isInteger(f.held.strafe) && ['attack','jump_next','jump_held','crouch_try'].every(k=>typeof f.held[k]==='boolean'),'held schema');
    fail(f.actor_present || neutral(s),'absent actor held');
    fail(integer(f.wasm_heap_bytes) && exact(f.logical_viewport,['width','height']) && integer(f.logical_viewport.width)&&integer(f.logical_viewport.height),'heap/viewport schema');
    fail(exact(f.document,['focused','visibility','pointer_is_canvas']) && typeof f.document.focused==='boolean' && typeof f.document.visibility==='string' && typeof f.document.pointer_is_canvas==='boolean','document schema');
    fail(Object.values(s.immutable).every(v=>v===true),'mutable/missing public snapshot');
    fail(d?.schema_version===1&&d.profile==='network-client'&&d.frame_count===f.frame_count&&d.rendered_frame_count===f.rendered_frame_count&&Array.isArray(d.runtime_errors)&&d.runtime_errors.length===0,'diagnostics/schema/error');
    fail(t?.schema_version===1&&integer(t.frame_id)&&t.frame_id+1===f.frame_count&&finite(t.raw_elapsed_ms)&&t.raw_elapsed_ms>=0&&t.raw_elapsed_ms<=1000&&finite(t.prediction_elapsed_ms)&&t.prediction_elapsed_ms>=0&&t.prediction_elapsed_ms<=50&&t.embedded_server_path_compiled===false,'source frame/timing relationship');
    fail(n?.schema_version===1&&n.profile==='network-client'&&Array.isArray(n.events)&&n.events.length<=512&&Array.isArray(n.remotes)&&n.remotes.length<=256,'network schema/overflow');
    fail(n.own && Number.isInteger(n.own.cn)&&Number.isInteger(n.own.life)&&Array.isArray(n.own.position)&&n.own.position.length===3&&n.own.position.every(finite),'native own identity/position');
    fail(s.audio?.schema_version===1 && !s.audio.error && s.audio.phase!=='error','audio schema/error');
    fail(s.model?.schema_version===1&&s.model.profile==='network-client','model schema');
    if (!terminal) {
        fail(n.state==='BN_ACTIVE'&&n.error===0&&n.map_name==='dev_outbreak_browser'&&n.map_revision===2&&n.own.cn>=0&&n.own.life>=0&&n.own.state===0&&n.counters?.spawn_acknowledgments>0,'not genuine joined/alive map2 client');
        fail(n.events.filter(e=>e.kind===1).slice(0,4).map(e=>e.milestone).join()==='1,2,3,4','missing genuine native milestones');
        fail(d.phase==='running'&&d.map_name==='dev_outbreak_browser'&&f.actor_present&&f.rendered_frame_count>0&&t.lifecycle_state===4,'not running rendered active actor');
        fail(s.document.visibility==='visible','page not visible');
    } else {
        fail(d.phase==='running'||d.phase==='stopped','unrelated terminal diagnostics');
        fail(n.error===0 || (n.error===15&&n.state==='BN_FAILED'),'unrelated terminal error');
    }
    return s;
}

function frameFacts(batch) {
    fail(!batch.error,batch.error || 'steady failure');
    fail(Array.isArray(batch.tuples)&&batch.tuples.length>=2&&batch.tuples.length<=32768,'steady sample count');
    const rows=batch.tuples,intervals=[];let duplicates=0,peak=0,jsPeak=null;
    for(let i=0;i<rows.length;i++) {
        const r=rows[i];fail(Array.isArray(r)&&r.length===9&&r.slice(0,8).every(finite),'invalid sample tuple');
        fail(integer(r[2])&&integer(r[3])&&integer(r[4])&&r[4]+1===r[2]&&r[5]>=0&&r[5]<=1000&&r[6]>=0&&r[6]<=50&&integer(r[7]),'invalid game timing/counter tuple');
        peak=Math.max(peak,r[7]);if(r[8]!==null){fail(integer(r[8]),'JS heap invalid');jsPeak=Math.max(jsPeak||0,r[8]);}
        if(!i)continue;const p=rows[i-1];fail(r[0]>p[0]&&r[1]>p[1],'observer clock regression/stale');
        const delta=r[2]-p[2];fail(delta===0||delta===1,'unexplained skipped/regressed game frames');
        fail(r[3]>=p[3]&&r[3]-p[3]<=2,'render counter regression/jump');
        if(delta===0){fail(r.slice(2,8).every((v,k)=>v===p[k+2]),'same frame changed timing');duplicates++;fail(r[0]-rows[Math.max(0,i-duplicates)][0]<=1000,'stale game frame');}
        else {intervals.push(r[5]);duplicates=0;}
    }
    const elapsed=rows.at(-1)[0]-rows[0][0];fail(elapsed>=60000&&elapsed<=62000,'steady duration');
    fail(intervals.length>0,'no game progress');const sorted=intervals.slice().sort((a,b)=>a-b);
    const p95=sorted[Math.ceil(sorted.length*.95)-1],fps=(rows.at(-1)[3]-rows[0][3])*1000/elapsed;
    return {status:fps>=55&&p95<=33.4&&peak<=512*1024*1024?'PASS':'FAIL',elapsed_ms:elapsed,average_rendered_fps:fps,p95_game_interval_ms:p95,
        game_intervals:intervals.length,observer_samples:rows.length,duplicate_observer_samples:rows.length-1-intervals.length,long_game_intervals:intervals.filter(x=>x>33.4).length,
        wasm_peak_bytes:peak,js_heap:{available:jsPeak!==null,peak_bytes:jsPeak},tuples:rows,tuple_fields:['raf_timestamp_ms','observer_now_ms','game_frame','rendered_count','timing_frame','raw_game_ms','prediction_ms','wasm_bytes','js_heap_bytes_or_null']};
}

async function measureFoundation(page) {
    const report={kind:'FOUNDATION_COMPONENT_OBSERVATIONS',schema_version:1,scope:'CALLER_SUPPLIED_PAGE; supervisor identity/execution authorization external',checks:{},events:[],initial:null,last:null,final:null,
        load:{status:'NOT_OBSERVED'},canvas:{status:'NOT_OBSERVED'},input:{mouse:{status:'NOT_OBSERVED'},movement:{status:'NOT_OBSERVED'},escape_release:{status:'NOT_OBSERVED'},recapture:{status:'NOT_OBSERVED'}},audio:{status:'NOT_OBSERVED'},frames:null,expected_terminal:{status:'NOT_OBSERVED'},cleanup:{keys_released:false,button_released:false,probe_closed:null,errors:[]},
        pending_external:['accepted artifact/source/native/pins and startup errors','GPU identity and process/RSS ownership/peak','complete requested artifact/notices transfer inventory','physical pixels/animation/alignment/audibility and human playtest','P0/MVP/authority acceptance']};
    let probe=null,previous=null;const keys=new Set();let button=false;
    const event=name=>{fail(report.events.length<512,'512 event overflow');report.events.push({stage:name});};
    const retain=s=>{fail(bytes(s)<=262144,'sample byte overflow');report.last=s;return s;};
    const read=async(terminal=false)=>validate(retain(await page.evaluate(observe,false)),terminal);
    const progressed=(a,b)=>{fail(b.now_ms>a.now_ms&&b.foundation.frame_count>a.foundation.frame_count,'stale observation/no frame progress');};
    const poll=async(predicate,terminal=false)=>{
        let start=null;
        for(let i=0;i<80;i++){const s=await read(terminal);if(start===null)start=s.now_ms;fail(s.now_ms-start<=2000,'2s observation deadline');if(predicate(s))return s;await page.waitForTimeout(25);}
        throw Error('2s observation deadline');
    };
    const down=async()=>{for(const k of ['w','Space']){keys.add(k);await page.keyboard.down(k);}button=true;await page.mouse.down({button:'left'});};
    const release=async()=>{
        for(const k of [...keys]){try{await page.keyboard.up(k);keys.delete(k);}catch(e){report.cleanup.errors.push(String(e.message).slice(0,256));}}
        if(button)try{await page.mouse.up({button:'left'});button=false;}catch(e){report.cleanup.errors.push(String(e.message).slice(0,256));}
    };
    try {
        fail(arguments.length===1,'exact measureFoundation(page) API; no options/hooks');
        event('entry');const initial=await read();report.initial=initial;previous=initial;
        fail(initial.viewport.width===1280&&initial.viewport.height===720&&initial.viewport.dpr===1,'reference viewport/DPR');
        const c=initial.canvas,f=initial.foundation;fail(c&&[c.x,c.y,c.width,c.height,c.intrinsic_width,c.intrinsic_height].every(finite)&&c.width>0&&c.height>0&&c.x>=0&&c.y>=0&&c.x+c.width<=1281&&c.y+c.height<=721,'canvas clipping/availability');
        const aspect=1280/720;fail(Math.abs(c.width/c.height-aspect)<.01&&Math.abs(c.intrinsic_width/c.intrinsic_height-aspect)<.01&&Math.abs(f.logical_viewport.width/f.logical_viewport.height-aspect)<.01,'canvas aspect/projection');
        report.canvas={status:'PASS',css:c,logical:f.logical_viewport,viewport:initial.viewport};
        const entries=initial.performance;
        const rows=entries?.navigation&&entries?.resources?[...entries.navigation,...entries.resources]:null;
        const sizes=rows&&rows.length>0&&rows.every(e=>['decodedBodySize','encodedBodySize','transferSize'].every(k=>integer(e[k])));
        report.load={status:sizes?'PASS':'NOT_OBSERVED',navigation:entries?.navigation??null,resources:entries?.resources??null,
            running_observed_since_navigation_ms:initial.now_ms,readiness_is_upper_bound:true,
            bytes:sizes?{decoded:rows.reduce((a,e)=>a+e.decodedBodySize,0),encoded:rows.reduce((a,e)=>a+e.encodedBodySize,0),transfer:rows.reduce((a,e)=>a+e.transferSize,0)}:null,
            cache_meaning:'zero transfer may reflect cache or API restrictions; no cold/warm-cache assertion'};
        if(sizes&&report.load.bytes.transfer>16*1024*1024)report.load.status='FAIL';
        report.audio.before_gesture=initial.audio;
        await page.bringToFront();if(!initial.document.pointer_is_canvas||!initial.diagnostics.input_locked)await page.locator('#canvas').click({timeout:2000});
        let s=await poll(x=>x.foundation.frame_count>initial.foundation.frame_count&&x.document.focused&&x.document.pointer_is_canvas&&x.foundation.document.pointer_is_canvas&&x.diagnostics.input_locked);
        report.audio.after_gesture=s.audio;report.audio.physical_audibility='PENDING_HUMAN';
        report.audio.status='PASS';report.audio.observed_context_running=s.audio.audio_context_state==='running';report.audio.observed_cue_playing=s.audio.openal_source_state===4114;
        report.load.controlled_observed_since_navigation_ms=s.now_ms;report.checks.ready_observed_within_15s=s.now_ms<=15000?'PASS':'FAIL';
        fail(neutral(s),'entry capture not neutral');previous=s;
        event('relative-mouse');await page.mouse.move(640,360);s=await read();await page.mouse.move(672,376);
        const moved=await poll(x=>x.foundation.frame_count>s.foundation.frame_count&&(x.foundation.yaw_degrees!==s.foundation.yaw_degrees||x.foundation.pitch_degrees!==s.foundation.pitch_degrees));progressed(s,moved);
        const yaw=wrap(moved.foundation.yaw_degrees-s.foundation.yaw_degrees),pitch=moved.foundation.pitch_degrees-s.foundation.pitch_degrees;
        fail(yaw>0&&pitch<0,'relative mouse expected direction (default unscoped invmouse0)');report.input.mouse={status:'PASS',yaw_delta_wrapped:yaw,pitch_delta:pitch};
        event('W250');previous=await read();keys.add('w');try{await page.keyboard.down('w');await page.waitForTimeout(250);}finally{await release();}
        s=await poll(x=>x.foundation.frame_count>previous.foundation.frame_count&&neutral(x));progressed(previous,s);
        const distance=Math.hypot(...s.network.own.position.map((v,i)=>v-previous.network.own.position[i]));fail(distance>=2,'W250 movement below2');report.input.movement={status:'PASS',distance_units:distance,before:previous.network.own.position,after:s.network.own.position};
        // Require a fresh stationary state before the held-input test.
        previous=s;await page.waitForTimeout(50);s=await read();progressed(previous,s);fail(Math.hypot(...s.network.own.position.map((v,i)=>v-previous.network.own.position[i]))<=.05,'post-input state not stable');
        event('escape-held');await down();await page.waitForTimeout(100);previous=await read();
        fail(previous.foundation.held.move!==0&&previous.foundation.held.attack&&(previous.foundation.held.jump_next||previous.foundation.held.jump_held),'held actions not observed');
        await page.keyboard.press('Escape');s=await poll(x=>x.foundation.frame_count>previous.foundation.frame_count&&neutral(x)&&!x.document.pointer_is_canvas&&!x.diagnostics.input_locked);progressed(previous,s);
        report.input.escape_release={status:'PASS',sample:s};await release();
        previous=s;await page.locator('#canvas').click({timeout:2000});s=await poll(x=>x.foundation.frame_count>previous.foundation.frame_count&&x.document.pointer_is_canvas&&x.diagnostics.input_locked);fail(neutral(s),'recapture not neutral');report.input.recapture={status:'PASS'};
        event('warmup-3s');await page.waitForTimeout(3000);s=await read();fail(s.document.focused&&s.document.pointer_is_canvas,'warmup capture/focus');
        event('steady-60s');const batch=await page.evaluate(observe,true);if(batch.last)retain(batch.last);report.frames={status:'FAIL',tuples:batch.tuples,error:batch.error};
        validate(batch.last);report.frames=frameFacts(batch);fail(report.frames.status==='PASS','steady FPS/p95/Wasm budget');
        event('last-focus-loss');await down();await page.waitForTimeout(100);previous=await read();
        fail(previous.foundation.held.move!==0&&previous.foundation.held.attack&&(previous.foundation.held.jump_next||previous.foundation.held.jump_held),'terminal held actions not observed');
        const candidate=await page.context().newPage();fail(candidate!==page,'probe must not be original page');probe=candidate;
        fail(probe.url()==='about:blank','owned blank probe required');await probe.bringToFront();
        let hidden=false,terminal=null;
        for(let i=0;i<80;i++){
            s=await read(true);if(s.now_ms-previous.now_ms>2000)break;if(s.document.visibility==='hidden')hidden=true;
            if(hidden&&neutral(s)&&!s.document.pointer_is_canvas&&s.network.state==='BN_FAILED'&&s.network.error===15&&s.network.events.some(e=>e.kind===2&&e.error===15)){terminal=s;break;}
            await page.waitForTimeout(25);
        }
        report.expected_terminal={status:terminal?'PASS':'NOT_OBSERVED',classification:terminal?'EXPECTED_HIDDEN_BNE_VISIBILITY15':'NO_COMPLETE_HIDDEN_TERMINAL_EVIDENCE',hidden_observed:hidden,sample:s};
        report.final=s;
    } catch(e) {
        report.checks.component_sequence='FAIL';report.error=String(e.message).slice(0,512);
    } finally {
        await release();
        if(probe)try{await probe.close({runBeforeUnload:false});report.cleanup.probe_closed=true;}catch(e){report.cleanup.probe_closed=false;report.cleanup.errors.push(String(e.message).slice(0,256));}
        report.cleanup.keys_released=keys.size===0;report.cleanup.button_released=!button;
        report.checks.cleanup=report.cleanup.keys_released&&report.cleanup.button_released&&report.cleanup.probe_closed!==false&&report.cleanup.errors.length===0?'PASS':'FAIL';
    }
    if(!report.final)report.final=report.last;
    // No aggregate performance/P0 PASS. Preserve bounded failure and cleanup facts.
    if(bytes(report)>8*1024*1024){report.error='8MiB report overflow';report.checks.component_sequence='FAIL';report.frames={status:'FAIL',overflow:true,retained_first:report.frames?.tuples?.slice(0,128),retained_last:report.frames?.tuples?.slice(-128)};}
    return report;
}
module.exports={measureFoundation};
