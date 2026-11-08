"""Pure owned-process selection. FIXTURE tested; never signals a process."""
from pathlib import PurePosixPath
import policy

def select(rows, result, executable, known=()):
 """Only exact executable + isolated attempt profile, then proved descendants.
 Process table is transient; callers persist selected identities only.
 """
 prefix=str(PurePosixPath(result))+'/browser-temp-'
 selected={r['pid']:r for r in rows if r['pid'] in known}
 for r in rows:
  args=r['command']
  if args.startswith(executable+' ') and '--user-data-dir='+prefix in args:
   profile=args.split('--user-data-dir=',1)[1].split(' --',1)[0]
   if '..' not in PurePosixPath(profile).parts and profile.startswith(prefix):selected[r['pid']]=r
 while True:
  children={r['pid']:r for r in rows if r['ppid'] in selected and r['pid'] not in selected}
  if not children:break
  selected.update(children)
 return list(selected.values())

def same_identity(old,current):
 return all(old[k]==current[k] for k in ('pid','birth','command'))

def signal_owned(known,current,send,kind):
 """Injected effect; only still-matching identities, children first."""
 sent=[]
 for pid,row in reversed(list(known.items())):
  if pid in current and same_identity(row,current[pid]):
   try:send(pid,kind);sent.append(pid)
   except ProcessLookupError:pass
 return sent

def parse(text):
 rows=[]
 for line in text.splitlines():
  parts=line.strip().split(None,8)
  if len(parts)==9 and all(x.isdigit() for x in parts[:3]):rows.append(dict(zip(('pid','ppid','pgid','birth','command'),[int(x) for x in parts[:3]]+[' '.join(parts[3:8]),parts[8]])))
 return rows
