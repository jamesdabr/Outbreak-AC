#include "../src/extractiontest.h"
#include <cassert>
#include <cstdio>

int main()
{
    extractiontestround round;
    assert(!round.enter(0, true));
    assert(!round.start(0, 120000));
    assert(!round.start(9, 120000));
    assert(!round.start(1, 0));

    // No extraction: everyone loses, including a player arriving at the deadline.
    assert(round.start(4, 120000));
    round.advance(119999);
    assert(round.running && !round.finished && round.remaining == 1);
    round.advance(1);
    assert(!round.enter(0, true));
    assert(round.finished && round.winners() == 0);
    for(int i = 0; i < 4; ++i) assert(!round.won(i));

    // One extraction: only that participant wins, after expiry.
    assert(round.start(4, 120000));
    assert(!round.enter(0, false));
    assert(!round.enter(-1, true));
    assert(!round.enter(4, true));
    assert(round.enter(1, true));
    assert(!round.enter(1, true));
    assert(!round.won(1));
    round.advance(120001);
    assert(round.winners() == 1 && round.won(1));
    assert(!round.won(0) && !round.won(2) && !round.won(3));
    round.advance(1000);
    assert(round.remaining == 0 && round.won(1));

    // Multiple extractions: all extracted players win, everyone else loses.
    assert(round.start(8, 120000));
    assert(round.enter(0, true));
    assert(round.enter(7, true));
    round.advance(-1);
    assert(round.remaining == 120000);
    round.advance(120000);
    assert(round.winners() == 2 && round.won(0) && round.won(7));
    assert(!round.won(3) && !round.won(8));

    // Restart and cancellation cannot preserve extraction from an older round.
    assert(round.start(1, 1000));
    assert(!round.extracted[0] && round.winners() == 0);
    round.reset();
    assert(!round.running && !round.finished && !round.enter(0, true));
    assert(round.participants == 0 && round.remaining == 0);
    std::puts("PASS: deadline, nobody/one/multiple extracted, invalid entry, restart/reset");
}
