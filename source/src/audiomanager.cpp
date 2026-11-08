// audio interface of the engine

#include "cube.h"

#define DEBUGCOND (audiodebug==1)

VARF(audio, 0, 1, 1, initwarning("sound configuration", INIT_RESET, CHANGE_SOUND));
VARP(audiodebug, 0, 0, 1);
char *musicdonecmd = NULL;

VARFP(musicvol, 0, 128, 255, audiomgr.setmusicvol(musicvol));

// audio manager

audiomanager::audiomanager()
{
    nosound = true;
    currentpitch = 1.0f;
    device = NULL;
    context = NULL;
}

void audiomanager::initsound()
{
    if(!audio)
    {
        conoutf("audio is disabled");
        return;
    }

    nosound = true;
    device = NULL;
    context = NULL;

    // list available devices
    if(alcIsExtensionPresent(NULL, "ALC_ENUMERATION_EXT"))
    {
        const ALCchar *devices = alcGetString(NULL, ALC_DEVICE_SPECIFIER);
        if(devices)
        {
            string d;
            copystring(d, "Audio devices: ");

            // null separated device string
            for(const ALchar *c = devices; *c; c += strlen(c)+1)
            {
                if(c!=devices) concatstring(d, ", ");
                concatstring(d, c);
            }
            conoutf("%s", d);
        }
    }

    // open device
    const char *devicename = getalias("openaldevice");
    device = alcOpenDevice(devicename && devicename[0] ? devicename : NULL);

    if(device)
    {
        context = alcCreateContext(device, NULL);
        if(context)
        {
            alcMakeContextCurrent(context);

            alDistanceModel(AL_INVERSE_DISTANCE_CLAMPED);

            // backend infos
            conoutf("Sound: %s / %s (%s)", alcGetString(device, ALC_DEVICE_SPECIFIER), alGetString(AL_RENDERER), alGetString(AL_VENDOR));
            conoutf("Driver: %s", alGetString(AL_VERSION));

            // allocate OpenAL resources
            sourcescheduler::instance().init(16);

            // let the stream get the first source from the scheduler
            gamemusic = new oggstream();
            if(!gamemusic->valid) DELETEP(gamemusic);
            setmusicvol(musicvol);

            nosound = false;
        }
    }

    if(nosound)
    {
        ALERR;
        if(context) alcDestroyContext(context);
        if(device) alcCloseDevice(device);
        conoutf("sound initialization failed!");
    }
}

#if defined(__EMSCRIPTEN__) && !defined(STANDALONE)
#include <emscripten/emscripten.h>
EM_JS_DEPS(outbreak_audio_proof, "$AL");

// Use the inspected SDK's real OpenAL context, not a second Web Audio backend.
EM_JS(int, browserproofcontext, (uintptr_t handle, int action), {
    const owner = AL.contexts[handle];
    if (!owner || !owner.audioCtx) return 0;
    if (action === 0) return owner.T052Error ? 0 : 1;
    const epoch = owner.T052Epoch = (owner.T052Epoch || 0) + 1;
    const report = (error) => {
        if (AL.contexts[handle] !== owner || owner.T052Epoch !== epoch) return;
        owner.T052Error = String(error).slice(0, 512);
    };
    try {
        if (action === 1) {
            owner.T052Error = null;
            const result = owner.audioCtx.resume(); // invoked synchronously in the canvas gesture
            if (result && result.catch) result.catch(report);
        } else if (action === 2) {
            if (owner.audioCtx.state !== 'closed' && owner.audioCtx.state !== 'suspended') {
                const result = owner.audioCtx.suspend();
                if (result && result.catch) result.catch(report);
            }
        } else if (action === 3) {
            const actual = owner.audioCtx;
            const before = window.OUTBREAK_AUDIO_DIAGNOSTICS;
            const gesture = before ? before.gesture_count : 0;
            // Engine sources/context are torn down synchronously after this call.
            // Close the underlying device context after those nodes are released.
            Promise.resolve().then(() => actual.state === 'closed' ? undefined : actual.close()).catch((error) => {
                const message = 'OpenAL proof AudioContext close failed: ' + String(error).slice(0, 512);
                console.error(message);
                const current = window.OUTBREAK_AUDIO_DIAGNOSTICS;
                if (current && current.gesture_count === gesture && current.phase === 'stopped') {
                    Object.defineProperty(window, 'OUTBREAK_AUDIO_DIAGNOSTICS', {
                        value: Object.freeze(Object.assign({}, current, {phase: 'error', error: message})),
                        writable: false, configurable: true, enumerable: true
                    });
                }
            });
        }
        return 1;
    } catch (error) {
        report(error);
        return 0;
    }
});

EM_JS(void, browserproofsnapshot, (const char *phase, int gestures, int loaded, int plays,
                                  int source_state, const char *error, uintptr_t handle), {
    const owner = handle ? AL.contexts[handle] : null;
    const observedError = owner && owner.T052Error;
    let actualError = observedError || (error ? UTF8ToString(error) : null);
    const previous = window.OUTBREAK_AUDIO_DIAGNOSTICS;
    if (!actualError && !handle && UTF8ToString(phase) === 'stopped' && previous &&
        previous.error && previous.error.startsWith('OpenAL proof AudioContext close failed:'))
        actualError = previous.error;
    Object.defineProperty(window, 'OUTBREAK_AUDIO_DIAGNOSTICS', {
        value: Object.freeze({schema_version: 1, phase: actualError ? 'error' : UTF8ToString(phase),
            gesture_count: gestures, sample_loaded: !!loaded, play_count: plays,
            openal_source_state: source_state < 0 ? null : source_state,
            audio_context_state: owner && owner.audioCtx ? owner.audioCtx.state : null,
            error: actualError}),
        writable: false, configurable: true, enumerable: true
    });
});

