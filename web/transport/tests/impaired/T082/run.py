"""T082 fixed private case. PREPARATION; no execution without future MAIN release."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT/'web/transport/tests/two-client/T067'))
import policy,supervise
CASE='impaired40_drop50'
def main():
 p=argparse.ArgumentParser();p.add_argument('--prepare-plan',action='store_true');p.add_argument('--execute',action='store_true');p.add_argument('--pins');p.add_argument('--pins-sha');p.add_argument('--attempt');a=p.parse_args()
 if a.prepare_plan and not any((a.execute,a.pins,a.pins_sha,a.attempt)):
  print(json.dumps({'status':'NOT_RUN','case_kind':CASE,'impairment':policy.IMPAIRMENT,'pending':['MAIN T082 acceptance','fresh complete pins + expected SHA + explicit actual release'],'limits':supervise.plan()['limits']},indent=2));return 0
 policy.require(a.execute and a.pins and a.pins_sha and a.attempt and not a.prepare_plan,'future MAIN impaired execution pins required')
 result=supervise.gated_execute(ROOT,a.pins,a.pins_sha,a.attempt,supervise.Runtime(ROOT,CASE),case_kind=CASE);print(json.dumps(policy.redact(result),indent=2));return 0 if result['status']=='PASS' else 1
if __name__=='__main__':
 try:raise SystemExit(main())
 except (policy.Refused,ValueError,OSError) as e:print(json.dumps({'status':'REFUSED','reason':str(e),'runtime_started':supervise.EXECUTION_STARTED}));raise SystemExit(2)
