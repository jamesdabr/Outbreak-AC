/* Experimental platform replacement only. Core ENet/wire/game parsing is unchanged. */
#if defined(OUTBREAK_NETWORK_CLIENT) && defined(__EMSCRIPTEN__) && !defined(STANDALONE)
#define ENET_BUILDING_LIB 1
#include "enet/enet.h"
#include "enet_ws_bridge.h"
#include <emscripten/emscripten.h>
#include <emscripten/heap.h>
#include <stdint.h>
#include <string.h>

static ENetSocket ob_socket = ENET_SOCKET_NULL;
static enet_uint32 ob_time_base;

static int ob_fail(ENetSocket s, int reason) { ob_ws_close(s, reason); return -1; }
static int ob_range(const void *p, size_t n)
{
    uintptr_t start = (uintptr_t)p;
    size_t heap = emscripten_get_heap_size();
    return (!n || p) && start <= heap && n <= heap - start;
}
static int ob_vectors(const ENetBuffer *v, size_t count, size_t *total)
{
    if(!count || count > 65 || !v || !ob_range(v, count * sizeof(*v))) return 0;
    *total = 0;
    for(size_t i = 0; i < count; ++i)
    {
        if(!ob_range(v[i].data, v[i].dataLength) || v[i].dataLength > SIZE_MAX - *total) return 0;
        *total += v[i].dataLength;
    }
    return 1;
}
int enet_initialize(void) { return 0; }
void enet_deinitialize(void)
{
    if(ob_socket != ENET_SOCKET_NULL) { ob_ws_close(ob_socket, OB_WS_CLOSED); ob_socket = ENET_SOCKET_NULL; }
}
enet_uint32 enet_time_get(void) { return (enet_uint32)(uint64_t)emscripten_get_now() - ob_time_base; }
void enet_time_set(enet_uint32 t) { ob_time_base = (enet_uint32)(uint64_t)emscripten_get_now() - t; }
int enet_address_set_host(ENetAddress *a, const char *name)
{
    if(!a || !name || strcmp(name, "127.0.0.1")) return -1;
    a->host = ENET_HOST_TO_NET_32(0x7f000001u);
    return 0;
}
int enet_address_get_host_ip(const ENetAddress *a, char *name, size_t n)
{
    if(!a || !name || n < sizeof("127.0.0.1") || a->host != ENET_HOST_TO_NET_32(0x7f000001u)) return -1;
    memcpy(name, "127.0.0.1", sizeof("127.0.0.1")); return 0;
}
int enet_address_get_host(const ENetAddress *a, char *name, size_t n) { return enet_address_get_host_ip(a, name, n); }
ENetSocket enet_socket_create(ENetSocketType type)
{
    if(type != ENET_SOCKET_TYPE_DATAGRAM) return ENET_SOCKET_NULL;
    int handle = ob_ws_open();
    if(handle < 1) return ENET_SOCKET_NULL;
    ob_socket = handle; return handle;
}
int enet_socket_bind(ENetSocket s, const ENetAddress *a) { (void)s; (void)a; return -1; }
int enet_socket_listen(ENetSocket s, int n) { (void)s; (void)n; return -1; }
ENetSocket enet_socket_accept(ENetSocket s, ENetAddress *a) { (void)s; (void)a; return ENET_SOCKET_NULL; }
int enet_socket_connect(ENetSocket s, const ENetAddress *a) { (void)s; (void)a; return -1; }
int enet_socket_shutdown(ENetSocket s, ENetSocketShutdown how) { (void)s; (void)how; return -1; }
void enet_socket_destroy(ENetSocket s)
{
    if(s == ob_socket) { ob_ws_close(s, OB_WS_CLOSED); ob_socket = ENET_SOCKET_NULL; }
    else ob_ws_close(s, OB_WS_CLOSED); /* stale operations cannot close a current generation */
}
int enet_socket_set_option(ENetSocket s, ENetSocketOption option, int value)
{
    if(s != ob_socket || ob_ws_status(s) < 0) return -1;
    if(option == ENET_SOCKOPT_NONBLOCK && value == 1) return 0;
    if((option == ENET_SOCKOPT_RCVBUF || option == ENET_SOCKOPT_SNDBUF) && value > 0) return 0;
    return -1; /* BROADCAST is intentionally unsupported; host ignores its failure. */
}
int enet_socket_send(ENetSocket s, const ENetAddress *a, const ENetBuffer *v, size_t count)
{
    size_t total;
    if(s != ob_socket) return -1;
    if(!a || !ob_range(a, sizeof(*a)) || a->host != ENET_HOST_TO_NET_32(0x7f000001u) || a->port != 29863)
        return ob_fail(s, OB_WS_TARGET);
    if(!ob_vectors(v, count, &total) || total < 2 || total > 4096) return ob_fail(s, OB_WS_SIZE);
    unsigned char bytes[4096]; size_t at = 0;
    for(size_t i = 0; i < count; ++i)
    {
        if(v[i].dataLength) memcpy(bytes + at, v[i].data, v[i].dataLength);
        at += v[i].dataLength;
    }
    return ob_ws_send(s, bytes, (int)total);
}
int enet_socket_receive(ENetSocket s, ENetAddress *a, ENetBuffer *v, size_t count)
{
    size_t total;
    if(s != ob_socket) return -1;
    if((a && !ob_range(a, sizeof(*a))) || !ob_vectors(v, count, &total)) return ob_fail(s, OB_WS_SIZE);
    unsigned char bytes[4096];
    int n = ob_ws_recv(s, bytes, (int)(total < sizeof(bytes) ? total : sizeof(bytes)));
    if(n <= 0) return n;
    size_t left = (size_t)n, at = 0;
    for(size_t i = 0; i < count && left; ++i)
    {
        size_t amount = v[i].dataLength < left ? v[i].dataLength : left;
        if(amount) memcpy(v[i].data, bytes + at, amount);
        at += amount; left -= amount;
    }
    if(a) { a->host = ENET_HOST_TO_NET_32(0x7f000001u); a->port = 29863; }
    return n;
}
int enet_socket_wait(ENetSocket s, enet_uint32 *conditions, enet_uint32 timeout)
{
    if(!conditions || !ob_range(conditions, sizeof(*conditions))) return ob_fail(s, OB_WS_ENET);
    int wanted = (int)*conditions; *conditions = 0;
    if(timeout || (wanted & ~3)) return ob_fail(s, OB_WS_ENET);
    int ready = ob_ws_readiness(s, wanted);
    if(ready < 0) return -1;
    *conditions = (enet_uint32)ready; return 0;
}
int enet_socketset_select(ENetSocket max, ENetSocketSet *r, ENetSocketSet *w, enet_uint32 timeout)
{
    (void)max; (void)r; (void)w; (void)timeout; return -1; /* never inspect/index fd_set */
}
#endif