void audiomanager::browserproofpublish()
{
    browserproofsnapshot(browserproofphase, browserproofgestures,
        browserproofbuffer && browserproofbuffer->id, browserproofplays,
        browserproofstate, browserprooferror[0] ? browserprooferror : NULL, (uintptr_t)context);
}

bool audiomanager::browserproofrelease()
{
    browserproofstate = -1;
    bool ok = true;
    if(browserproofsource)
    {
        if(browserproofsource->valid)
        {
            if(!browserproofsource->stop())
            {
                copystring(browserprooferror, "OpenAL proof source stop failed");
                ok = false;
            }
            if(!browserproofsource->delete_())
            {
                copystring(browserprooferror, "OpenAL proof source deletion failed");
                return false; // retain ownership for retry, never allocate a duplicate
            }
            browserproofsource->valid = false;
        }
        DELETEP(browserproofsource);
    }
    if(browserproofbuffer && browserproofbuffer->id)
    {
        alclearerr();
        const ALuint id = browserproofbuffer->id;
        alDeleteBuffers(1, &id);
        if(alerr(false))
        {
            copystring(browserprooferror, "OpenAL proof buffer deletion failed");
            return false; // keep the buffer/backend alive for a later cleanup retry
        }
        browserproofbuffer->id = 0; // the destructor must not delete the same buffer again
    }
    DELETEP(browserproofbuffer);
    browserproofstate = -1;
    return ok;
}

void audiomanager::browserprooffail(const char *error)
{
    if(error != browserprooferror) copystring(browserprooferror, error);
    conoutf("Browser audio proof: %s", browserprooferror);
    browserproofrelease();
    browserproofphase = "error";
    browserproofpublish();
}

bool audiomanager::browserproofquerystate()
{
    browserproofstate = -1;
    if(!browserproofsource) return true;
    alclearerr();
    ALint actual = 0;
    alGetSourcei(browserproofsource->id, AL_SOURCE_STATE, &actual);
    const ALenum error = alGetError();
    if(error != AL_NO_ERROR)
    {
        formatstring(browserprooferror)("OpenAL proof source query failed (0x%x)", int(error));
        return false;
    }
    browserproofstate = actual;
    return true;
}

void audiomanager::browserproofgesture()
{
    ++browserproofgestures;
    browserprooferror[0] = '\0';
    if(!browserproofrelease()) { browserprooffail(browserprooferror); return; }
    if(nosound)
    {
        // This is the existing engine initialization, only now inside a real gesture.
        initsound();
        if(nosound)
        {
            // initsound already disposes failed handles; do not reuse its dangling fields.
            context = NULL;
            device = NULL;
            browserprooffail("OpenAL backend initialization failed");
            return;
        }
    }
    if(!context || !device || alcGetCurrentContext() != context)
    {
        browserprooffail("OpenAL proof backend has no current context");
        return;
    }
    if(!browserproofcontext((uintptr_t)context, 1))
    {
        browserprooffail("OpenAL proof AudioContext resume failed");
        return;
    }
    // Do not invoke the inherited map-sound reload side effect of setlistenervol.
    alclearerr();
    alListenerf(AL_GAIN, soundvol/255.0f);
    if(alerr(false)) { browserprooffail("OpenAL proof listener gain failed"); return; }
    browserproofphase = "ready";
    browserproofbuffer = new sbuffer;
    browserproofbuffer->name = "outbreak/proof_tone";
    if(!browserproofbuffer->load(false))
    {
        browserprooffail("Cannot load/decode packages/audio/outbreak/proof_tone.wav");
        return;
    }
    browserproofsource = new source;
    if(!browserproofsource->valid || !browserproofsource->buffer(browserproofbuffer->id) ||
       !browserproofsource->looping(false) || !browserproofsource->sourcerelative(true) ||
       !browserproofsource->position(0.0f, 0.0f, 0.0f) || !browserproofsource->gain(1.0f) ||
       !browserproofsource->pitch(1.0f) || !browserproofsource->play())
    {
        browserprooffail("OpenAL proof source configuration/play failed");
        return;
    }
    if(!browserproofquerystate()) { browserprooffail(browserprooferror); return; }
    if(browserproofstate != AL_PLAYING)
    {
        browserprooffail("OpenAL proof source did not enter AL_PLAYING");
        return;
    }
    ++browserproofplays; // actual queried OpenAL playback, not a physical audibility claim
    browserproofphase = "playing";
    browserproofpublish();
}

void audiomanager::browserproofpoll()
{
    if(!strcmp(browserproofphase, "error")) { browserproofpublish(); return; } // retry only on a later gesture
    if(!nosound && context && !browserproofcontext((uintptr_t)context, 0))
    {
        browserprooffail("OpenAL proof AudioContext resume/suspend failed");
        return;
    }
    if(!browserproofquerystate()) { browserprooffail(browserprooferror); return; }
    if(!strcmp(browserproofphase, "playing") && browserproofstate != AL_PLAYING)
        browserproofphase = "ready";
    browserproofpublish();
}

void audiomanager::browserproofstop(bool shutdown)
{
    // Startup focus reset must not manufacture an initialized backend or cue.
    if(!browserproofgestures && !shutdown) { browserproofpublish(); return; }
    const bool released = browserproofrelease();
    if(context && !nosound)
    {
        if(shutdown)
        {
            if(browserproofsource || browserproofbuffer)
            {
                // The SDK keeps buffers outside the context registry. Retain failed
                // deletion ownership and its backend for retry rather than orphan it.
                browserproofcontext((uintptr_t)context, 2);
                browserproofphase = "error";
                browserproofpublish();
                return;
            }
            browserproofcontext((uintptr_t)context, 3);
            soundcleanup(); // real scheduler/buffer/source/context/device teardown
            context = NULL;
            device = NULL;
            nosound = true; // existing later cleanup is now idempotent
        }
        else if(!browserproofcontext((uintptr_t)context, 2) && !browserprooferror[0])
            copystring(browserprooferror, "OpenAL proof AudioContext suspend failed");
    }
    browserproofstate = -1;
    browserproofphase = released && !browserprooferror[0] ? "stopped" : "error";
    browserproofpublish();
}
#endif


