#ifndef OUTBREAKSTATE_H
#define OUTBREAKSTATE_H

// Local combat timing, independent of rendering and network state.
struct outbreakstate
{
    enum { BLEEDOUT = 20000, REVIVE = 3000 };
    bool downed, used;
    int downmillis, revivemillis, helper, attacker, gun;

    outbreakstate() { reset(); }
    void reset()
    {
        downed = used = false;
        downmillis = revivemillis = 0;
        helper = attacker = gun = -1;
    }
    bool down(int now, int actor, int weapon)
    {
        if(used) return false;
        downed = used = true;
        downmillis = now;
        attacker = actor;
        gun = weapon;
        cancelrevive();
        return true;
    }
    void cancelrevive() { helper = -1; revivemillis = 0; }
    bool expired(int now) const { return downed && now - downmillis >= BLEEDOUT; }
    bool revive(int now, int actor)
    {
        if(!downed || expired(now) || actor < 0) { cancelrevive(); return false; }
        if(helper != actor) { helper = actor; revivemillis = now; }
        if(now - revivemillis < REVIVE) return false;
        downed = false;
        cancelrevive();
        return true;
    }
};
#endif
