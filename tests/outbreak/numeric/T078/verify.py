"""Local T078-only compile/oracle gate. No network, installations or game entrypoints."""
import hashlib
import itertools
import json
import math
import os
from pathlib import Path
import platform
import random
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
SDK = Path('/private/tmp/outbreak-web-sdk')
ATTEMPT = HERE / 'attempt-1'
LO, HI = -(2**31), 2**31 - 1
SENTINELS = (123456789, -987654321)


def sha(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def snapshot(roots):
    result = {}
    for root in roots:
        if not root.exists():
            raise RuntimeError('Missing preservation input: ' + str(root))
        paths = [root] if root.is_file() else sorted(root.rglob('*'))
        for path in paths:
            if path.is_file():
                result[str(path)] = sha(path)
            elif path.is_symlink():
                result[str(path)] = 'symlink:' + os.readlink(path)
    return result


def write_json(name, value):
    (ATTEMPT / name).write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def trunc(n, d):
    return (-1 if (n < 0) != (d < 0) else 1) * (abs(n) // abs(d))


def oracle(case):
    op, *args = case
    if op == 8:
        return (1, math.isqrt(args[0]), 0)
    a, b, d = args
    initial = a if op in (5, 6, 7) else SENTINELS[0]
    if op in (3, 4):
        if op == 4 or not (-127 <= a <= 127 and -127 <= b <= 127):
            return (0, SENTINELS[0], SENTINELS[1])
        squared = a*a + b*b
        if squared <= 127**2:
            x, y = trunc(a * 65536, 127), trunc(b * 65536, 127)
        else:
            radicand = squared * 2**32
            floor = math.isqrt(radicand)
            denominator = floor + (floor*floor != radicand)
            x, y = trunc(a * 2**32, denominator), trunc(b * 2**32, denominator)
        assert x*x + y*y <= 65536**2
        return (1, x, y)
    if op in (0, 5):
        value = a + b
    elif op in (1, 6):
        value = a - b
    elif op in (2, 7):
        if d == 0:
            return (0, initial, SENTINELS[1])
        # Independent arbitrary-precision formulation, including signed ties.
        magnitude = (2 * abs(a*b) + abs(d)) // (2 * abs(d))
        value = -magnitude if (a*b < 0) != (d < 0) else magnitude
    else:
        raise AssertionError(case)
    return (1, value, SENTINELS[1]) if LO <= value <= HI else (0, initial, SENTINELS[1])


def cases():
    boundary = [LO, LO+1, -65536, -32768, -3, -2, -1, 0, 1, 2, 3,
                32767, 65536, HI-1, HI]
    for a, b in itertools.product(boundary, repeat=2):
        for op in (0, 1, 5, 6):
            yield (op, a, b, 0)
        for d in boundary:
            for op in (2, 7):
                yield (op, a, b, d)
    for a, b, d in [(1431655765, 3, 2), (-1431655765, 3, 2),
                    (-1431655766, 3, 2), (HI, HI, HI-1)]:
        for sign in (-1, 1):
            yield (2, a, b, d*sign)
    rng = random.Random(78051)
    for _ in range(8192):
        a, b, d = (rng.randint(LO, HI) for _ in range(3))
        yield (2, a, b, d)
        yield (rng.choice((0, 1)), a, b, 0)
    # Every signed-byte pair: 65025 valid +511 invalid pairs with -128.
    for x in range(-128, 128):
        for y in range(-128, 128):
            yield (3, x, y, 0)
    axis_edges = [-32768, -129, -128, -127, -1, 0, 1, 127, 128, 129, 32767]
    for x, y in itertools.product(axis_edges, repeat=2):
        yield (3, x, y, 0)
        yield (4, x, y, 0)
    roots = [0, 1, 2, 3, 4, 65535, 65536, 2**16+1, 2**31-1, 2**31,
             2**32-2, 2**32-1] + [rng.randrange(2**32) for _ in range(1024)]
    for r in roots:
        for offset in (-1, 0, 1):
            value = r*r + offset
            if 0 <= value < 2**64:
                yield (8, value)
    yield (8, 2**64-1)
    for _ in range(2048):
        yield (8, rng.randrange(2**64))


def main():
    # Never overwrite or reuse evidence/cache from a previous attempt.
    ATTEMPT.mkdir()
    for name in ('tmp', 'node-cache', 'logs'):
        (ATTEMPT / name).mkdir()
    cache = ATTEMPT / 'cache'
    env = dict(PATH='/usr/bin:/bin:/usr/sbin:/sbin', TMPDIR=str(ATTEMPT / 'tmp'),
               EM_CACHE=str(cache), EM_PORTS=str(cache / 'ports'), EM_FROZEN_CACHE='1',
               EMCC_TEMP_DIR=str(ATTEMPT / 'tmp'), NODE_COMPILE_CACHE=str(ATTEMPT / 'node-cache'),
               PYTHONDONTWRITEBYTECODE='1')
    native = Path('/usr/bin/clang++')
    clang = SDK / 'upstream/bin/clang++'
    linker = SDK / 'upstream/bin/wasm-ld'
    node = SDK / 'node/24.19.0_64bit/bin/node'
    if sha(node) != '27db838bb204ef7c21df2931f5656e4c8fb32e6e947f363a402b49714d32b5b1':
        raise RuntimeError('Node identity differs from accepted pin')
    if (SDK / 'upstream/emscripten/emscripten-version.txt').read_text().strip() != '"7.0.0"':
        raise RuntimeError('SDK identity mismatch')
    if (SDK / 'upstream/emscripten/emscripten-revision.txt').read_text().strip() != '777e6e5db7b4990bcaeb1b9998ed642cc84e6629':
        raise RuntimeError('Compiler revision mismatch')
    protected_roots = [REPO / name for name in ('source/src', 'source/enet', 'web/runtime',
        'web/build/out', 'web/server/out', 'web/build/.cache',
        'web/build/generated/t066/attempt-T070-1/bundle')] + [SDK]
    protected = snapshot(protected_roots)
    write_json('protected-before.json', protected)
    sources = [REPO / 'source/outbreak/fixed.h', REPO / 'source/outbreak/fixed.cpp',
               HERE / 'wrapper.cpp', HERE / 'wasm_runner.mjs', Path(__file__).resolve(),
               REPO / 'MVP/SHARED_NUMERIC_FOUNDATION.md', REPO / 'tickets/T078.md']
    inputs = snapshot(sources)
    include = ['-I', str(REPO / 'source/outbreak')]
    common = ['-std=c++11', '-O2', '-Wall', '-Wextra', '-Werror'] + include
    source = str(REPO / 'source/outbreak/fixed.cpp')
    wrapper = str(HERE / 'wrapper.cpp')
    commands = [
        [str(native)] + common + ['-DT078_NATIVE', source, wrapper, '-o', str(ATTEMPT / 'native')],
        [str(clang), '--target=wasm32-unknown-emscripten', '--sysroot=' + str(cache / 'sysroot')]
        + common + ['-c', source, '-o', str(ATTEMPT / 'fixed.o')],
        [str(clang), '--target=wasm32-unknown-emscripten', '--sysroot=' + str(cache / 'sysroot')]
        + common + ['-c', wrapper, '-o', str(ATTEMPT / 'wrapper.o')],
        [str(linker), '--no-entry', '--export=run', '--export=root', '--export=result_x',
         '--export=result_y', str(ATTEMPT / 'fixed.o'), str(ATTEMPT / 'wrapper.o'),
         '-o', str(ATTEMPT / 'numeric.wasm')]]
    write_json('plan.json', dict(environment=env, commands=commands, inputs=inputs,
        tools=snapshot([native, clang, linker, node, Path(sys.executable).resolve()]),
        platform=platform.platform(), machine=platform.machine(), python=sys.version,
        execution=[[str(ATTEMPT / 'native')], [str(node), str(HERE / 'wasm_runner.mjs'),
                    str(ATTEMPT / 'numeric.wasm')]], batch_limit=4096,
        link_dependencies='Only fixed.o and wrapper.o; no runtime library or imports'))
    # Copy only frozen sysroot: no Emscripten driver or port builder is invoked.
    shutil.copytree(REPO / 'web/build/.cache/sysroot', cache / 'sysroot', symlinks=True)
    if snapshot([REPO / 'web/build/.cache/sysroot']) != {
        str(REPO / 'web/build/.cache/sysroot' / Path(p).relative_to(cache / 'sysroot')): v
        for p, v in snapshot([cache / 'sysroot']).items()}:
        raise RuntimeError('Sysroot copy mismatch')
    for index, command in enumerate(commands):
        result = subprocess.run(command, cwd=REPO, env=env, capture_output=True, timeout=60)
        (ATTEMPT / 'logs' / f'build-{index}.stdout').write_bytes(result.stdout)
        (ATTEMPT / 'logs' / f'build-{index}.stderr').write_bytes(result.stderr)
        if result.returncode:
            raise RuntimeError(f'Build {index} failed; no flag/library fallback authorized')
    for tool in (native, clang, linker, node):
        result = subprocess.run([str(tool), '--version'], cwd=REPO, env=env,
                                capture_output=True, timeout=10, check=True)
        (ATTEMPT / 'logs' / (tool.name + '.version')).write_bytes(result.stdout + result.stderr)
    executions = [[str(ATTEMPT / 'native')],
                  [str(node), str(HERE / 'wasm_runner.mjs'), str(ATTEMPT / 'numeric.wasm')]]
    count, batches, failures = 0, 0, []
    counts = {str(op): 0 for op in range(9)}
    iterator = iter(cases())
    with (ATTEMPT / 'corpus.txt').open('w') as corpus, \
         (ATTEMPT / 'expected.txt').open('w') as expected_file, \
         (ATTEMPT / 'native.txt').open('w') as native_file, \
         (ATTEMPT / 'wasm.txt').open('w') as wasm_file:
        while True:
            batch = list(itertools.islice(iterator, 4096))
            if not batch:
                break
            payload = ''.join(' '.join(map(str, case)) + '\n' for case in batch)
            expected = ''.join(' '.join(map(str, oracle(case))) + '\n' for case in batch)
            corpus.write(payload)
            expected_file.write(expected)
            for target, command in enumerate(executions):
                result = subprocess.run(command, cwd=REPO, env=env, input=payload,
                                        capture_output=True, text=True, timeout=30)
                (native_file if target == 0 else wasm_file).write(result.stdout)
                if result.returncode or result.stderr:
                    raise RuntimeError(f'Target {target}, batch {batches}: {result.stderr[:2000]}')
                if result.stdout != expected:
                    actual = result.stdout.splitlines()
                    wanted = expected.splitlines()
                    if len(actual) != len(wanted):
                        raise RuntimeError('Output record count differs')
                    for offset, (got, want) in enumerate(zip(actual, wanted)):
                        if got != want and len(failures) < 16:
                            failures.append(dict(target=target, index=count+offset,
                                                 case=batch[offset], actual=got, expected=want))
            for case in batch:
                counts[str(case[0])] += 1
            count += len(batch)
            batches += 1
    after = snapshot(protected_roots)
    write_json('protected-after.json', after)
    changed = [p for p in sorted(set(protected) | set(after)) if protected.get(p) != after.get(p)]
    input_changes = snapshot(sources) != inputs
    hashes = snapshot([ATTEMPT / name for name in
        ('corpus.txt', 'expected.txt', 'native.txt', 'wasm.txt', 'native', 'fixed.o', 'wrapper.o', 'numeric.wasm')])
    passed = not failures and not changed and not input_changes
    write_json('result.json', dict(passed=passed, cases=count, batches=batches, by_operation=counts,
        failures=failures, protected_files=len(protected), changed_protected=changed,
        inputs_changed=input_changes, hashes=hashes, exact_native_wasm_oracle=True if not failures else False))
    print(json.dumps(dict(passed=passed, cases=count, batches=batches,
                         failures=len(failures), changed_protected=len(changed))))
    return 0 if passed else 1


if __name__ == '__main__':
    sys.exit(main())
