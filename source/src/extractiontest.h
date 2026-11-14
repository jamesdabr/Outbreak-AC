#ifndef EXTRACTIONTEST_H
#define EXTRACTIONTEST_H

// Small local mock shared by the engine adapter and the standalone logic test.
// Expiry is resolved before zone entry: reaching the zone at the deadline loses.
struct extractiontestround
{
    enum { MAX_ACTORS = 8 };
    bool running, finished, extracted[MAX_ACTORS];
    int remaining, participants;

    extractiontestround() { reset(); }
    void reset()
    {
        running = finished = false;
        remaining = participants = 0;
        for(int i = 0; i < MAX_ACTORS; ++i) extracted[i] = false;
    }
    bool start(int count, int milliseconds)
    {
        if(count < 1 || count > MAX_ACTORS || milliseconds <= 0) return false;
        reset();
        participants = count;
        remaining = milliseconds;
        running = true;
        return true;
    }
    void advance(int milliseconds)
    {
        if(!running || milliseconds <= 0) return;
        if(milliseconds >= remaining)
        {
            remaining = 0;
            running = false;
            finished = true;
        }
        else remaining -= milliseconds;
    }
    bool enter(int actor, bool alive)
    {
        if(!running || !alive || actor < 0 || actor >= participants || extracted[actor]) return false;
        extracted[actor] = true;
        return true;
    }
    int winners() const
    {
        int count = 0;
        for(int i = 0; i < participants; ++i) if(extracted[i]) ++count;
        return count;
    }
    bool won(int actor) const
    {
        return finished && actor >= 0 && actor < participants && extracted[actor];
    }
};

#endif
