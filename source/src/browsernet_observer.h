#ifndef OUTBREAK_BROWSERNET_OBSERVER_H
#define OUTBREAK_BROWSERNET_OBSERVER_H
#if defined(OUTBREAK_NETWORK_CLIENT) && defined(__EMSCRIPTEN__) && !defined(STANDALONE)
void browsernet_position_observed(int cn,int lifeSequence,float x,float y,float z);
void browsernet_remove_observed(int cn);
void browsernet_map_observed(const char *name,int revision);
bool browsernet_spawn_request_allowed();
#endif
#endif
