#!/usr/bin/env python3
"""T066 fixed network recipe; --plan-only or future MAIN-authorized --execute."""
import sys
sys.dont_write_bytecode = True
from profile_client import Recipe

RECIPE = Recipe('network')
main = RECIPE.main

if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError) as error:
        print('T066 refused: ' + str(error), file=sys.stderr)
        sys.exit(2)
