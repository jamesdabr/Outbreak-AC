// client.cpp, mostly network related client game code

#include "browser_map_profile.h"
#include "cube.h"
#include "bot/bot.h"
#if defined(OUTBREAK_NETWORK_CLIENT) && defined(__EMSCRIPTEN__) && !defined(STANDALONE)
#include "browsernet.h"
#include "browsernet_observer.h"
#include "enet_ws_bridge.h"
#include <emscripten/emscripten.h>
#endif

VAR(connected, 1, 0, 0);

ENetHost *clienthost = NULL;
ENetPeer *curpeer = NULL, *connpeer = NULL;
int connmillis = 0, connattempts = 0, discmillis = 0;
SVAR(curdemofile, "n/a");
extern int searchlan;

int getclientnum() { return player1 ? player1->clientnum : -1; }

bool multiplayer(const char *op)
{
#if defined(OUTBREAK_NETWORK_CLIENT) && defined(__EMSCRIPTEN__) && !defined(STANDALONE)
    return true; // A remote-only profile must not select local gameplay when joining/closed.
#endif
    // check not correct on listen server?
    if(curpeer && op) conoutf("%s%s%s not available in multiplayer", *op ? "\"" : "", *op ? op : "operation", *op ? "\"" : "");
    return curpeer!=NULL;
}

bool allowedittoggle()
{
#if defined(OUTBREAK_NETWORK_CLIENT) && defined(__EMSCRIPTEN__) && !defined(STANDALONE)
    return false;
#endif
    bool allow = !curpeer || gamemode==1;
    if(!allow) conoutf("editing in multiplayer requires coopedit mode (1)");
    return allow;
}

void throttle();

VARF(throttle_interval, 0, 5, 30, throttle());
VARF(throttle_accel,    0, 2, 32, throttle());
VARF(throttle_decel,    0, 2, 32, throttle());

void throttle()
{
    if(!curpeer) return;
    ASSERT(ENET_PEER_PACKET_THROTTLE_SCALE==32);
    enet_peer_throttle_configure(curpeer, throttle_interval*1000, throttle_accel, throttle_decel);
}

string clientpassword = "";
int connectrole = CR_DEFAULT;
bool modprotocol = false;

#if defined(OUTBREAK_NETWORK_CLIENT) && defined(__EMSCRIPTEN__) && !defined(STANDALONE)
// T061: one consumed boot, genuine ENet peers/parser, no local-session fallback.
extern vector<uchar> messages;
extern packetqueue pktlogger;
extern bool sendmapidenttoserver;
namespace
{
    BrowserNetState bnphase = BN_IDLE;
    int bnerror = BNE_NONE, bnstage = 0, bncn = -1, bnlife = -1, bnparserdepth = 0;
    bool bnconsumed = false, bnseenframe = false, bnpending = false, bndiscsent = false, bndrained = false;
    unsigned bnframeid = 0, bneventsleft = 0;
    bool bnhasspawnrequest = false;
    bool bnspawnack = false;
    enet_uint32 bnlastspawnrequest = 0;
    double bnjoinat = 0, bncloseat = 0;
    bool bnmap = false;
    struct BNRemote { bool valid; int cn, life, count; float x,y,z; double at; } bnremotes[MAXCLIENTS] = {};
    struct BNEvent { int kind, milestone, cn, life, error; double at; } bnevents[512];
    int bneventcount = 0;
    struct BNCounters
    {
        unsigned begin_calls, repeated_begin, frame_calls, frame_advances, ws_frames,
          service_calls, game_events, receive_packets, send_queued, send_rejected,
          owned_local_attempts, milestones, life_observations, position_receipts,
          remove_receipts, map_receipts, join_timeouts, spawn_requests, spawn_acknowledgments, teardowns;
    } bnc = {};
    double bnnow() { return emscripten_get_now(); }
    bool bnterminal() { return bnphase==BN_CLOSING || bnphase==BN_FAILED; }
    void bninputoff()
    {
        if(!player1) return;
        player1->attacking = player1->jumpnext = false;
        player1->move = player1->strafe = 0;
        player1->state = CS_SPECTATE;
    }
    void bnrecord(int kind, int milestone=0, int cn=-1, int life=-1)
    {
        if(bneventcount>=512)
        {
            if(!bnerror) bnerror=BNE_BACKLOG;
            bnphase=BN_FAILED; bnpending=true; bninputoff(); return;
        }
        BNEvent &e=bnevents[bneventcount++];
        e.kind=kind; e.milestone=milestone; e.cn=cn; e.life=life; e.error=bnerror; e.at=bnnow();
    }
    void bncleardisplay()
    {
        // Deliberately does not touch clienthost/connpeer/curpeer or local server.
        loopv(players) if(players[i]) zapplayer(players[i]);
        if(player1) { player1->clientnum=-1; player1->lifesequence=0; player1->clientrole=CR_DEFAULT; }
        bninputoff(); connected=0; clientpassword[0]='\0'; connectrole=CR_DEFAULT; modprotocol=false;
    }
    int bnbackend()
    {
        int status=ob_ws_status(clienthost ? clienthost->socket : 0);
        if(status<0) browsernet_close(-status>=BNE_BOOT && -status<=BNE_VISIBILITY ? -status : BNE_ENET);
        return status;
    }
    bool bnflush()
    {
        if(!clienthost) return false;
        enet_host_flush(clienthost); // ENet's void API cannot expose send failure.
        return bnbackend()>=0;      // Poll the platform's first latched error.
    }
    void bnteardown()
    {
        if(!bnpending || bnparserdepth) return;
        // Only a frame safe point owns logger/actors/peer/host destruction.
        messages.setsize(0); pktlogger.clear();
        if(clienthost) enet_host_destroy(clienthost);
        clienthost=NULL; curpeer=connpeer=NULL; connmillis=connattempts=discmillis=0;
        bncleardisplay(); memset(bnremotes,0,sizeof(bnremotes)); bnmap=false;
        bncn=-1; bnlife=-1; bnstage=0; bnspawnack=false;
        bnpending=false; ++bnc.teardowns;
        if(bneventcount<512) bnrecord(3);
        else { if(!bnerror) bnerror=BNE_BACKLOG; bnphase=BN_FAILED; }
    }
}

