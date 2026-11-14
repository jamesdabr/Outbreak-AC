"""Independent read-only verifier CLI; no compiler/Node/process calls."""
import sys
from recipe import verify_main

if __name__=='__main__':
    try:raise SystemExit(verify_main())
    except (OSError,ValueError,KeyError,TypeError) as e:
        print('Blackwood verification refused: '+str(e)[:2048],file=sys.stderr);raise SystemExit(2)
