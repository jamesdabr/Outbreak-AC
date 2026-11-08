"""T083 local-only golden/oracle gate; never runs game or acquisition helpers."""
import argparse
import hashlib
import itertools
import json
import os
from pathlib import Path
import platform
import random
import re
import shutil
import struct
import subprocess
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
SDK = Path('/private/tmp/outbreak-web-sdk')
WIRE = struct.Struct('<4sHBBHHI16sI')
FIELDS = struct.Struct('<BHI16sI')
CASE = struct.Struct('<BBBBI')
SENTINEL = b'\xa5'


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()


def snapshot(roots):
    result = {}
    for root in roots:
        if not root.exists():
            raise RuntimeError('Missing input: ' + str(root))
        for p in ([root] if root.is_file() else sorted(root.rglob('*'))):
            if p.is_file():
                result[str(p)] = sha(p)
            elif p.is_symlink():
                result[str(p)] = 'symlink:' + os.readlink(p)
    return result


def header(kind=255, body=0, epoch=0x89abcdef, identity=bytes(range(16)), seq=0xfedcba98):
    return WIRE.pack(b'OBP1', 1, kind, 0, 36+body, 36, epoch, identity, seq)


def decode_case(data, offset=0, null=0):
    return CASE.pack(0, null, offset, 0, len(data)) + data


def encode_case(kind=255, body=0, capacity=36, offset=0, null=0,
                epoch=0x89abcdef, identity=bytes(range(16)), seq=0xfedcba98):
    return CASE.pack(1, null, offset, 0, capacity) + FIELDS.pack(kind, body, epoch, identity, seq)


def oracle(case):
    op, null, offset, _, length = CASE.unpack_from(case)
    error = 0
    if op == 0:
        data = case[8:]
        if null:
            error = 1
        elif length < 36:
            error = 2
        elif length > 1100:
            error = 7
        else:
            magic, version, kind, flags, total, size, epoch, identity, seq = WIRE.unpack_from(data)
            if magic != b'OBP1':
                error = 3
            elif version != 1:
                error = 4
            elif flags != 0:
                error = 5
            elif size != 36:
                error = 6
            elif total != length:
                error = 7
            elif kind == 0:
                error = 8
        result = SENTINEL * 27 if error else FIELDS.pack(kind, length-36, epoch, identity, seq)
    else:
        kind, body, epoch, identity, seq = FIELDS.unpack_from(case, 8)
        if null:
            error = 1
        elif length < 36:
            error = 2
        elif body > 1064:
            error = 7
        elif kind == 0:
            error = 8
        result = bytearray(SENTINEL * (16+offset+length+16))
        if not error:
            result[16+offset:16+offset+36] = WIRE.pack(b'OBP1', 1, kind, 0, 36+body,
                                                     36, epoch, identity, seq)
    return (bytes([int(error == 0), error, 1, 1, 1, 1]) + result).hex()