EM_JS(void, bn_publish_json, (const char *json), {
    const text=UTF8ToString(json);
    const freeze=(value)=>{if(value && typeof value==='object'){Object.keys(value).forEach(k=>freeze(value[k]));Object.freeze(value);}return value;};
    // Each getter closes over an immutable serialized observation, never C handles.
    Object.defineProperty(window,'outbreakNetworkSnapshot',{
        configurable:true,enumerable:true,writable:false,
        value:()=>freeze(JSON.parse(text))
    });
});
static void bnpublish()
{
    static char json[131072];
    int n=0;
    const char *states[]={"BN_IDLE","BN_OPENING","BN_OPEN","BN_JOINING","BN_ACTIVE","BN_CLOSING","BN_FAILED"};
    vec own=player1 ? player1->o : vec(0,0,0);
    if(!__builtin_isfinite(own.x)||!__builtin_isfinite(own.y)||!__builtin_isfinite(own.z)) { browsernet_close(BNE_SIZE); own=vec(0,0,0); }
#define BN_JSON(...) do { int wrote=snprintf(json+n,sizeof(json)-n,__VA_ARGS__); if(wrote<0 || wrote>=int(sizeof(json)-n)) { browsernet_close(BNE_BACKLOG); return; } n+=wrote; } while(0)
    BN_JSON("{\"schema_version\":1,\"profile\":\"network-client\",\"state\":\"%s\",\"error\":%d,\"map_name\":\"%s\",\"map_revision\":%d,\"own\":{\"cn\":%d,\"life\":%d,\"state\":%d,\"position\":[%.9g,%.9g,%.9g]},\"remotes\":[", states[bnphase],bnerror,ob_browser_map::receipt_name(bnmap),ob_browser_map::receipt_revision(bnmap),player1?player1->clientnum:-1,bnlife,player1?player1->state:CS_SPECTATE,own.x,own.y,own.z);
    bool comma=false;
    loopi(MAXCLIENTS) if(bnremotes[i].valid)
    {
        BNRemote &r=bnremotes[i];
        BN_JSON("%s{\"cn\":%d,\"life\":%d,\"position\":[%.9g,%.9g,%.9g],\"parse_count\":%d,\"last_parse_ms\":%.3f}",comma?",":"",r.cn,r.life,r.x,r.y,r.z,r.count,r.at); comma=true;
    }
    BN_JSON("],\"counters\":{");
#define BN_COUNT(key) BN_JSON("\"" #key "\":%u,",bnc.key)
    BN_COUNT(begin_calls); BN_COUNT(repeated_begin); BN_COUNT(frame_calls); BN_COUNT(frame_advances); BN_COUNT(ws_frames);
    BN_COUNT(service_calls); BN_COUNT(game_events); BN_COUNT(receive_packets); BN_COUNT(send_queued); BN_COUNT(send_rejected);
    BN_COUNT(owned_local_attempts); BN_COUNT(milestones); BN_COUNT(life_observations); BN_COUNT(position_receipts);
    BN_COUNT(remove_receipts); BN_COUNT(map_receipts); BN_COUNT(join_timeouts); BN_COUNT(spawn_requests); BN_COUNT(spawn_acknowledgments);
    BN_JSON("\"teardowns\":%u},\"coverage\":\"owned client send/local receive paths only; main/local server unobserved\",\"events\":[",bnc.teardowns);
    loopi(bneventcount)
    {
        BNEvent &e=bnevents[i];
        BN_JSON("%s{\"kind\":%d,\"milestone\":%d,\"cn\":%d,\"life\":%d,\"error\":%d,\"at_ms\":%.3f}",i?",":"",e.kind,e.milestone,e.cn,e.life,e.error,e.at);
    }
    BN_JSON("]}"); bn_publish_json(json);
#undef BN_COUNT
#undef BN_JSON
}
BrowserNetState browsernet_state() { return bnphase; }
int browsernet_error() { return bnerror; }
void browsernet_close(int reason)
{
    if(reason && !bnerror) bnerror=reason>=BNE_BOOT && reason<=BNE_VISIBILITY ? reason : BNE_ENET;
    if(bnterminal()) { if(bnerror) bnphase=BN_FAILED; return; }
    bnphase=bnerror ? BN_FAILED : BN_CLOSING; bncloseat=bnnow(); bnpending=true;
    bninputoff(); bnrecord(2);
    // No packet logger, actor, host or peer is destroyed on this stack.
}
void browsernet_begin()
{
    ++bnc.begin_calls;
    if(bnconsumed || bnterminal()) { ++bnc.repeated_begin; return; }
    bnconsumed=true; bncleardisplay(); gamemode=GMODE_DEATHMATCH; watchingdemo=false; editmode=false;
    if(sk || clienthost || curpeer || connpeer) { browsernet_close(BNE_BOOT); bnpublish(); return; }
    bnphase=BN_OPENING;
    clienthost=enet_host_create(NULL,1,3,0,0);
    if(!clienthost)
    {
        int status=ob_ws_status(0);
        browsernet_close(status<0 && -status>=BNE_BOOT && -status<=BNE_VISIBILITY ? -status : BNE_OPEN);
    }
    bnrecord(0); bnpublish();
}
void browsernet_frame(unsigned frameId)
{
    ++bnc.frame_calls;
    if(bnseenframe && frameId==bnframeid) return;
    bnseenframe=true; bnframeid=frameId; bneventsleft=64; ++bnc.frame_advances;
    ob_ws_frame(frameId); ++bnc.ws_frames;
    if(clienthost && !bnterminal())
    {
        int status=bnbackend();
        if(bnphase==BN_OPENING && status==1)
        {
            bnphase=BN_OPEN; bnjoinat=bnnow(); bnrecord(0);
            ENetAddress address;
            address.host=ENET_HOST_TO_NET_32(0x7f000001); address.port=29863;
            connpeer=enet_host_connect(clienthost,&address,3,0);
            if(!connpeer) browsernet_close(BNE_ENET);
            else { bnphase=BN_JOINING; connmillis=totalmillis; connattempts=0; bnflush(); }
        }
        if(bnphase==BN_JOINING && bnnow()-bnjoinat>=15000) { ++bnc.join_timeouts; browsernet_close(BNE_DEADLINE); }
    }
    if(bnpending && !bnparserdepth)
    {
        if(!bnerror && curpeer && clienthost)
        {
            if(!bndiscsent) { bndiscsent=true; enet_peer_disconnect(curpeer,DISC_BECAUSE); bnflush(); }
            if(!bnerror && !bndrained && bnnow()-bncloseat<2000) { gets2c(); bnpublish(); return; }
        }
        bnteardown();
    }
    bnpublish();
}
void browsernet_game_observed(unsigned milestone,int cn,int lifeSequence)
{
    if(bnterminal()) return;
    if(!curpeer || curpeer->host!=clienthost || cn<0 || cn>=MAXCLIENTS) { browsernet_close(BNE_MILESTONE); return; }
    if(milestone==4 && lifeSequence!=player1->lifesequence) { browsernet_close(BNE_MILESTONE); return; }
    if(bnphase==BN_ACTIVE && milestone==4 && cn==bncn && lifeSequence>=0 && bnspawnack)
    {
        bnspawnack=false; bnlife=lifeSequence; ++bnc.life_observations; bnrecord(1,4,cn,lifeSequence); return;
    }
    if(bnphase!=BN_JOINING || milestone!=unsigned(bnstage+1) || milestone>4 || (bnstage && cn!=bncn) || (milestone<4 && lifeSequence!=-1)) { browsernet_close(BNE_MILESTONE); return; }
    if(milestone==4 && (!bnmap || !bnspawnack || lifeSequence<0 || player1->clientnum!=cn || player1->state!=CS_ALIVE)) { browsernet_close(bnmap?BNE_MILESTONE:BNE_MAP); return; }
    bncn=cn; bnstage=milestone; ++bnc.milestones; bnrecord(1,milestone,cn,lifeSequence);
    if(milestone==4) { bnspawnack=false; bnlife=lifeSequence; bnphase=BN_ACTIVE; }
}
bool browsernet_spawn_expected()
{
    if(bnterminal()) return false;
    if(!ob_browser_map::spawn_matches(bnmap,getclientmap(),hdr.maprevision,maploaded,gamemode,GMODE_DEATHMATCH))
    { browsernet_close(BNE_MAP); return false; }
    if(!curpeer || player1->clientnum!=bncn || (bnphase!=BN_ACTIVE && (bnphase!=BN_JOINING || bnstage!=3))) { browsernet_close(BNE_MILESTONE); return false; }
    bnspawnack=false;
    return true;
}
bool browsernet_spawn_request_allowed()
{
    return player1 && curpeer && clienthost && curpeer->host==clienthost &&
      ob_browser_map::spawn_matches(bnmap,getclientmap(),hdr.maprevision,maploaded,gamemode,GMODE_DEATHMATCH) &&
      bncn>=0 && bncn<MAXCLIENTS && player1->clientnum==bncn &&
      ((bnphase==BN_JOINING && bnstage==3) || (bnphase==BN_ACTIVE && bnstage==4));
}
bool browsernet_message_allowed(int type)
{
    if(bnterminal() || (bnphase!=BN_JOINING && bnphase!=BN_ACTIVE)) return false;
    if(type==SV_TRYSPAWN) return browsernet_spawn_request_allowed();
    switch(type)
    {
        case SV_SENDMAP: case SV_RECVMAP: case SV_REMOVEMAP: case SV_LISTDEMOS: case SV_GETDEMO: case SV_SENDDEMO:
        case SV_DEMOPLAYBACK: case SV_DEMOCHECKSUM: case SV_DEMOSIGNATURE: case SV_EDITMODE: case SV_EDITENT:
        case SV_EDITXY: case SV_EDITARCH: case SV_EDITBLOCK: case SV_EDITD: case SV_EDITE: case SV_NEWMAP: return false;
    }
    if(bnphase==BN_ACTIVE) return true;
    return type==SV_SERVINFO_RESPONSE || type==SV_CONNECT || type==SV_MAPIDENT || type==SV_SPAWN || type==SV_PING || type==SV_PONG;
}
bool browsernet_parser_busy() { return bnparserdepth>0; }
void browsernet_local_attempt() { ++bnc.owned_local_attempts; browsernet_close(BNE_ENET); }
void browsernet_position_observed(int cn,int lifeSequence,float x,float y,float z)
{
    if(bnterminal()) return;
    if(cn<0 || cn>=MAXCLIENTS || lifeSequence<0 || !__builtin_isfinite(x)||!__builtin_isfinite(y)||!__builtin_isfinite(z)) { browsernet_close(BNE_MILESTONE); return; }
    BNRemote &r=bnremotes[cn]; r.valid=true; r.cn=cn; r.life=lifeSequence; r.x=x; r.y=y; r.z=z; ++r.count; r.at=bnnow(); ++bnc.position_receipts;
}
void browsernet_remove_observed(int cn)
{
    if(cn>=0 && cn<MAXCLIENTS) { bnremotes[cn]=BNRemote(); ++bnc.remove_receipts; }
}
void browsernet_map_observed(const char *name,int revision)
{
    if(bnterminal()) return;
    if(!ob_browser_map::observed_matches(name,revision,getclientmap(),hdr.maprevision,maploaded,gamemode,GMODE_DEATHMATCH))
    { browsernet_close(BNE_MAP); return; }
    bnmap=true; ++bnc.map_receipts;
}
#endif

