"""T101 new evidence runner; old17 bodies/receipts untouched, no real effects."""
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import unittest
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'test_prerequisites.py'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    # Existing original fixture bodies resolve their tiny helpers relative to
    # HERE; keep their shape and put all NEW fake trees/evidence in this lease.
    verifier=HERE/'verify_real.py';original=HERE.parent/'verify_real.py'
    if not verifier.exists():verifier.write_bytes(original.read_bytes())
    assert verifier.read_bytes()==original.read_bytes()
    spec=importlib.util.spec_from_file_location('T101_own_fixture_module',SOURCE);suite=importlib.util.module_from_spec(spec);spec.loader.exec_module(suite)
    suite.HERE=HERE
    sys.addaudithook(suite.audit)
    number=1
    while (HERE/('fixture-attempt-%d.json'%number)).exists():number+=1
    capture=io.StringIO();result=unittest.TextTestRunner(stream=capture,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(suite))
    (HERE/('fixture-attempt-%d.txt'%number)).write_text(capture.getvalue())
    value=dict(schema_version=1,ticket='T1011.0',scope='FIXTURE_ONLY_ACTUAL_BOUNDARY_POLICY',status='PASS' if result.wasSuccessful() else 'FAIL',
      groups=result.testsRun,failures=len(result.failures),errors=len(result.errors),original_groups=17,new_groups=3,
      stager_sha256=sha(suite.REAL/'web/repro/stage_prerequisites.py'),test_source_sha256=sha(SOURCE),runner_sha256=sha(Path(__file__)),
      real_sdk_process_network_effects='DENIED_BY_FIXTURE_AUDIT',real_stager_execution=False,old_fixture_receipts_overwritten=False)
    (HERE/('fixture-attempt-%d.json'%number)).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
    print(json.dumps(value));return 0 if result.wasSuccessful() else 1
if __name__=='__main__':sys.exit(main())
