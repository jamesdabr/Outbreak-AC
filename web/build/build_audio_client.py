#!/usr/bin/env python3
"""T060 fixed audio recipe; --plan-only or future MAIN-authorized --execute."""
import sys
sys.dont_write_bytecode = True
from profile_client import Recipe

RECIPE = Recipe('audio')
main = RECIPE.main

if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError) as error:
        print('T060 refused: ' + str(error), file=sys.stderr)
        sys.exit(2)