void abortconnect()
{
#if defined(OUTBREAK_NETWORK_CLIENT) && defined(__EMSCRIPTEN__) && !defined(STANDALONE)
    browsernet_close(BNE_ENET); return;
#endif
    if(!connpeer) return;
    clientpassword[0] = '\0';
    connectrole = CR_DEFAULT;
    if(connpeer->state!=ENET_PEER_STATE_DISCONNECTED) enet_peer_reset(connpeer);
    connpeer = NULL;
}

void connectserv_(const char *servername, int serverport = 0, const char *password = NULL, int role = CR_DEFAULT)
{
#if defined(OUTBREAK_NETWORK_CLIENT) && defined(__EMSCRIPTEN__) && !defined(STANDALONE)
    browsernet_close(BNE_TARGET); return;
#endif
    if(serverport <= 0) serverport = CUBE_DEFAULT_SERVER_PORT;
    if(watchingdemo) enddemoplayback();

    if(connpeer)
    {
        conoutf("aborting connection attempt");
        abortconnect();
    }
    connectrole = role;
    copystring(clientpassword, password ? password : "");
    ENetAddress address;
    address.port = serverport;

    if(servername)
    {
        addserver(servername, serverport, 0);
        conoutf("\f2attempting to %sconnect to \f5%s\f4:%d\f2", role==CR_DEFAULT?"":"\f8admin\f2", servername, serverport);
        if(!resolverwait(servername, &address))
        {
            conoutf("\f2could \f3not resolve\f2 server \f5%s\f2", servername);
            clientpassword[0] = '\0';
            connectrole = CR_DEFAULT;
            return;
        }
    }
    else
    {
        conoutf("\f2attempting to connect over \f1LAN\f2");
        address.host = ENET_HOST_BROADCAST;
    }

    if(!clienthost)
        clienthost = enet_host_create(NULL, 2, 3, 0, 0);

    if(clienthost)
    {
        connpeer = enet_host_connect(clienthost, &address, 3, 0);
        enet_host_flush(clienthost);
        connmillis = totalmillis;
        connattempts = 0;
        if(!m_mp(gamemode)) gamemode = GMODE_TEAMDEATHMATCH;
    }
    else
    {
        conoutf("\f2could \f3not connect\f2 to server");
        clientpassword[0] = '\0';
        connectrole = CR_DEFAULT;
    }
}