void audiomanager::music(char *name, int millis, char *cmd)
{
    if(nosound) return;
    stopsound();
    if(musicvol && *name)
    {
        if(cmd[0]) musicdonecmd = newstring(cmd);

        if(gamemusic->open(name))
        {
            // fade
            if(millis > 0)
            {
                const int fadetime = 1000;
                gamemusic->fadein(lastmillis, fadetime);
                gamemusic->fadeout(lastmillis+millis, fadetime);
            }

            // play
            bool loop = cmd && cmd[0];
            if(!gamemusic->playback(loop))
            {
                conoutf("could not play music: %s", name);
                return;
            }
            setmusicvol(musicvol);
        }
        else conoutf("could not open music: %s", name);
    }
}

void audiomanager::musicpreload(int id)
{
    if(nosound) return;
    stopsound();
    if(musicvol && (id>=M_FLAGGRAB && id<=M_LASTMINUTE2) && musics.inrange(id))
    {
        char *name = musics[id];
        conoutf("preloading music #%d : %s", id, name);
        if(gamemusic->open(name))
        {
            /*defformatstring(whendone)("musicvol %d", musicvol);
            musicdonecmd = newstring(whendone);
            conoutf("when done: %s", musicdonecmd);*/
            const int preloadfadetime = 3;
            gamemusic->fadein(lastmillis, preloadfadetime);
            gamemusic->fadeout(lastmillis+2*preloadfadetime, preloadfadetime);
            if(!gamemusic->playback(false))
            {
                conoutf("could not play music: %s", name);
                return;
            }
            setmusicvol(1); // not 0 !
        }
        else conoutf("could not open music: %s", name);
    }
    else setmusicvol(musicvol); // call "musicpreload -1" to ensure musicdonecmd runs - but it should w/o that
}

void audiomanager::musicsuggest(int id, int millis, bool rndofs) // play bg music if nothing else is playing
{
    if(nosound || !gamemusic) return;
    if(gamemusic->playing()) return;
    if(!musicvol) return;
    if(!musics.inrange(id))
    {
        conoutf("\f3music %d not registered", id);
        return;
    }
    char *name = musics[id];
    if(gamemusic->open(name))
    {
        gamemusic->fadein(lastmillis, 1000);
        gamemusic->fadeout(millis ? lastmillis+millis : 0, 1000);
        if(rndofs) gamemusic->seek(millis ? (double)rnd(millis)/2.0f : (double)lastmillis);
        if(!gamemusic->playback(rndofs)) conoutf("could not play music: %s", name);
    }
    else conoutf("could not open music: %s", name);
}

void audiomanager::musicfadeout(int id)
{
    if(nosound || !gamemusic) return;
    if(!gamemusic->playing() || !musics.inrange(id)) return;
    if(!strcmp(musics[id], gamemusic->name)) gamemusic->fadeout(lastmillis+1000, 1000);
}

void audiomanager::setmusicvol(int musicvol)
{
    if(gamemusic) gamemusic->setvolume(musicvol > 0 ? musicvol/255.0f : 0);
}

void reloadmapsoundconfig();

void audiomanager::setlistenervol(int vol)
{
    static int oldvol = 0;
    if(!nosound)
    {
        alListenerf(AL_GAIN, vol/255.0f);
        if(vol && !oldvol && !mapsounds.length()) reloadmapsoundconfig();
    }
    oldvol = vol;
}

void audiomanager::registermusic(char *name)
{
    if(nosound||!musicvol) return;
    if(!name || !name[0]) return;
    musics.add(newstring(name));
}

int audiomanager::findsound(const char *name, int vol, vector<soundconfig> &sounds)
{
    loopv(sounds)
    {
        if(!strcmp(sounds[i].buf->name, name) && (!vol || sounds[i].vol==vol)) return i;
    }
    return -1;
}

int audiomanager::addsound(const char *name, int vol, int maxuses, bool loop, vector<soundconfig> &sounds, bool load, int audibleradius)
{
    if(nosound) return -1;
    if(!soundvol) return -1;

    // check if the sound was already registered
    int index = findsound(name, vol, sounds);
    if(index > -1) return index;

    sbuffer *b = bufferpool.find(name);
    if(!b)
    {
        conoutf("\f3failed to allocate sample %s", name);
        return -1;
    }

    if(load && !b->load()) conoutf("\f3failed to load sample %s", name);

    soundconfig s(b, vol, maxuses, loop, audibleradius);
    sounds.add(s);
    return sounds.length()-1;
}

bool audiomanager::preloadmapsound(entity &e, bool trydl)
{
    if(e.type!=SOUND || !mapsounds.inrange(e.attr1)) return false;
    sbuffer *buf = mapsounds[e.attr1].buf;
    if(!buf->load(trydl) && !trydl) { conoutf("\f3failed to load sample %s", buf->name); return false; }
    return true;
}

bool audiomanager::preloadmapsounds(bool trydl)
{
    int missing = 0;
    loopv(ents)
    {
        entity &e = ents[i];
        if(e.type == SOUND && !preloadmapsound(e, trydl)) missing++;
    }
    return !missing;
}

