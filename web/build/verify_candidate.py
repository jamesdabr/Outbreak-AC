#!/usr/bin/env python3
"""Independent read-only candidate verifier; optional one exclusive receipt."""
import sys
sys.dont_write_bytecode=True
from candidate_recipe import verify_main

if __name__ == '__main__':
    try:
        sys.exit(verify_main())
    except (OSError,ValueError,KeyError,TypeError) as error:
        print('candidate verification refused: '+str(error),file=sys.stderr)
        sys.exit(2)