void connectserv(char *servername, int *serverport, char *password)
{
#if defined(OUTBREAK_NETWORK_CLIENT) && defined(__EMSCRIPTEN__) && !defined(STANDALONE)
    browsernet_close(BNE_TARGET); return;
#endif
    if(sk)
    {
        modprotocol = false;
        connectserv_(servername, *serverport, password);
    }else{
        extern char *aaconnect;// assaultcube://example.org[:28763][/][?[port=28763][&password=secret]]
        string cp1, cp2, cp3, cpc;
        formatstring(cp1)("assaultcube://%s",servername);
        if(serverport)formatstring(cp2)(":%d",*serverport);
        if(password)formatstring(cp3)("/?password=%s",password);
        formatstring(cpc)("%s%s%s", cp1, cp2, cp3);
        aaconnect = newstring(cpc);
        hudoutf("\f5.. \f2waiting \f4for \fUauth\f5entication ..");
        extern gmenu *curmenu;
        if(!curmenu) showmenu("enter password");
    }
}
COMMANDN(connect, connectserv, "sis");

void connectadmin(char *servername, int *serverport, char *password)
{
#if defined(OUTBREAK_NETWORK_CLIENT) && defined(__EMSCRIPTEN__) && !defined(STANDALONE)
    browsernet_close(BNE_TARGET); return;
#endif
    modprotocol = false;
    connectserv_(servername, *serverport, password, CR_ADMIN);
}
COMMAND(connectadmin, "sis");

void lanconnect()
{
#if defined(OUTBREAK_NETWORK_CLIENT) && defined(__EMSCRIPTEN__) && !defined(STANDALONE)
    browsernet_close(BNE_TARGET); return;
#endif
    modprotocol = false;
    connectserv_(NULL);
}
COMMAND(lanconnect, "");

void modconnectserv(char *servername, int *serverport, char *password)
{
#if defined(OUTBREAK_NETWORK_CLIENT) && defined(__EMSCRIPTEN__) && !defined(STANDALONE)
    browsernet_close(BNE_TARGET); return;
#endif
    modprotocol = true;
    connectserv_(servername, *serverport, password);
}
COMMANDN(modconnect, modconnectserv, "sis");

void modconnectadmin(char *servername, int *serverport, char *password)
{
#if defined(OUTBREAK_NETWORK_CLIENT) && defined(__EMSCRIPTEN__) && !defined(STANDALONE)
    browsernet_close(BNE_TARGET); return;
#endif
    modprotocol = true;
    connectserv_(servername, *serverport, password, CR_ADMIN);
}
COMMAND(modconnectadmin, "sis");

void modlanconnect()
{
#if defined(OUTBREAK_NETWORK_CLIENT) && defined(__EMSCRIPTEN__) && !defined(STANDALONE)
    browsernet_close(BNE_TARGET); return;
#endif
    modprotocol = true;
    connectserv_(NULL);
}
COMMAND(modlanconnect, "");

void disconnect(int onlyclean, int async)
{
#if defined(OUTBREAK_NETWORK_CLIENT) && defined(__EMSCRIPTEN__) && !defined(STANDALONE)
    browsernet_close(onlyclean ? BNE_NONE : BNE_CLOSED); return;
#endif
    bool cleanup = onlyclean!=0;
    if(curpeer)
    {
        if(!discmillis)
        {
            enet_peer_disconnect(curpeer, DISC_BECAUSE);
            enet_host_flush(clienthost);
            discmillis = totalmillis;
        }
        if(curpeer->state!=ENET_PEER_STATE_DISCONNECTED)
        {
            if(async) return;
            enet_peer_reset(curpeer);
        }
        curpeer = NULL;
        discmillis = 0;
        connected = 0;
        conoutf("disconnected");
        cleanup = true;
    }

    if(cleanup)
    {
        player1->clientnum = -1;
        player1->lifesequence = 0;
        player1->clientrole = CR_DEFAULT;
        lastpm = -1;
        kickallbots();
        loopv(players) zapplayer(players[i]);
        clearvote();
        audiomgr.clearworldsounds(false);
        localdisconnect();
    }
    if(!onlyclean) localconnect();
    exechook(HOOK_SP_MP, "onDisconnect", "%d", -1);
}

void trydisconnect()
{
#if defined(OUTBREAK_NETWORK_CLIENT) && defined(__EMSCRIPTEN__) && !defined(STANDALONE)
    browsernet_close(BNE_NONE); return;
#endif
    if(connpeer)
    {
        conoutf("aborting connection attempt");
        abortconnect();
        return;
    }
    if(!curpeer)
    {
        conoutf("not connected");
        return;
    }
    conoutf("attempting to disconnect...");
    disconnect(0, !discmillis);
}
COMMANDN(disconnect, trydisconnect, "");

// core game function: ingame chat

void _toserver(char *text, int msg, int msgt)
{
    bool toteam = text && text[0] == '%' && (m_teammode || team_isspect(player1->team));
    if(!toteam && text[0] == '%' && strlen(text) > 1) text++; // convert team-text to normal-text if no team-mode is active
    if(toteam) text++;
    filtertext(text, text, FTXT__CHAT);
    if(servstate.mastermode == MM_MATCH && servstate.matchteamsize && !team_isactive(player1->team) && !(player1->team == TEAM_SPECT && player1->clientrole == CR_ADMIN)) toteam = true; // spect chat
    if(*text) addmsg(toteam ? msgt : msg, "rs", text);
}

void toserver(char *text)
{
    _toserver(text, SV_TEXT, SV_TEAMTEXT);
}
COMMANDN(say, toserver, "c");

void toserverme(char *text)
{
    _toserver(text, SV_TEXTME, SV_TEAMTEXTME);
}
COMMANDN(me, toserverme, "c");

