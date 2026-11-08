#ifndef OUTBREAK_BROWSERNET_H
#define OUTBREAK_BROWSERNET_H
#if defined(OUTBREAK_NETWORK_CLIENT) && defined(__EMSCRIPTEN__) && !defined(STANDALONE)
enum BrowserNetState { BN_IDLE, BN_OPENING, BN_OPEN, BN_JOINING, BN_ACTIVE, BN_CLOSING, BN_FAILED };
enum BrowserNetError { BNE_NONE=0, BNE_BOOT=1, BNE_OPEN=2, BNE_CLOSED=3,
 BNE_TYPE=4, BNE_SIZE=5, BNE_BACKLOG=6, BNE_DEADLINE=7, BNE_TARGET=8,
 BNE_STALE=9, BNE_AUTH=10, BNE_MAP=11, BNE_MILESTONE=12,
 BNE_CAP_CONSUMED=13, BNE_ENET=14, BNE_VISIBILITY=15 };
void browsernet_begin();
void browsernet_frame(unsigned frameId);
BrowserNetState browsernet_state();
int browsernet_error();
void browsernet_close(int reason);
void browsernet_game_observed(unsigned milestone,int cn,int lifeSequence);
#endif
#endif