void audiomanager::applymapsoundchanges() // during map editing, drop all mapsounds so they can be re-added
{
    loopv(locations)
    {
        location *l = locations[i];
        if(l && l->ref && l->ref->type==worldobjreference::WR_ENTITY) l->drop();
    }
}

void audiomanager::setchannels(int num)
{
    if(!nosound) sourcescheduler::instance().init(num);
};



// called at game exit
void audiomanager::soundcleanup()
{
#if defined(__EMSCRIPTEN__) && !defined(STANDALONE)
    // Normal engine exit may call here after a proof shutdown deletion failure.
    // Keep its owned handles/backend retryable rather than bypassing that failure.
    if(browserproofsource || browserproofbuffer)
    {
        browserproofstop(true);
        return;
    }
#endif
    if(nosound) return;

    // destroy consuming code
    stopsound();
    DELETEP(gamemusic);
    mapsounds.shrink(0);
    locations.deletecontents();
    gamesounds.shrink(0);

    // kill scheduler
    sourcescheduler::instance().reset();

    bufferpool.clear();

    // shutdown openal
    alcMakeContextCurrent(NULL);
    if(context) alcDestroyContext(context);
    if(device) alcCloseDevice(device);
}

// clear world-related sounds, called on mapchange
void audiomanager::clearworldsounds(bool fullclean)
{
    stopsound();
    if(fullclean) mapsounds.shrink(0);
    locations.deleteworldobjsounds();
}

void audiomanager::mapsoundreset()
{
    mapsounds.shrink(0);
    locations.deleteworldobjsounds();
}

VARP(footsteps, 0, 1, 1);
VARP(localfootsteps, 0, 1, 1);

void audiomanager::updateplayerfootsteps(playerent *p)
{
    if(!p || ispaused) return;

    const int footstepradius = 20;

    // find existing footstep sounds
    physentreference ref(p);
    location *locs[] =
    {
        locations.find(S_FOOTSTEPS, &ref, gamesounds),
        locations.find(S_FOOTSTEPSCROUCH, &ref, gamesounds),
        locations.find(S_WATERFOOTSTEPS, &ref, gamesounds),
        locations.find(S_WATERFOOTSTEPSCROUCH, &ref, gamesounds)
    };

    if(intermission)
    {
        loopi(sizeof(locs)/sizeof(locs[0]))
        {
            location *l = locs[i];
            if(!l) continue;
            l->drop();
        }
        return;
    }

    bool local = (p == camera1);
    bool inrange = footsteps && (local || (camera1->o.dist(p->o) < footstepradius));

    if(!footsteps || (local && !localfootsteps) || !inrange || p->state != CS_ALIVE || lastmillis-p->lastpain < 300 || (!p->onfloor && p->timeinair>50) || (!p->move && !p->strafe) || p->inwater)
    {
        const int minplaytime = 200;
        loopi(sizeof(locs)/sizeof(locs[0]))
        {
            location *l = locs[i];
            if(!l) continue;
            if(l->playmillis+minplaytime>totalmillis) continue; // tolerate short interruptions by enforcing a minimal playtime
            l->drop();
        }
    }
    else
    {
        // play footsteps

        float grounddist = 0;
        if(!((int(p->o.x) | int(p->o.y)) & ~(ssize - 1))) grounddist = waterlevel - S((int)p->o.x, (int)p->o.y)->floor;
        bool water = p->o.z - p->eyeheight+0.25f < waterlevel;
        if(water && grounddist > p->eyeheight) return; // don't play step sound when jumping into water

        int stepsound;
        if(p->crouching) stepsound = water ? S_WATERFOOTSTEPSCROUCH : S_FOOTSTEPSCROUCH; // crouch
        else stepsound = water ? S_WATERFOOTSTEPS : S_FOOTSTEPS; // normal

        // proc existing sounds
        bool isplaying = false;
        loopi(sizeof(locs)/sizeof(locs[0]))
        {
            location *l = locs[i];
            if(!l) continue;
            if(i+S_FOOTSTEPS==stepsound) isplaying = true; // already playing
            else l->drop(); // different footstep sound, drop it
        }

        if(!isplaying)
        {
            // play
            float rndoffset = float(rnd(500))/500.0f;
            _playsound(stepsound, ref, local ? SP_HIGH : SP_LOW, rndoffset);
        }
    }
}

// manage looping sounds
location *audiomanager::updateloopsound(int sound, bool active, float vol)
{
    location *l = locations.find(sound, NULL, gamesounds);
    if(!l && active) l = _playsound(sound, camerareference(), SP_HIGH, 0.0f, true);
    else if(l && !active) l->drop();
    if(l && vol != 1.0f) l->src->gain(vol);
    return l;
}

VARP(mapsoundrefresh, 0, 10, 1000);

void audiomanager::mutesound(int n, int off)
{
    bool mute = (off == 0);
    if(!gamesounds.inrange(n))
    {
        conoutf("\f3could not %s sound #%d", mute ? "silence" : "unmute", n);
        return;
    }
    gamesounds[n].muted = mute;
}

void audiomanager::unmuteallsounds()
{
    loopv(gamesounds) gamesounds[i].muted = false;
}

int audiomanager::soundmuted(int n)
{
    return gamesounds.inrange(n) && !gamesounds[n].muted ? 0 : 1;
}

void audiomanager::writesoundconfig(stream *f)
{
    bool wrotesound = false;
    loopv(gamesounds)
    {
        if(gamesounds[i].muted)
        {
            if(!wrotesound)
            {
                f->printf("// sound settings\n\n");
                wrotesound = true;
            }
            f->printf("mutesound %d\n", i);
        }
    }
}