void pm(char *text)
{
    char *msg;
    int cn = (int) strtol(text, &msg, 10);
    if(msg != text && getclient(cn))
    {
        filtertext(msg, msg, FTXT__CHAT | FTXT_CROPWHITE_LEAD);
        if(*msg) addmsg(SV_TEXTPRIVATE, "ris", cn, msg);
    }
    else conoutf("\f3pm: invalid client number specified");
}
COMMAND(pm, "c");

void echo(char *text)
{
    char *b, *s = strtok_r(text, "\n", &b);
    do
    {
        conoutf("%s", s ? s : "");
        s = strtok_r(NULL, "\n", &b);
    }
    while(s);
}
COMMAND(echo, "c");

VARP(allowhudechos, 0, 1, 1);

void hudecho(char *text)
{
    char *b, *s = strtok_r(text, "\n", &b);
    void (*outf)(const char *s, ...) = allowhudechos ? hudoutf : conoutf;
    do
    {
        outf("%s", s ? s : "");
        s = strtok_r(NULL, "\n", &b);
    }
    while(s);
}
COMMAND(hudecho, "c");

void whereami()
{
    conoutf("you are at (%.2f,%.2f)", player1->o.x, player1->o.y);
}
COMMAND(whereami, "");

void current_version(char *text)
{
    int version = atoi(text);
    if (version && AC_VERSION<version)
    {
        hudoutf("\f3YOUR VERSION OF ASSAULTCUBE IS OUTDATED!");
        conoutf("\f3YOU MUST UPDATE ASSAULTCUBE\nplease visit \f2http://assault.cubers.net \f3for more information");
    }
}
COMMAND(current_version, "s");

void cleanupclient()
{
#if defined(OUTBREAK_NETWORK_CLIENT) && defined(__EMSCRIPTEN__) && !defined(STANDALONE)
    browsernet_close(BNE_NONE); return;
#endif
    abortconnect();
    disconnect(1);
    if(clienthost)
    {
        enet_host_destroy(clienthost);
        clienthost = NULL;
    }
}

// collect c2s messages conveniently

vector<uchar> messages;

void addmsg(int type, const char *fmt, ...)
{
#if defined(OUTBREAK_NETWORK_CLIENT) && defined(__EMSCRIPTEN__) && !defined(STANDALONE)
    if(!browsernet_message_allowed(type)) return;
    if(type==SV_TRYSPAWN)
    {
        enet_uint32 at=enet_time_get();
        if(bnhasspawnrequest && enet_uint32(at-bnlastspawnrequest)<1000) return;
        bnhasspawnrequest=true; bnlastspawnrequest=at; ++bnc.spawn_requests;
    }
#endif
    static uchar buf[MAXTRANS];
    ucharbuf p(buf, MAXTRANS);
    putint(p, type);
    int numi = 1, nums = 0;
    bool reliable = false;
    if(fmt)
    {
        va_list args;
        va_start(args, fmt);
        while(*fmt) switch(*fmt++)
        {
            case 'r': reliable = true; break;
            case 'v':
            {
                int n = va_arg(args, int);
                int *v = va_arg(args, int *);
                loopi(n) putint(p, v[i]);
                numi += n;
                break;
            }

            case 'i':
            {
                int n = isdigit(*fmt) ? *fmt++-'0' : 1;
                loopi(n) putint(p, va_arg(args, int));
                numi += n;
                break;
            }
            case 'a':
            {
                int n = isdigit(*fmt) ? *fmt++-'0' : 1;
                loopi(n) putaint(p, va_arg(args, int));
                numi += n;
                break;
            }
            case 's':
            {
                const char *t = va_arg(args, const char *);
                sendstring(t, p);
                nums++;
                break;
            }
        }
        va_end(args);
    }
    int num = nums?0:numi, msgsize = msgsizelookup(type);
    if(msgsize && num!=msgsize) { fatal("inconsistent msg size for %d (%d != %d)", type, num, msgsize); }
    int len = p.length();
    messages.add(len&0xFF);
    messages.add((len>>8)|(reliable ? 0x80 : 0));
    loopi(len) messages.add(buf[i]);
}

static int lastupdate = -1000, lastping = 0;
bool sendmapidenttoserver = false;

#if defined(OUTBREAK_NETWORK_CLIENT) && defined(__EMSCRIPTEN__) && !defined(STANDALONE)
ENetPacket *browsernet_take_packet(packetbuf &p)
{
    ENetPacket *packet=p.finalize();
    p.packet=NULL; p.buf=NULL; // finalize alone does NOT transfer packetbuf ownership.
    return packet;
}
#endif

void sendpackettoserv(int chan, ENetPacket *packet)
{
#if defined(OUTBREAK_NETWORK_CLIENT) && defined(__EMSCRIPTEN__) && !defined(STANDALONE)
    if(!packet) return;
    if(!curpeer || curpeer->host!=clienthost || bnterminal() || chan<0 || chan>1 || (chan==0 && bnphase!=BN_ACTIVE))
    {
        if(!curpeer) ++bnc.owned_local_attempts;
        ++bnc.send_rejected;
        if(!packet->referenceCount) enet_packet_destroy(packet);
        return;
    }
    if(chan==1)
    {
        ucharbuf inspect(packet->data,int(packet->dataLength));
        int type=getint(inspect); // Use the native decoder; never a second protocol parser.
        if(inspect.overread() || !browsernet_message_allowed(type))
        { ++bnc.send_rejected; if(!packet->referenceCount) enet_packet_destroy(packet); return; }
    }
    if(enet_peer_send(curpeer,chan,packet)<0)
    {
        ++bnc.send_rejected;
        if(!packet->referenceCount) enet_packet_destroy(packet);
        browsernet_close(BNE_ENET);
    }
    else ++bnc.send_queued;
#else
    if(curpeer) enet_peer_send(curpeer, chan, packet);
    else localclienttoserver(chan, packet);
#endif
}

#if defined(OUTBREAK_NETWORK_CLIENT) && defined(__EMSCRIPTEN__) && !defined(STANDALONE)
bool browsernet_acknowledge_spawn(int life,int gun)
{
    if(bnterminal() || !curpeer) return false;
    unsigned queued=bnc.send_queued;
    packetbuf ack(32,ENET_PACKET_FLAG_RELIABLE);
    putint(ack,SV_SPAWN); putint(ack,life); putint(ack,gun);
    sendpackettoserv(1,browsernet_take_packet(ack));
    if(bnterminal() || bnc.send_queued!=queued+1) { browsernet_close(BNE_ENET); return false; }
    if(!bnflush()) return false;
    bnspawnack=true; ++bnc.spawn_acknowledgments;
    return true;
}
#endif

