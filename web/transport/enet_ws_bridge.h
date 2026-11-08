#ifndef OUTBREAK_ENET_WS_BRIDGE_H
#define OUTBREAK_ENET_WS_BRIDGE_H
#if defined(OUTBREAK_NETWORK_CLIENT) && defined(__EMSCRIPTEN__) && !defined(STANDALONE)
enum ob_ws_error { OB_WS_NONE=0, OB_WS_BOOT=1, OB_WS_OPEN=2, OB_WS_CLOSED=3,
 OB_WS_TYPE=4, OB_WS_SIZE=5, OB_WS_BACKLOG=6, OB_WS_DEADLINE=7, OB_WS_TARGET=8,
 OB_WS_STALE=9, OB_WS_AUTH=10, OB_WS_MAP=11, OB_WS_MILESTONE=12,
 OB_WS_CAP_CONSUMED=13, OB_WS_ENET=14, OB_WS_VISIBILITY=15 };
#ifdef __cplusplus
extern "C" {
#endif
int ob_ws_open(void);
int ob_ws_status(int handle);
int ob_ws_send(int handle,const void *bytes,int length);
int ob_ws_recv(int handle,void *bytes,int capacity);
void ob_ws_frame(unsigned frameId);
void ob_ws_close(int handle,int reason);
int ob_ws_readiness(int handle,int conditions);
#ifdef __cplusplus
}
#endif
#endif
#endif
