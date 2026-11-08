#!/usr/bin/env python3
"""Generate T080 isolated DATA once. Never overlays an accepted profile."""
import sys
sys.dont_write_bytecode=True
from candidate import HERE,build,canonical,require

if __name__=='__main__':
    require(not (HERE/'manifest.json').exists(),'existing candidate manifest immutable')
    result=build(HERE/'pack-root')
    (HERE/'manifest.json').write_text(canonical(result))
    print('Generated five-member Blackwood candidate DATA only; runtime NOT RUN')