void c2skeepalive()
{
#if defined(OUTBREAK_NETWORK_CLIENT) && defined(__EMSCRIPTEN__) && !defined(STANDALONE)
    gets2c(); // Shared event dispatch/budget and explicit error path, including keepalive.
#else
    if(clienthost && (curpeer || connpeer)) enet_host_service(clienthost, NULL, 0);
#endif
}

extern string masterpwd;
bool sv_pos = true;

void c2sinfo(playerent *d)                  // send update to the server
{
#if defined(OUTBREAK_NETWORK_CLIENT) && defined(__EMSCRIPTEN__) && !defined(STANDALONE)
    if(!curpeer || bnterminal()) return;
#endif
    if(d->clientnum<0) return;              // we haven't had a welcome message from the server yet
    if(totalmillis-lastupdate<40) return;    // don't update faster than 25fps

#if defined(OUTBREAK_NETWORK_CLIENT) && defined(__EMSCRIPTEN__) && !defined(STANDALONE)
    if(bnphase==BN_ACTIVE && (d->state==CS_ALIVE || d->state==CS_EDITING))
#else
    if(d->state==CS_ALIVE || d->state==CS_EDITING)
#endif
    {
        ASSERT(!(d->crouching && d->onladder)); // onladder is never set while crouching - and we're going to rely on it ;)
        ASSERT(!(d->move < -1 || d->move > 1 || d->strafe < -1 || d->strafe > 1));
        packetbuf q(100);
        int cn = d->clientnum,
            x = (int)(d->o.x*DMF + 0.5f),          // quantize coordinates to 1/16th of a cube, between 1 and 3 bytes
            y = (int)(d->o.y*DMF + 0.5f),
            z = (int)floorf((d->o.z - d->eyeheight)*DMF + 0.5f),
            zsign = z < 0 ? 1 : 0,
            ya = encodeyaw(d->yaw),
            pi = encodepitch(d->pitch),
            dx = (int)floorf(d->vel.x*DVELF + 0.5f),
            dy = (int)floorf(d->vel.y*DVELF + 0.5f),
            dz = (int)floorf(d->vel.z*DVELF + 0.5f);
        int f = (d->strafe + 4 + d->move * 3 + (d->onladder ? 9 : 0) + (d->crouching ? 18 : 0))     // pack 6 bit into 5 with ternary logic :)
                 | (((int)d->scoping)<<5) | ((d->lifesequence&1)<<6) | (((int)d->onfloor)<<7) | (((int)d->jumpd)<<8) | (((int)(dx||dy||dz))<<9) | (zsign << 10);  // number of used bits: FLAGBITS
        int usefactor = sfactor < 7 ? 7 : sfactor;
        if(zsign) z = -z;
        if(cn >= 0 && cn < 32 &&
            usefactor <= 7 + 3 &&       // map size 7..10
            !((x | y) & ~((1 << (usefactor + 4)) - 1)) &&
            z >= -2047 && z <= 2047 &&
            dx >= -8 && dx <= 7 &&
            dy >= -8 && dy <= 7 &&
            dz >= -8 && dz <= 7)
        { // compact POS packet
            bitbuf<packetbuf> b(q);
            putint(q, SV_POSC + usefactor - 7);
            b.putbits(5, cn);
            b.putbits(usefactor + 4, x);
            b.putbits(usefactor + 4, y);
            b.putbits(YAWBITS, ya);
            b.putbits(PITCHBITS, pi);
            b.putbits(FLAGBITS, f);
            if(f & (1 << 9)) // hasvel
            {
                b.putbits(4, dx + 8);
                b.putbits(4, dy + 8);
                b.putbits(4, dz + 8);
            }
            int s = (b.rembits() - 1 + 8) % 8; // z is encoded with 3..10 bits minimum (fitted to byte boundaries), or full 11 bits if necessary
            if(s < 3) s += 8;
            if(z >= (1 << s)) s = 11;
            b.putbits(1, s == 11 ? 1 : 0);
            b.putbits(s, z);
        }
        else
        { // classic POS packet
            putint(q, SV_POS);
            putint(q, d->clientnum);
            putuint(q, x);
            putuint(q, y);
            putuint(q, z);
            putuintn(q, (ya << (uint64_t)(FLAGBITS + PITCHBITS)) | (pi << FLAGBITS) | f, (YAWBITS + PITCHBITS + FLAGBITS + 7) / 8);
            if(f & (1<<9))
            {
                putint(q, dx);
                putint(q, dy);
                putint(q, dz);
            }
        }
#if defined(OUTBREAK_NETWORK_CLIENT) && defined(__EMSCRIPTEN__) && !defined(STANDALONE)
        sendpackettoserv(0, browsernet_take_packet(q));
#else
        sendpackettoserv(0, q.finalize());
#endif
        d->jumpd = false;
    }

    if(sendmapidenttoserver || messages.length() || totalmillis-lastping>250)
    {
        packetbuf p(MAXTRANS);

        if(sendmapidenttoserver) // new map
        {
            p.reliable();
            putint(p, SV_MAPIDENT);
            putint(p, maploaded);
            putint(p, hdr.maprevision);
            sendmapidenttoserver = false;
        }
        int i = 0;
        while(i < messages.length()) // send messages collected during the previous frames
        {
            int len = messages[i] | ((messages[i+1]&0x7F)<<8);
            if(p.remaining() < len) break;
            if(messages[i+1]&0x80) p.reliable();
            p.put(&messages[i+2], len);
            i += 2 + len;
        }
        messages.remove(0, i);
        if(totalmillis-lastping>250)
        {
            putint(p, SV_PING);
            putint(p, totalmillis);
            lastping = totalmillis;
        }
#if defined(OUTBREAK_NETWORK_CLIENT) && defined(__EMSCRIPTEN__) && !defined(STANDALONE)
        if(p.length()) sendpackettoserv(1, browsernet_take_packet(p));
#else
        if(p.length()) sendpackettoserv(1, p.finalize());
#endif
    }

#if defined(OUTBREAK_NETWORK_CLIENT) && defined(__EMSCRIPTEN__) && !defined(STANDALONE)
    if(clienthost) bnflush();
#else
    if(clienthost) enet_host_flush(clienthost);
#endif
    lastupdate = totalmillis;
}

int getbuildtype()
{
    return (isbigendian() ? 0x80 : 0 )|(adler((unsigned char *)guns, sizeof(guns)) % 31 << 8)|
        #ifdef WIN32
            0x40 |
        #endif
        #ifdef __APPLE__
            0x20 |
        #endif
        #ifdef _DEBUG
            0x08 |
        #endif
        #ifdef __GNUC__
            0x04 |
        #endif
            0;
}