void voicecom(char *sound, char *text)
{
    if(!sound || !sound[0]) return;
    if(!text || !text[0]) return;
    static int last = 0;
    if(!last || lastmillis-last > 2000)
    {
        defformatstring(soundpath)("voicecom/%s", sound);
        int s = audiomgr.findsound(soundpath, 0, gamesounds);
        if(!gamesound_isvoicecom(s)) return;
        bool playvc = true;
        if(gamesound_ispublicvoicecom(s)||(!m_teammode&&gamesound_ispublicwhenffa(s))) // public 
        {
            addmsg(SV_VOICECOM, "ri", s);
            toserver(text);
        }
        else // team
        {
            if(gamesound_isflagvoicecom(s)?m_flags_:true)
            {
                addmsg(SV_VOICECOMTEAM, "ri", s);
                defformatstring(teamtext)("%c%s", '%', text);
                toserver(teamtext);
            }
            else
            {
                playvc = false;
            }
        }
        if(voicecomsounds > 0 && playvc) audiomgr.playsound(s, SP_HIGH);
        last = lastmillis;
    }
}

COMMAND(voicecom, "ss");

void soundtest()
{
    loopi(S_NULL) audiomgr.playsound(i, rnd(SP_HIGH+1));
}

COMMAND(soundtest, "");

// sound configuration

soundconfig::soundconfig(sbuffer *b, int vol, int maxuses, bool loop, int audibleradius)
{
    buf = b;
    this->vol = vol > 0 ? vol : 100;
    this->maxuses = maxuses;
    this->loop = loop;
    this->audibleradius = audibleradius;
    this->model = audibleradius > 0 ? DM_LINEAR : DM_DEFAULT; // use linear model when radius is configured
    uses = 0;
    muted = false;
}

void soundconfig::onattach()
{
    uses++;
}

void soundconfig::ondetach()
{
    uses--;
}

vector<soundconfig> gamesounds, mapsounds;

void audiomanager::detachsounds(playerent *owner)
{
    if(nosound) return;
    // make all dependent locations static
    locations.replaceworldobjreference(physentreference(owner), staticreference(owner->o));
}


VARP(maxsoundsatonce, 0, 32, 100);

location *audiomanager::_playsound(int n, const worldobjreference &r, int priority, float offset, bool loop)
{
    if(nosound || !soundvol) return NULL;
    if(soundmuted(n)) return NULL;
    DEBUGVAR(n);
    DEBUGVAR(priority);

    if(r.type!=worldobjreference::WR_ENTITY)
    {
        // avoid bursts of sounds with heavy packetloss and in sp
        static int soundsatonce = 0, lastsoundmillis = 0;
        if(totalmillis==lastsoundmillis) soundsatonce++; else soundsatonce = 1;
        lastsoundmillis = totalmillis;
        if(maxsoundsatonce && soundsatonce>maxsoundsatonce)
        {
            DEBUGVAR(soundsatonce);
            return NULL;
        }
    }

    location *loc = new location(n, r, priority);
    locations.add(loc);
    if(!loc->stale)
    {
        if(offset>0) loc->offset(offset);
        if(currentpitch!=1.0f) loc->pitch(currentpitch);
        loc->play(loop);
    }

    return loc;
}

void audiomanager::playsound(int n, int priority) { _playsound(n, camerareference(), priority); }
void audiomanager::playsound(int n, physent *p, int priority) { if(p) _playsound(n, physentreference(p), priority); }
void audiomanager::playsound(int n, entity *e, int priority) { if(e) _playsound(n, entityreference(e), priority); }
void audiomanager::playsound(int n, const vec *v, int priority) { if(v) _playsound(n, staticreference(*v), priority); }

void audiomanager::playsoundname(char *s, const vec *loc, int vol)
{
    if(!nosound) return;

    if(vol <= 0) vol = 100;
    int id = findsound(s, vol, gamesounds);
    if(id < 0) id = addsound(s, vol, 0, false, gamesounds, true, 0);
    playsound(id, loc, SP_NORMAL);
}

void audiomanager::playsoundc(int n, physent *p, int priority)
{
    if(p && p!=player1) playsound(n, p, priority);
    else
    {
        addmsg(SV_SOUND, "i", n);
        playsound(n, priority);
    }
}

void audiomanager::stopsound()
{
    if(nosound) return;
    DELETEA(musicdonecmd);
    if(gamemusic) gamemusic->reset();
}

VARP(heartbeat, 0, 0, 99);

// main audio update routine