def corpus():
    # Every truncation, provided length, encoder capacity and body boundary.
    for length in range(36):
        yield 'truncation', decode_case(header()[:length], length % 8)
    for length in range(36, 1102):
        yield 'provided-length', decode_case(header(body=length-36) + bytes([0x53])*(length-36), length % 8)
    for length in range(1138):
        yield 'capacity', encode_case(body=(1064 if length % 2 else 0), capacity=length, offset=length % 8)
    for body in list(range(1066)) + [65535]:
        yield 'body-boundary', encode_case(body=body, capacity=1100, offset=body % 8)
    for length in (0, 1, 35, 36, 1100, 1101, 1137):
        yield 'null-decode', decode_case(bytes(length), null=1)
        yield 'null-encode', encode_case(kind=0, body=65535, capacity=length, null=1)
    for kind in range(256):
        yield 'all-types-decode', decode_case(header(kind=kind), kind % 8)
        yield 'all-types-encode', encode_case(kind=kind, capacity=67, offset=kind % 8)
    for flags in range(256):
        data = bytearray(header()); data[7] = flags
        yield 'all-flags', decode_case(data, flags % 8)
    for position in range(36):
        for bit in range(8):
            data = bytearray(header()); data[position] ^= 1 << bit
            yield 'header-bit', decode_case(data, bit)
    for offset in range(8):
        for epoch, seq, identity in itertools.product((0, 1, 0x80000000, 0xffffffff),
                (0, 1, 0x80000000, 0xffffffff), (bytes(16), b'\xff'*16, bytes(range(16)))):
            yield 'fields-extrema-decode', decode_case(header(epoch=epoch, seq=seq, identity=identity), offset)
            yield 'fields-extrema-encode', encode_case(epoch=epoch, seq=seq, identity=identity, offset=offset)
    for position, values in ((4, (0, 2, 255, 256, 65535)),
                             (10, (0, 1, 35, 37, 1100, 65535)),
                             (8, (0, 1, 35, 37, 1100, 1101, 65535))):
        for value in values:
            data = bytearray(header()); struct.pack_into('<H', data, position, value)
            yield 'scalar-malformed', decode_case(data)
    # Every pair of malformed checks: assert the contract's first-failure order.
    defects = [(0, b'NOPE'), (4, b'\x00\x00'), (7, b'\xff'),
               (10, b'\x00\x00'), (8, b'\x00\x00'), (6, b'\x00')]
    for n in range(1, 7):
        for chosen in itertools.combinations(defects, n):
            data = bytearray(header())
            for pos, value in chosen:
                data[pos:pos+len(value)] = value
            yield 'error-priority-decode', decode_case(data)
    for null, capacity, body, kind in itertools.product((0, 1), (0, 35, 36, 37),
                                                     (0, 1064, 1065, 65535), (0, 1)):
        yield 'error-priority-encode', encode_case(kind=kind, body=body, capacity=capacity, null=null)
    rng = random.Random(83056)
    for index in range(4096):
        body = rng.randrange(1065)
        data = bytearray(header(kind=rng.randrange(256), body=body,
                         epoch=rng.getrandbits(32), identity=rng.randbytes(16), seq=rng.getrandbits(32))
                         + rng.randbytes(body))
        if index % 3 == 0:
            for _ in range(rng.randrange(1, 5)):
                pos = rng.randrange(len(data)); data[pos] = rng.randrange(256)
        if index % 7 == 0:
            data = data[:rng.randrange(len(data)+1)]
        if index % 11 == 0 and len(data) < 1101:
            data.append(0xff)
        yield 'random-decode', decode_case(data, rng.randrange(8), int(index % 127 == 0))
        yield 'random-encode', encode_case(kind=rng.randrange(256), body=rng.randrange(65536),
               capacity=rng.randrange(1138), offset=rng.randrange(8), null=int(index % 127 == 0),
               epoch=rng.getrandbits(32), identity=rng.randbytes(16), seq=rng.getrandbits(32))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--attempt', default='attempt-1')
    args = parser.parse_args()
    if not re.fullmatch(r'attempt-[1-9][0-9]*', args.attempt):
        raise RuntimeError('Attempt must be a new task-local attempt-N directory')
    attempt = HERE / args.attempt
    attempt.mkdir()  # once-only, never overwrite evidence
    for name in ('tmp', 'logs', 'node-cache'):
        (attempt / name).mkdir()
    def record(name, value):
        (attempt / name).write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')
    env = dict(PATH='/usr/bin:/bin:/usr/sbin:/sbin', TMPDIR=str(attempt / 'tmp'),
        PYTHONDONTWRITEBYTECODE='1', EM_CACHE=str(attempt / 'cache'), EM_FROZEN_CACHE='1',
        EM_PORTS=str(attempt / 'cache/ports'), EMCC_TEMP_DIR=str(attempt / 'tmp'),
        NODE_COMPILE_CACHE=str(attempt / 'node-cache'),
        ASAN_OPTIONS='halt_on_error=1:abort_on_error=1', UBSAN_OPTIONS='halt_on_error=1:print_stacktrace=1')
    native = Path('/usr/bin/clang++')  # D080: approved launcher correction only.
    clang, linker, nm, node = [SDK / p for p in ('upstream/bin/clang++', 'upstream/bin/wasm-ld',
                                               'upstream/bin/llvm-nm', 'node/24.19.0_64bit/bin/node')]
    runtimes = [Path('/Library/Developer/CommandLineTools/usr/lib/clang/17/lib/darwin') / n for n in
                ('libclang_rt.asan_osx_dynamic.dylib', 'libclang_rt.ubsan_osx_dynamic.dylib')]
    if sha(node) != '27db838bb204ef7c21df2931f5656e4c8fb32e6e947f363a402b49714d32b5b1':
        raise RuntimeError('Accepted Node identity mismatch')
    if (SDK / 'upstream/emscripten/emscripten-version.txt').read_text().strip() != '"7.0.0"' or \
       (SDK / 'upstream/emscripten/emscripten-revision.txt').read_text().strip() != '777e6e5db7b4990bcaeb1b9998ed642cc84e6629':
        raise RuntimeError('SDK identity mismatch')
    # Exclude unconsumed controller/candidate-test sources owned by other workers.
    protected_roots = [REPO / n for n in ('source/src', 'source/enet', 'source/outbreak/fixed.h',
        'source/outbreak/fixed.cpp', 'web/build/out', 'web/server/out', 'web/build/.cache',
        'web/build/generated/t066/attempt-T070-1/bundle', 'tests/outbreak/numeric/T078')] + [SDK]
    before = snapshot(protected_roots)
    record('protected-before.json', before)
    source = REPO / 'source/outbreak/envelope.cpp'
    wrapper = HERE / 'wrapper.cpp'
    inputs = snapshot([source, source.with_suffix('.h'), wrapper, HERE / 'wasm_runner.mjs',
        Path(__file__).resolve(), REPO / 'MVP/PORTABLE_FORMAT_FOUNDATION.md', REPO / 'tickets/T083.md'])
    common = ['-std=c++11', '-O2', '-Wall', '-Wextra', '-Werror', '-I', str(source.parent)]
    sanitizers = ['-fsanitize=address,undefined', '-fno-sanitize-recover=all', '-fno-omit-frame-pointer']
    commands = [
        [str(native)] + common + ['-DT083_NATIVE', str(source), str(wrapper), '-o', str(attempt / 'native')],
        [str(native)] + common + sanitizers + ['-DT083_NATIVE', str(source), str(wrapper), '-o', str(attempt / 'sanitized')]]
    for src, obj in ((source, 'envelope.o'), (wrapper, 'wrapper.o')):
        commands.append([str(clang), '--target=wasm32-unknown-emscripten',
            '--sysroot=' + str(attempt / 'cache/sysroot')] + common + ['-c', str(src), '-o', str(attempt / obj)])
    link = [str(linker), '--no-entry', '--export=case_buffer', '--export=result_buffer', '--export=execute',
            str(attempt / 'envelope.o'), str(attempt / 'wrapper.o')]
    archive = attempt / 'cache/sysroot/lib/wasm32-emscripten/libc.a'
    nm_command = [str(nm), '--undefined-only', str(attempt / 'envelope.o'), str(attempt / 'wrapper.o')]
    executions = [[str(attempt / 'native')], [str(node), str(HERE / 'wasm_runner.mjs'), str(attempt / 'envelope.wasm')],
                  [str(attempt / 'sanitized')]]
    # Generate and hash exact corpus/goldens before invoking any compiler.
    counts = {}
    with (attempt / 'corpus.txt').open('w') as c, (attempt / 'expected.txt').open('w') as e, \
         (attempt / 'labels.txt').open('w') as labels:
        for label, case in corpus():
            c.write(case.hex() + '\n'); e.write(oracle(case) + '\n'); labels.write(label + '\n')
            counts[label] = counts.get(label, 0) + 1
    record('plan.json', dict(commands=commands, nm=nm_command, link_prefix=link,
        conditional_libc='Append only inspected cached libc.a if nm reports memcpy/memset/memmove; no fallback',
        link_suffix=['-o', str(attempt / 'envelope.wasm')], execution=executions,
        environment=env, inputs=inputs, tools=snapshot([native, clang, linker, nm, node,
        Path(sys.executable).resolve()] + runtimes), corpus=snapshot([attempt / 'corpus.txt', attempt / 'expected.txt']),
        batch_limit=256, counts=counts, platform=platform.platform(), machine=platform.machine(), python=sys.version))
    shutil.copytree(REPO / 'web/build/.cache/sysroot', attempt / 'cache/sysroot', symlinks=True)
    copied = snapshot([attempt / 'cache/sysroot'])
    expected_copy = {str(attempt / 'cache/sysroot' / Path(p).relative_to(REPO / 'web/build/.cache/sysroot')): h
                     for p, h in snapshot([REPO / 'web/build/.cache/sysroot']).items()}
    if copied != expected_copy:
        raise RuntimeError('Frozen sysroot copy mismatch')
    def invoke(command, name, payload=None):
        record('logs/' + name + '.command.json', dict(command=command, environment=env))
        result = subprocess.run(command, cwd=REPO, env=env, input=payload,
                                text=True, capture_output=True, timeout=60)
        (attempt / 'logs' / (name + '.stdout')).write_text(result.stdout)
        (attempt / 'logs' / (name + '.stderr')).write_text(result.stderr)
        if result.returncode:
            raise RuntimeError(f'{name} failed ({result.returncode}); inspect logs, no acquisition/flag fallback')
        return result
    for i, tool in enumerate((native, clang, linker, nm, node)):
        invoke([str(tool), '--version'], f'tool-{i}')
    for i, command in enumerate(commands):
        invoke(command, f'build-{i}')
    undefined = invoke(nm_command, 'undefined').stdout
    needs_memory = bool(re.search(r'\bU\s+(memcpy|memset|memmove)\b', undefined))
    if needs_memory:
        # This source/archive was inspected before execution and is frozen in the
        # copied sysroot + before snapshot. Record exact identity before link.
        record('memory-library.json', dict(path=str(archive), sha256=sha(archive)))
        link.append(str(archive))
    link += ['-o', str(attempt / 'envelope.wasm')]
    invoke(link, 'link')
    failures, batches, count, passed_counts = [], 0, 0, {'success': 0, 'failure': 0}
    files = [attempt / n for n in ('native.txt', 'wasm.txt', 'sanitized.txt')]
    streams = [p.open('w') for p in files]
    try:
        with (attempt / 'corpus.txt').open() as c, (attempt / 'expected.txt').open() as e:
            while True:
                batch = list(itertools.islice(c, 256))
                if not batch:
                    break
                expected = list(itertools.islice(e, len(batch)))
                expected_text, payload = ''.join(expected), ''.join(batch)
                for name, command, stream in zip(('native', 'wasm', 'sanitized'), executions, streams):
                    result = invoke(command, f'{name}-{batches:03}', payload)
                    stream.write(result.stdout)
                    if result.stderr:
                        raise RuntimeError(f'{name} batch {batches}: unexpected stderr, inspect retained log')
                    actual = result.stdout.splitlines()
                    if len(actual) != len(expected):
                        raise RuntimeError(f'{name}: result count mismatch')
                    if result.stdout != expected_text:
                        for i, (got, want) in enumerate(zip(actual, expected)):
                            if got != want.strip() and len(failures) < 16:
                                failures.append(dict(target=name, index=count+i, case=batch[i].strip(),
                                                     expected=want.strip(), actual=got))
                for value in expected:
                    passed_counts['success' if value.startswith('01') else 'failure'] += 1
                batches += 1
                count += len(batch)
    finally:
        for stream in streams:
            stream.close()
    after = snapshot(protected_roots)
    record('protected-after.json', after)
    changed = [p for p in sorted(set(before) | set(after)) if before.get(p) != after.get(p)]
    input_changes = snapshot([Path(p) for p in inputs]) != inputs
    record('result.json', dict(passed=not failures and not changed and not input_changes,
        cases=count, batches=batches, classification=passed_counts, by_category=counts,
        failures=failures, protected_files=len(before), changed_protected=changed, inputs_changed=input_changes,
        libc_linked=needs_memory, hashes=snapshot(files + [attempt / n for n in
        ('corpus.txt', 'expected.txt', 'native', 'sanitized', 'envelope.o', 'wrapper.o', 'envelope.wasm')])) )
    print(json.dumps(dict(cases=count, batches=batches, failures=len(failures),
                         changed_protected=len(changed), inputs_changed=input_changes)))
    return int(bool(failures or changed or input_changes))


if __name__ == '__main__':
    sys.exit(main())