void sendintro()
{
    packetbuf p(MAXTRANS, ENET_PACKET_FLAG_RELIABLE);
    putint(p, SV_CONNECT);
    putint(p, AC_VERSION);
    putint(p, getbuildtype());
    sendstring(player1->name, p);
    sendstring(genpwdhash(player1->name, clientpassword, sessionid), p);
    sendstring(!lang || strlen(lang) != 2 ? "" : lang, p);
    putint(p, connectrole);
    clientpassword[0] = '\0';
    connectrole = CR_DEFAULT;
    putint(p, player1->nextprimweap->type);
    loopi(2) putint(p, player1->skin(i));
    putint(p, player1->maxroll);
    putint(p, player1->maxrolleffect);
    putint(p, player1->ffov);
    putint(p, player1->scopefov);
#if defined(OUTBREAK_NETWORK_CLIENT) && defined(__EMSCRIPTEN__) && !defined(STANDALONE)
    sendpackettoserv(1, browsernet_take_packet(p));
#else
    sendpackettoserv(1, p.finalize());
#endif
}

void gets2c()           // get updates from the server
{
#if defined(OUTBREAK_NETWORK_CLIENT) && defined(__EMSCRIPTEN__) && !defined(STANDALONE)
    if(bnparserdepth) return; // Map/control keepalive cannot recursively evict the current logger payload.
    if(!clienthost || !bnseenframe || (!curpeer && !connpeer) || bnphase==BN_FAILED) return;
    if(bnbackend()<0) return;
    if(connpeer && totalmillis/3000 > connmillis/3000)
    {
        connmillis=totalmillis; ++connattempts;
        if(connattempts>3) { browsernet_close(BNE_DEADLINE); return; }
    }
    while(clienthost && bneventsleft && bnphase!=BN_FAILED)
    {
        ENetEvent event; ++bnc.service_calls;
        int result=enet_host_service(clienthost,&event,0);
        if(result<0) { if(bnbackend()>=0) browsernet_close(BNE_ENET); return; }
        if(bnbackend()<0) { if(result>0 && event.type==ENET_EVENT_TYPE_RECEIVE) enet_packet_destroy(event.packet); return; }
        if(!result) return;
        --bneventsleft; ++bnc.game_events;
        switch(event.type)
        {
            case ENET_EVENT_TYPE_CONNECT:
                if(bnterminal()) break;
                if(event.peer!=connpeer || event.peer->host!=clienthost) { browsernet_close(BNE_ENET); return; }
                bncleardisplay(); // Host and the real event peer survive display cleanup.
                curpeer=event.peer; connpeer=NULL; connected=1; throttle();
                break;
            case ENET_EVENT_TYPE_RECEIVE:
                if(event.peer!=curpeer || event.channelID>1 || bnterminal())
                {
                    enet_packet_destroy(event.packet);
                    if(!bnterminal()) browsernet_close(BNE_TARGET);
                    break;
                }
                pktlogger.queue(event.packet); ++bnc.receive_packets;
                ++bnparserdepth;
                servertoclient(event.channelID,event.packet->data,int(event.packet->dataLength));
                --bnparserdepth;
                // Logger owns event.packet. It must survive even a nested close.
                if(bnterminal())
                {
                    if(bnerror) bnteardown(); // Parser has returned; safe even if main canceled.
                    return;
                }
                break;
            case ENET_EVENT_TYPE_DISCONNECT:
                if(event.peer!=curpeer && event.peer!=connpeer) { browsernet_close(BNE_ENET); return; }
                if(bnphase==BN_CLOSING) bndrained=true;
                else browsernet_close(BNE_CLOSED);
                return;
            default: break;
        }
    }
#else
    ENetEvent event;
    if(!clienthost || (!curpeer && !connpeer)) return;
    if(connpeer && totalmillis/3000 > connmillis/3000)
    {
        conoutf("attempting to connect...");
        connmillis = totalmillis;
        ++connattempts;
        if(connattempts > 3)
        {
            conoutf("\f3could not connect to server");
            abortconnect();
            return;
        }
    }
    while(clienthost!=NULL && enet_host_service(clienthost, &event, 0)>0)
    switch(event.type)
    {
        case ENET_EVENT_TYPE_CONNECT:
            disconnect(1);
            curpeer = connpeer;
            connpeer = NULL;
            connected = 1;
            conoutf("connected to server");
            exechook(HOOK_SP_MP, "onConnect", "%d", -1);
            throttle();
            if(editmode) toggleedit(true);
            break;

        case ENET_EVENT_TYPE_RECEIVE:
        {
            extern packetqueue pktlogger;
            pktlogger.queue(event.packet);

            if(discmillis) conoutf("attempting to disconnect...");
            else servertoclient(event.channelID, event.packet->data, (int)event.packet->dataLength);
            // destroyed in logger
            //enet_packet_destroy(event.packet);
            break;
        }

        case ENET_EVENT_TYPE_DISCONNECT:
        {
            if(event.peer==connpeer)
            {
                conoutf("\f3could not connect to server");
                abortconnect();
            }
            else
            {
                if(!discmillis || event.data) conoutf("\f3server network error, disconnecting (%s) ...", disc_reason(event.data));
                disconnect();
            }
            return;
        }

        default:
            break;
    }
#endif
}

// sendmap/getmap commands, should be replaced by more intuitive map downloading

vector<char *> securemaps;

COMMANDF(resetsecuremaps, "", () { securemaps.deletearrays(); });
COMMANDF(securemap, "s", (char *map) { if(map) securemaps.add(newstring(map)); });

bool securemapcheck(const char *map, bool msg)
{
    if(strstr(map, "maps/")==map || strstr(map, "maps\\")==map) map += strlen("maps/");
    loopv(securemaps) if(!strcmp(securemaps[i], map))
    {
        if(msg)
        {
            conoutf("\f3Map \f4%s\f3 is secured. This means you CAN'T send, receive or overwrite it.", map);
            if(curpeer)
            {
                conoutf("\f3If you get this error often, you (or the server) may be running an outdated game.");
                conoutf("\f3You can check for updates at \f1http://assault.cubers.net/download.html");
            }
        }
        return true;
    }
    return false;
}

