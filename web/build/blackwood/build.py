"""Fixed CLI; preparation may invoke only inside the guarded FIXTURE_ONLY harness."""
import sys
from recipe import build_main

if __name__=='__main__':
    try:raise SystemExit(build_main())
    except (OSError,ValueError,KeyError,TypeError) as e:
        print('Blackwood build refused: '+str(e)[:2048],file=sys.stderr);raise SystemExit(2)
