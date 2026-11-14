#ifndef OUTBREAK_BROWSER_MAP_PROFILE_H
#define OUTBREAK_BROWSER_MAP_PROFILE_H

#if defined(OUTBREAK_SWAMP_CLIENT) && defined(OUTBREAK_BLACKWOOD_CLIENT)
#error OUTBREAK_SWAMP_CLIENT and OUTBREAK_BLACKWOOD_CLIENT are mutually exclusive
#endif
#if defined(OUTBREAK_SWAMP_CLIENT) && (!defined(__EMSCRIPTEN__) || !defined(OUTBREAK_NETWORK_CLIENT) || defined(STANDALONE))
#error OUTBREAK_SWAMP_CLIENT requires __EMSCRIPTEN__ and OUTBREAK_NETWORK_CLIENT without STANDALONE
#endif
#if defined(OUTBREAK_BLACKWOOD_CLIENT) && (!defined(__EMSCRIPTEN__) || !defined(OUTBREAK_NETWORK_CLIENT) || defined(STANDALONE))
#error OUTBREAK_BLACKWOOD_CLIENT requires __EMSCRIPTEN__ and OUTBREAK_NETWORK_CLIENT without STANDALONE
#endif

// Private fixed identity shared by real browser load/parser/receipt/spawn gates.
// No engine state is stored here and no runtime selector or fallback is exposed.
namespace ob_browser_map {
inline const char *name() {
#if defined(OUTBREAK_SWAMP_CLIENT)
    return "ac_swamp";
#elif defined(OUTBREAK_BLACKWOOD_CLIENT)
    return "blackwood_greybox_v1";
#else
    return "dev_outbreak_browser";
#endif
}
inline int revision() {
#if defined(OUTBREAK_SWAMP_CLIENT)
    return 179;
#elif defined(OUTBREAK_BLACKWOOD_CLIENT)
    return 1;
#else
    return 2;
#endif
}
inline const char *cgz_path() {
#if defined(OUTBREAK_SWAMP_CLIENT)
    return "packages/maps/official/ac_swamp.cgz";
#elif defined(OUTBREAK_BLACKWOOD_CLIENT)
    return "packages/maps/blackwood_greybox_v1.cgz";
#else
    return "packages/maps/dev_outbreak_browser.cgz";
#endif
}
inline const char *cfg_path() {
#if defined(OUTBREAK_SWAMP_CLIENT)
    return 0; // Swamp executes its automatic embedded config, not an external CFG.
#elif defined(OUTBREAK_BLACKWOOD_CLIENT)
    return "packages/maps/blackwood_greybox_v1.cfg";
#else
    return "packages/maps/dev_outbreak_browser.cfg";
#endif
}
inline bool name_matches(const char *value) {
    if(!value)return false;
    const char *selected=name();
    for(unsigned i=0;;++i) {
        if(value[i]!=selected[i])return false;
        if(!selected[i])return true;
    }
}
inline bool loaded_matches(const char *loaded_name,int loaded_revision,int loaded_bytes) {
    return name_matches(loaded_name) && loaded_revision==revision() && loaded_bytes>0;
}
inline bool startup_loaded(int load_result,const char *loaded_name,int loaded_revision,int loaded_bytes) {
    return load_result==0 && loaded_matches(loaded_name,loaded_revision,loaded_bytes);
}
inline bool observed_matches(const char *received_name,int received_revision,
                             const char *loaded_name,int loaded_revision,int loaded_bytes,
                             int mode,int deathmatch_mode) {
    return name_matches(received_name) && received_revision==revision() &&
        mode==deathmatch_mode && loaded_matches(loaded_name,loaded_revision,loaded_bytes);
}
inline bool pre_change(const char *received_name,int mode,int deathmatch_mode,
                       int advertised_bytes,int received_revision,
                       const char *loaded_name,int loaded_revision,int loaded_bytes) {
    return advertised_bytes>0 && loaded_bytes==advertised_bytes &&
        observed_matches(received_name,received_revision,loaded_name,loaded_revision,loaded_bytes,mode,deathmatch_mode);
}
inline bool post_change(int load_result,bool incompatible,const char *received_name,
                        int mode,int deathmatch_mode,int advertised_bytes,int received_revision,
                        const char *loaded_name,int loaded_revision,int loaded_bytes) {
    return load_result>=0 && !incompatible && pre_change(received_name,mode,deathmatch_mode,
        advertised_bytes,received_revision,loaded_name,loaded_revision,loaded_bytes);
}
inline bool spawn_matches(bool accepted_receipt,const char *loaded_name,int loaded_revision,
                          int loaded_bytes,int mode,int deathmatch_mode) {
    return accepted_receipt && mode==deathmatch_mode && loaded_matches(loaded_name,loaded_revision,loaded_bytes);
}
inline const char *receipt_name(bool accepted_receipt) { return accepted_receipt?name():""; }
inline int receipt_revision(bool accepted_receipt) { return accepted_receipt?revision():0; }
}
#endif