void sendmap(char *mapname)
{
#if defined(OUTBREAK_NETWORK_CLIENT) && defined(__EMSCRIPTEN__) && !defined(STANDALONE)
    browsernet_close(BNE_TARGET); return;
#endif
    if(!*mapname) mapname = getclientmap();
    if(securemapcheck(mapname)) return;
    if(gamemode == GMODE_COOPEDIT && !strcmp(getclientmap(), mapname)) save_world(mapname, true, false); // skip optimisations, don't add undos

    int mapsize, cfgsize, cfgsizegz, revision;
    uchar *mapdata = readmap(path(mapname), &mapsize, &revision);
    if(!mapdata) return;
    uchar *cfgdata = readmcfggz(path(mapname), &cfgsize, &cfgsizegz);
    if(!cfgdata) { cfgsize = 0; cfgsizegz = 0; }

    packetbuf p(MAXTRANS + mapsize + cfgsizegz, ENET_PACKET_FLAG_RELIABLE);

    putint(p, SV_SENDMAP);
    sendstring(mapname, p);
    putint(p, mapsize);
    putint(p, cfgsize);
    putint(p, cfgsizegz);
    putint(p, revision);
    if(MAXMAPSENDSIZE - p.length() < mapsize + cfgsizegz || cfgsize > MAXCFGFILESIZE)
    {
        conoutf("map %s is too large to send", mapname);
        delete[] mapdata;
        if(cfgsize) delete[] cfgdata;
        return;
    }
    p.put(mapdata, mapsize);
    delete[] mapdata;
    if(cfgsizegz)
    {
        p.put(cfgdata, cfgsizegz);
        delete[] cfgdata;
    }

#if defined(OUTBREAK_NETWORK_CLIENT) && defined(__EMSCRIPTEN__) && !defined(STANDALONE)
    sendpackettoserv(2, browsernet_take_packet(p));
#else
    sendpackettoserv(2, p.finalize());
#endif
    conoutf("sending map %s to server...", mapname);
}
COMMAND(sendmap, "s");

void getmap(char *name, char *callback)
{
#if defined(OUTBREAK_NETWORK_CLIENT) && defined(__EMSCRIPTEN__) && !defined(STANDALONE)
    browsernet_close(BNE_TARGET); return;
#endif
    if((!name || !*name)
        || (curpeer && !strcmp(name, getclientmap())) )
    {
        conoutf("requesting map from server...");
        packetbuf p(10, ENET_PACKET_FLAG_RELIABLE);
        putint(p, SV_RECVMAP);
#if defined(OUTBREAK_NETWORK_CLIENT) && defined(__EMSCRIPTEN__) && !defined(STANDALONE)
        sendpackettoserv(2, browsernet_take_packet(p));
#else
        sendpackettoserv(2, p.finalize());
#endif
    }
    else
    {
        requirepackage(PCK_MAP, name);
        if(downloadpackages(false))
        {
            if(callback && *callback) execute(callback);
            conoutf("map %s installed successfully", name);
        }
        else conoutf("\f3map download failed");
    }
}
COMMAND(getmap, "ss");

void deleteservermap(char *mapname)
{
#if defined(OUTBREAK_NETWORK_CLIENT) && defined(__EMSCRIPTEN__) && !defined(STANDALONE)
    browsernet_close(BNE_TARGET); return;
#endif
    const char *name = behindpath(mapname);
    if(!*name || securemapcheck(name)) return;
    addmsg(SV_REMOVEMAP, "rs", name);
}
COMMAND(deleteservermap, "s");

string demosubpath;
void getdemo(int *idx, char *dsp)
{
#if defined(OUTBREAK_NETWORK_CLIENT) && defined(__EMSCRIPTEN__) && !defined(STANDALONE)
    browsernet_close(BNE_TARGET); return;
#endif
    if(!multiplayer(NULL))
    {
        conoutf("\f3Getting demo from server is not available in singleplayer");
        return;
    }
    if(dsp && dsp[0]) formatstring(demosubpath)("%s/", dsp);
    else copystring(demosubpath, "");
    if(*idx<=0) conoutf("getting demo...");
    else conoutf("getting demo %d...", *idx);
    addmsg(SV_GETDEMO, "ri", *idx);
}
COMMAND(getdemo, "is");

void listdemos()
{
#if defined(OUTBREAK_NETWORK_CLIENT) && defined(__EMSCRIPTEN__) && !defined(STANDALONE)
    browsernet_close(BNE_TARGET); return;
#endif
    if(!multiplayer(NULL))
    {
        conoutf("\f3Listing demos from server is not available in singleplayer");
        return;
    }
    conoutf("listing demos...");
    addmsg(SV_LISTDEMOS, "r");
}
COMMAND(listdemos, "");

void shiftgametime(int newmillis)
{
#if defined(OUTBREAK_NETWORK_CLIENT) && defined(__EMSCRIPTEN__) && !defined(STANDALONE)
    browsernet_close(BNE_TARGET); return;
#endif
    if(!watchingdemo) { conoutf("You have to be watching a demo to change game time"); return; }

    newmillis = max(0, newmillis);
    if(newmillis > gametimemaximum) { conoutf("Invalid time specified"); return; }

    int gamemillis = gametimecurrent + (lastmillis - lastgametimeupdate);
    if(newmillis < gamemillis)
    {
        // if rewinding
        if(!curdemofile || !curdemofile[0]) return;
        watchingdemo = false;
        callvote(SA_MAP, curdemofile, "-1", "0");
        skipmillis = newmillis;
    }
    else
    {
        skipmillis = newmillis - gamemillis;
    }
}

void setminutesremaining(char *minutes)
{
    if(*minutes) shiftgametime(gametimemaximum - ATOI(minutes) * 60000);
}
COMMANDN(setmr, setminutesremaining, "s");

void rewinddemo(char *seconds)
{
    int gamemillis = gametimecurrent+(lastmillis-lastgametimeupdate);
    if(*seconds) shiftgametime(gamemillis - ATOI(seconds) * 1000);
}
COMMANDN(rewind, rewinddemo, "s");


COMMANDF(watchingdemo, "", () { intret(watchingdemo); });

COMMANDF(systime, "", () { result(numtime()); });
COMMANDF(timestamp, "", () { result(timestring(true, "%Y %m %d %H %M %S")); });
COMMANDF(datestring, "", () { result(timestring(true, "%c")); });

COMMANDF(timestring, "", ()
{
    const char *res = timestring(true, "%H:%M:%S");
    result(res[0] == '0' ? res + 1 : res);
});

COMMANDF(millis, "", () { intret(totalmillis); });

COMMANDN(setclipboardtext, SDL_SetClipboardText, "s");
