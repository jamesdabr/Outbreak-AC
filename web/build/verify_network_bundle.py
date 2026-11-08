#!/usr/bin/env python3
"""Read-only T066 network verifier: explicit --network-root and --attempt/pins."""
import sys
sys.dont_write_bytecode = True
from build_network_client import RECIPE

validate_payload = RECIPE.validate_payload
verify = RECIPE.verify
main = RECIPE.verify_main

if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError) as error:
        print('T066 verification refused: ' + str(error), file=sys.stderr)
        sys.exit(2)