void audiomanager::updateaudio()
{
    if(nosound) return;

    alcSuspendContext(context); // don't process sounds while we mess around

    bool alive = player1->state==CS_ALIVE;
    bool firstperson = camera1==player1 || (player1->isspectating() && player1->spectatemode==SM_DEATHCAM);

    // footsteps
    updateplayerfootsteps(player1);
    loopv(players)
    {
        playerent *p = players[i];
        if(!p) continue;
        updateplayerfootsteps(p);
    }

    // water
    bool underwater = /*alive &&*/ firstperson && waterlevel > player1->o.z + player1->aboveeye;
    updateloopsound(S_UNDERWATER, underwater);

    // tinnitus
    bool tinnitus = alive && firstperson && player1->eardamagemillis>0 && lastmillis<=player1->eardamagemillis;
    location *tinnitusloc = updateloopsound(S_TINNITUS, tinnitus);

    // heartbeat
    bool heartbeatsound = heartbeat && alive && firstperson && !m_osok && player1->health <= heartbeat;
    updateloopsound(S_HEARTBEAT, heartbeatsound);

    // pitch fx
    const float lowpitch = 0.65f;
    bool pitchfx = underwater || tinnitus;
    if(pitchfx && currentpitch!=lowpitch)
    {
        currentpitch = lowpitch;
        locations.forcepitch(currentpitch);
        if(tinnitusloc) tinnitusloc->pitch(1.9f); // super high pitched tinnitus
    }
    else if(!pitchfx && currentpitch==lowpitch)
    {
        currentpitch = 1.0f;
        locations.forcepitch(currentpitch);
    }

    // update map sounds
    static int lastmapsound = 0;
    if(!lastmapsound || totalmillis-lastmapsound>mapsoundrefresh || !mapsoundrefresh)
    {
        loopv(ents)
        {
            entity &e = ents[i];
            vec o(e.x, e.y, e.z);
            if(e.type!=SOUND) continue;

            int sound = e.attr1;
            int radius = e.attr2;
            bool hearable = (radius==0 || camera1->o.dist(o)<radius);
            entityreference entref(&e);

            // search existing sound loc
            location *loc = locations.find(sound, &entref, mapsounds);

            if(hearable && !loc) // play
            {
                _playsound(sound, entref, SP_LOW, 0.0f, true);
            }
            else if(!hearable && loc) // stop
            {
                loc->drop();
            }
        }
        lastmapsound = totalmillis;
    }

    // update all sound locations
    locations.updatelocations();

    // update background music
    if(gamemusic)
    {
        if(!gamemusic->update())
        {
            // music ended, exec command
            if(musicdonecmd)
            {
                char *cmd = musicdonecmd;
                musicdonecmd = NULL;
                setcontext("hook", "musicdonecmd");
                execute(cmd);
                resetcontext();
                delete[] cmd;
            }
        }
    }

    // listener
    vec o[2];
    o[0].x = (float)(cosf(RAD*(camera1->yaw-90)));
    o[0].y = (float)(sinf(RAD*(camera1->yaw-90)));
    o[0].z = 0.0f;
    o[1].x = o[1].y = 0.0f;
    o[1].z = -1.0f;
    alListenerfv(AL_ORIENTATION, (ALfloat *) &o);
    alListenerfv(AL_POSITION, (ALfloat *) &camera1->o);

    alcProcessContext(context);
}

// binding of sounds to the 3D world

// camera

camerareference::camerareference() : worldobjreference(WR_CAMERA) {}

worldobjreference *camerareference::clone() const
{
    return new camerareference(*this);
}

const vec &camerareference::currentposition() const
{
    return camera1->o;
}

bool camerareference::nodistance()
{
    return true;
}

bool camerareference::operator==(const worldobjreference &other)
{
    return type==other.type;
}

// physent

physentreference::physentreference(physent *ref) : worldobjreference(WR_PHYSENT)
{
    ASSERT(ref);
    phys = ref;
}

worldobjreference *physentreference::clone() const
{
    return new physentreference(*this);
}

const vec &physentreference::currentposition() const
{
    return phys->o;
}

bool physentreference::nodistance()
{
    return phys==camera1;
}

bool physentreference::operator==(const worldobjreference &other)
{
    return type==other.type && phys==((physentreference &)other).phys;
}

// entity

entityreference::entityreference(entity *ref) : worldobjreference(WR_ENTITY)
{
    ASSERT(ref);
    ent = ref;
}

worldobjreference *entityreference::clone() const
{
    return new entityreference(*this);
}
const vec &entityreference::currentposition() const
{
    static vec tmp;
    tmp = vec(ent->x, ent->y, ent->z);
    return tmp;
}
bool entityreference::nodistance() { return ent->attr3>0; }
bool entityreference::operator==(const worldobjreference &other) { return type==other.type && ent==((entityreference &)other).ent; }

// static

staticreference::staticreference(const vec &ref) : worldobjreference(WR_STATICPOS)
{
    pos = ref;
}

worldobjreference *staticreference::clone() const
{
    return new staticreference(*this);
}

const vec &staticreference::currentposition() const
{
    return pos;
}

bool staticreference::nodistance()
{
    return false;
}

bool staticreference::operator==(const worldobjreference &other)
{
    return type==other.type && pos==((staticreference &)other).pos;
}

// instance

audiomanager audiomgr;

const char *soundprioritynames[] = {"LOW", "NORMAL", "HIGH", "HIGHEST", ""}; // keep in sync with enum { SP_LOW = 0, SP_NORMAL, SP_HIGH, SP_HIGHEST }

COMMANDF(sound, "is", (int *n, char *priorityname)
{
    int priority = getlistindex(priorityname, soundprioritynames, true, SP_NORMAL);
    audiomgr.playsound(*n, priority);
});

COMMANDF(applymapsoundchanges, "", (){
    if(m_coop || !multiplayer("applymapsoundchanges")) audiomgr.applymapsoundchanges();
});

COMMANDF(unmuteallsounds, "", () {
    audiomgr.unmuteallsounds();
});

COMMANDF(mutesound, "ii", (int *n, int *off)
{
    audiomgr.mutesound(*n, *off);
});

COMMANDF(soundmuted, "i", (int *n)
{
    intret(audiomgr.soundmuted(*n));
});

VAR(mapsoundchanged, 0, 0, 1);

COMMANDF(mapsoundreset, "", ()
{
    audiomgr.mapsoundreset();
    mapconfigdata.mapsoundlines.shrink(0);
    mapsoundchanged = 1;
    flagmapconfigchange();
});

VARF(soundchannels, 4, 128, 1024, audiomgr.setchannels(soundchannels));

VARFP(soundvol, 0, 128, 255, audiomgr.setlistenervol(soundvol));

COMMANDF(registersound, "siii", (char *name, int *vol, int *loop, int *audibleradius)
{
    intret(audiomgr.addsound(name, *vol, -1, *loop != 0, gamesounds, true, *audibleradius));
});

void registerdefaultsounds()
{
    loopi(S_NULL)
    {
        ASSERT(soundcfg[i].key == i);
        audiomgr.addsound(soundcfg[i].name, soundcfg[i].vol, -1, soundcfg[i].loop != 0, gamesounds, true, soundcfg[i].audibleradius);
    }
}

