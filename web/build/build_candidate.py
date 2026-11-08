#!/usr/bin/env python3
"""Fixed network candidate preparation or separately MAIN-pinned execution."""
import sys
sys.dont_write_bytecode=True
from candidate_recipe import build_main

if __name__ == '__main__':
    try:
        sys.exit(build_main())
    except (OSError,ValueError,KeyError,TypeError) as error:
        print('candidate build refused: '+str(error),file=sys.stderr)
        sys.exit(2)
