#include "source/src/browser_map_profile.h"
#include <cassert>
#include <cstring>

int main()
{
    using namespace ob_browser_map;
#if defined(OUTBREAK_SWAMP_CLIENT)
    assert(!std::strcmp(name(), "ac_swamp") && revision() == 179);
    assert(!std::strcmp(cgz_path(), "packages/maps/official/ac_swamp.cgz"));
    assert(cfg_path() == 0);
#elif defined(OUTBREAK_BLACKWOOD_CLIENT)
    assert(!std::strcmp(name(), "blackwood_greybox_v1") && revision() == 1);
    assert(cfg_path() != 0);
#else
    assert(!std::strcmp(name(), "dev_outbreak_browser") && revision() == 2);
    assert(cfg_path() != 0);
#endif
    const int bytes = 23987, dm = 2;
    assert(startup_loaded(0, name(), revision(), bytes));
    assert(!startup_loaded(-1, name(), revision(), bytes));
    assert(pre_change(name(), dm, dm, bytes, revision(), name(), revision(), bytes));
    assert(!pre_change(name(), dm, dm, bytes + 1, revision(), name(), revision(), bytes));
    assert(!pre_change(name(), dm + 1, dm, bytes, revision(), name(), revision(), bytes));
    assert(!pre_change("wrong_map", dm, dm, bytes, revision(), name(), revision(), bytes));
    assert(!pre_change(name(), dm, dm, bytes, revision() + 1, name(), revision(), bytes));
    assert(!post_change(0, true, name(), dm, dm, bytes, revision(), name(), revision(), bytes));
    assert(!spawn_matches(false, name(), revision(), bytes, dm, dm));
    assert(!spawn_matches(true, name(), revision(), 0, dm, dm));
    assert(spawn_matches(true, name(), revision(), bytes, dm, dm));
    assert(!std::strcmp(receipt_name(false), "") && receipt_revision(false) == 0);
    assert(!std::strcmp(receipt_name(true), name()) && receipt_revision(true) == revision());
}