const char *soundcategories[SC_NUM + 1] = { "PAIN", "OWNPAIN", "WEAPON", "PICKUP", "MOVEMENT", "BULLET", "OTHER", "VOICECOM", "TEAM", "PUBLIC", "FFA", "FLAGONLY", "" };

void enumsounds(char *what)
{
    vector<char *> w;
    explodelist(what, w);
    int flags = 0, nflags = 0;
    loopv(w)
    {
        if(w[i][0] == '!') nflags |= 1 << getlistindex(w[i] + 1, soundcategories, false, SC_NUM);
        else flags |= 1 << getlistindex(w[i], soundcategories, false, SC_NUM);
        delstring(w[i]);
    }
    vector<char> res;
    loopi(S_NULL) if((soundcfg[i].flags & flags) && !(soundcfg[i].flags & nflags)) cvecprintf(res, "%d %s\n", i, escapestring(soundcfg[i].desc));
    resultcharvector(res, -1);
}
COMMAND(enumsounds, "s");

const char *mapsoundbasepath = "packages/audio/", *mapsoundfinalpath = "ambience/";
const int mapsoundbasepath_n = strlen(mapsoundbasepath), mapsoundfinalpath_n = strlen(mapsoundfinalpath);

COMMANDF(mapsound, "si", (char *name, int *maxuses)
{
    filtertext(name, name, FTXT__MEDIAFILEPATH);
    defformatstring(stripped)("%s%s", mapsoundbasepath, name[0] == '.' && name[1] == '/' ? name + 2 : name);
    unixpath(path(stripped));
    if(mapconfigdata.mapsoundlines.length() > 254)
    {
        conoutf("\f3error: too many mapsounds");
        flagmapconfigerror(LWW_CONFIGERR);
        scripterr();
    }
    else if(!strncmp(stripped, mapsoundbasepath, mapsoundbasepath_n))
    {
        name = stripped + mapsoundbasepath_n;
        audiomgr.addsound(name, 255, *maxuses, true, mapsounds, false, 0);
        intret(mapconfigdata.mapsoundlines.length());
        if(!strncmp(name, mapsoundfinalpath, mapsoundfinalpath_n)) name += mapsoundfinalpath_n; // base path for mapsoundlines is "packages/audio/ambience"
        copystring(mapconfigdata.mapsoundlines.add().name, name);
        mapconfigdata.mapsoundlines.last().maxuses = *maxuses;
        mapsoundchanged = 1;
        flagmapconfigchange();
    }
    else
    {
        conoutf("\f3error: mapsound \"%s\" outside packages/audio/", stripped);
        flagmapconfigerror(LWW_CONFIGERR);
        scripterr();
    }
});

COMMANDF(registermusic, "s", (char *name)
{
    audiomgr.registermusic(name);
});

COMMANDF(musicpreload, "i", (int *id)
{
    audiomgr.musicpreload(*id);
});

COMMANDF(music, "sis", (char *name, int *millis, char *cmd)
{
    audiomgr.music(name, *millis, cmd);
});

void mapsoundslotusage(int *n) // returns all entity indices that use a mapsound of slot n
{
    string res = "";
    loopv(ents) if(ents[i].type == SOUND && ents[i].attr1 == *n) concatformatstring(res, "%s%d", i ? " " : "", i);
    result(res);
}
COMMAND(mapsoundslotusage, "i");

void reloadmapsoundconfig()
{
    vector<char> sc;
    getcurrentmapconfig(sc, true); // only soundconfig
    execute(sc.getbuf()); // cheap and easy way ;)
}

void deletemapsoundslot(int *n, char *opt) // delete mapsound slot - only if unused or "purge" is specified
{
    EDITMP("deletemapsoundslot");
    if(!mapconfigdata.mapsoundlines.inrange(*n)) return;
    bool purgeall = !strcmp(opt, "purge"), slotused = false;
    loopv(ents) if(ents[i].type == SOUND && ents[i].attr1 == *n) slotused = true;
    if(!purgeall && slotused) { conoutf("mapsound slot #%d is in use: can't delete", *n); return; }
    audiomgr.mapsoundreset();
    int deld = 0;
    loopv(ents) if(ents[i].type == SOUND)
    {
        entity &e = ents[i];
        if(e.attr1 == *n)
        { // delete entity
            deleted_ents.add(e);
            deletesoundentity(e);
            memset((void *)&e, 0, sizeof(persistent_entity));
            e.type = NOTUSED;
            deld++;
        }
        else if(e.attr1 > *n) e.attr1--; // adjust models in higher slots
    }
    mapconfigdata.mapsoundlines.remove(*n);
    reloadmapsoundconfig();
    defformatstring(s)(" (%d mapsounds purged)", deld);
    conoutf("mapsound slot #%d deleted%s", *n, deld ? s : "");
    mapsoundchanged = 1;
    unsavededits++;
    hdr.flags |= MHF_AUTOMAPCONFIG; // requires automapcfg
}
COMMAND(deletemapsoundslot, "is");

void editmapsoundslot(int *n, char *name, char *maxuses) // edit slot parameters != ""
{
    string res = "";
    if(mapconfigdata.mapsoundlines.inrange(*n))
    {
        mapsoundline &msl = mapconfigdata.mapsoundlines[*n];
        if((*name || *maxuses) && !noteditmode("editmapsoundslot") && !multiplayer("editmapsoundslot"))
        { // change attributes
            if(*maxuses) msl.maxuses = strtol(maxuses, NULL, 0);
            if(*name) copystring(msl.name, strncmp(name, mapsoundfinalpath, mapsoundfinalpath_n) ? name : name + mapsoundfinalpath_n);
            reloadmapsoundconfig();
            mapsoundchanged = 1;
            unsavededits++;
            hdr.flags |= MHF_AUTOMAPCONFIG; // requires automapcfg
        }
        formatstring(res)("\"%s\" %d", msl.name, msl.maxuses); // give back all current attributes
    }
    result(res);
}
COMMAND(editmapsoundslot, "iss");

