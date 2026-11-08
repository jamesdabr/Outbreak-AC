#!/usr/bin/env python3
"""Verify linked T031 output as data; never execute the game or start a server."""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'web/build/out'
EVIDENCE = ROOT / 'web/build/generated/t031'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class CanvasParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []

    def handle_starttag(self, tag, attrs):
        if tag == 'canvas':
            self.ids.append(dict(attrs).get('id'))


def main():
    global EVIDENCE
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence-dir', default='web/build/generated/t031')
    args = parser.parse_args()
    EVIDENCE = (ROOT / args.evidence_dir).resolve()
    assert EVIDENCE.is_relative_to(ROOT / 'web/build/generated')
    result = json.loads((EVIDENCE / 'result.json').read_text())
    assert result['status'] == 'PASS' and result['link']['exit_code'] == 0 and result['link']['packaged']
    assert len(result['compiles']) == 61 and all(x['status'] == 'PASS' for x in result['compiles'])
    assert not result['stale_inputs'] and result['native_outputs_unchanged']
    assert all((ROOT / p).is_file() and sha(ROOT / p) == h for p, h in result['inputs_final'].items())
    assert all((ROOT / p).is_file() and sha(ROOT / p) == h for p, h in result['pack_inputs'].items())
    assert all((ROOT / p).is_file() and sha(ROOT / p) == h for p, h in result['link']['outputs'].items())
    assert sha(OUT / 'build-metadata.json') == result['bundle_metadata_sha256']
    html = (OUT / 'index.html').read_text()
    canvas = CanvasParser()
    canvas.feed(html)
    assert canvas.ids == ['canvas'] and '{{{ SCRIPT }}}' not in html
    assert (OUT / 'index.wasm').read_bytes()[:8] == b'\x00asm\x01\x00\x00\x00'
    data = (OUT / 'index.data').read_bytes()
    assert len(data) == 87897
    entries = re.findall(r'\{filename:"([^"]+)",start:(\d+),end:(\d+)\}', (OUT / 'index.js').read_text())
    manifest = json.loads((ROOT / 'web/assets/original/manifest.json').read_text())
    expected = {e['virtual_path']: e for e in manifest['entries']}
    assert len(entries) == 41 and {e[0] for e in entries} == set(expected)
    checks = []
    for path, start, end in entries:
        block = data[int(start):int(end)]
        entry = expected[path]
        assert len(block) == entry['bytes'] and hashlib.sha256(block).hexdigest() == entry['sha256']
        checks.append({'path': path, 'start': int(start), 'end': int(end), 'sha256': entry['sha256'], 'status': 'PASS'})
    verification = {'status': 'PASS', 'actual_preload_files': checks, 'data_bytes': len(data), 'canvas_id': 'canvas',
                    'wasm_magic': True, 'inputs_outputs_stable': True, 'runtime_decoding': 'NOT RUN'}
    (EVIDENCE / 'preload-output-verification.json').write_text(json.dumps(verification, indent=2) + '\n')
    files = [{'file': name, 'bytes': (OUT / name).stat().st_size, 'sha256': sha(OUT / name)}
             for name in ('index.html', 'index.js', 'index.wasm', 'index.data', 'build-metadata.json')]
    pins = {'artifact_id': result['ticket'].split()[0] + '-' + result['bundle_id'], 'root': str(OUT), 'status': 'LINKED_NOT_BROWSER_VERIFIED',
            'entry': 'index.html', 'bundle_id': result['bundle_id'], 'files': files,
            'pack_manifest_sha256': result['pack_validation']['manifest_sha256'], 'safe_gl_flag': '-sGL_UNSAFE_OPTS=0'}
    (EVIDENCE / 'artifact-pins.json').write_text(json.dumps(pins, indent=2) + '\n')
    command = ['/private/tmp/outbreak-web-sdk/node/24.19.0_64bit/bin/node', 'web/qa/game_probe.mjs', '--mode', 'real',
               '--root', 'web/build/out', '--url', 'http://127.0.0.1:0/index.html', '--artifact-id', pins['artifact_id']]
    for item in files:
        command += ['--expect-file', item['file'] + '=' + item['sha256']]
    command += ['--output', 'web/qa/results/' + result['ticket'].split()[0] + '-real-first.json']
    (EVIDENCE / 'qa-launch-command.json').write_text(json.dumps({'executed': False, 'owner': 'QA after MAIN dispatch',
                                                              'cwd': str(ROOT), 'command': command}, indent=2) + '\n')
    print(json.dumps(pins, indent=2))


if __name__ == '__main__':
    main()