void getmapsoundorigin(char *fname)
{
    if(!*fname) return;
    defformatstring(s)("packages/audio/ambience/%s", fname);
    findfile(path(s), "r");
    const char *res = s;
    switch(findfilelocation)
    {
        case FFL_ZIP:     res = "zip";                                                break;
        case FFL_WORKDIR: res = fileexists(s, "r") ? "official" : "<file not found>"; break;
        case FFL_HOME:    res = "custom";                                             break;
        default:          formatstring(s)("package dir #%d", findfilelocation);       break;
    }
    result(res);
}
COMMAND(getmapsoundorigin, "s");

void mapsoundslotbyname(char *name) // returns the slot(s) that a certain mapsound file is used in
{
    string res = "";
    loopv(mapconfigdata.mapsoundlines) if(!strcmp(name, mapconfigdata.mapsoundlines[i].name)) concatformatstring(res, "%s%d", *res ? " " : "", i);
    result(res);
}
COMMAND(mapsoundslotbyname, "s");

void getmapsoundlist() // create a list of mapsound filenames
{
    vector<char *> files;
    listfilesrecursive("packages/audio/ambience", files);
    files.sort(stringsort);
    loopvrev(files) if(files.inrange(i + 1) && !strcmp(files[i], files[i + 1])) delstring(files.remove(i + 1)); // remove doubles
    int pn = strlen("packages/audio/ambience/");
    vector<char> res;
    loopv(files)
    {
        if(!strncmp(files[i], "packages/audio/ambience/", pn))
        {
            const char *s = files[i] + pn;
            int sn = strlen(s);
            if(sn > 4)
            {
                const char *e = s + sn - 4;
                if(!strcmp(e, ".ogg") || !strcmp(e, ".wav")) cvecprintf(res, "\"%s\"\n", s);
            }
        }
    }
    files.deletearrays();
    resultcharvector(res, -1);
}
COMMAND(getmapsoundlist, "");

struct tempmsslot { mapsoundline m; vector<int> oldslot; bool used; };

int tempmscmp(tempmsslot *a, tempmsslot *b)
{
    int n = strcmp(a->m.name, b->m.name);
    if(n) return n;
    return a->m.maxuses - b->m.maxuses;
}

int tempmssort(tempmsslot *a, tempmsslot *b)
{
    int n = tempmscmp(a, b);
    return n ? n : a->oldslot[0] - b->oldslot[0];
}

int tempmsunsort(tempmsslot *a, tempmsslot *b)
{
    return a->oldslot[0] - b->oldslot[0];
}

void sortmapsoundslots(char **args, int numargs)
{
    bool nomerge = false, mergeused = false, nosort = false, unknownarg = false;
    loopi(numargs) if(args[i][0])
    {
        if(!strcasecmp(args[i], "nomerge")) nomerge = true;
        else if(!strcasecmp(args[i], "nosort")) nosort = true;
        else if(!strcasecmp(args[i], "mergeused")) mergeused = true;
        else { conoutf("sortmapsoundslots: unknown argument \"%s\"", args[i]); unknownarg = true; }
    }

    EDITMP("sortmapsoundslots");
    if(unknownarg || mapconfigdata.mapsoundlines.length() < 3) return;

    vector<tempmsslot> tempslots;
    loopv(mapconfigdata.mapsoundlines)
    {
        tempslots.add().m = mapconfigdata.mapsoundlines[i];
        tempslots.last().oldslot.add(i);
        tempslots.last().used = false;
    }
    loopv(ents) if(ents[i].type == SOUND && tempslots.inrange(ents[i].attr1)) tempslots[ents[i].attr1].used = true;
    tempslots.sort(tempmssort);

    // remove double entries
    if(!nomerge) loopvrev(tempslots) if(i > 0)
    {
        tempmsslot &s1 = tempslots[i], &s0 = tempslots[i - 1];
        if(!tempmscmp(&s0, &s1) && (mergeused || !s0.used || !s1.used))
        {
            if(s1.used) s0.used = true;
            loopvj(s1.oldslot) s0.oldslot.add(s1.oldslot[j]);
            tempslots.remove(i);
        }
    }
    if(nosort) tempslots.sort(tempmsunsort);

    // create translation table
    uchar newslot[256];
    loopk(256) newslot[k] = k;
    loopv(tempslots)
    {
        tempmsslot &t = tempslots[i];
        loopvj(t.oldslot)
        {
            if(t.oldslot[j] < 256) newslot[t.oldslot[j]] = i;
        }
    }

    // translate all mapsound entities
    loopv(ents) if(ents[i].type == SOUND) ents[i].attr1 = newslot[ents[i].attr1 & 255];

    conoutf("%d mapsound slots%s, %d %sslots merged", tempslots.length(), nosort ? "" : " sorted", mapconfigdata.mapsoundlines.length() - tempslots.length(), mergeused ? "" : "unused ");

    // rewrite mapmodel slot list
    mapconfigdata.mapsoundlines.shrink(tempslots.length());
    loopv(tempslots)
    {
        mapconfigdata.mapsoundlines[i] = tempslots[i].m;
    }
    reloadmapsoundconfig();
    unsavededits++;
    mapsoundchanged = 1;
    hdr.flags |= MHF_AUTOMAPCONFIG; // requires automapcfg
}
COMMAND(sortmapsoundslots, "v");


