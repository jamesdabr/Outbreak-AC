#!/usr/bin/env python3
"""Compile real engine client translation units; never link or launch a game."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shlex
import subprocess
import sys

sys.dont_write_bytecode = True
from preflight import CONFIG, ROOT, inspect_sdk


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_path(relative):
    path = ROOT / relative
    if path.is_symlink() or any(p.is_symlink() for p in path.parents if p != ROOT.parent):
        raise ValueError(f"Refusing symlinked output/cache path: {path}")
    if not path.resolve().is_relative_to(ROOT / "web/build"):
        raise ValueError(f"Output/cache escapes web/build: {path}")
    return path


def native_outputs():
    return {str(p.relative_to(ROOT)): digest(p) for p in (ROOT / "source").rglob("*")
            if p.is_file() and (p.suffix in (".o", ".lo", ".a", ".gch", ".pch") or p.name in ("ac_client", "ac_server", "ac_master"))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sdk-root", help="Existing pinned emsdk root")
    parser.add_argument("--dependency-authorization", type=Path,
                        help="Existing lead decision authorizing inspected SDK execution and exact port acquisition/cache setup")
    parser.add_argument("--units", nargs="+", choices=("clientgame", "main", "server"),
                        help="Subset of configured real sources (default: all)")
    args = parser.parse_args()
    config = json.loads(CONFIG.read_text())
    if args.units:
        config["translation_units"] = [u for u in config["translation_units"] if u["name"] in args.units]
    output = safe_path(config["output"])
    cache = safe_path(config["cache"])
    output.mkdir(parents=True, exist_ok=True)
    for name in ("result.json", "compiler-version.log"):
        safe_path(str((output / name).relative_to(ROOT)))
    # Remove only our previous object results, so failed reruns cannot leave stale successes.
    for mode in config["configurations"]:
        for unit in config["translation_units"]:
            target = safe_path(str((output / f"{mode}-{unit['name']}.o").relative_to(ROOT)))
            safe_path(str((output / f"{mode}-{unit['name']}.log").relative_to(ROOT)))
            target.unlink(missing_ok=True)
    report = {
        "scope": "object_compilation_only", "status": "blocked", "host": platform.platform(),
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "source_commit": subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, text=True, stdout=subprocess.PIPE).stdout.strip(),
        "config_sha256": digest(CONFIG), "preflight": inspect_sdk(args.sdk_root), "runs": [],
        "source_identity": {str(p.relative_to(ROOT)): digest(p)
                            for p in (ROOT / "source/src").rglob("*") if p.is_file() and p.suffix in (".h", ".cpp")},
        "claims": {"linked_runtime": False, "renderer": False, "browser_session": False, "network": False},
        "native_outputs_before": native_outputs(),
    }
    compiler = report["preflight"]["tools"]["em++"]
    report["planned_commands"] = [
        [compiler] + config["common_flags"] + config["port_flags"] + mode_flags + unit["flags"] +
        ["-I" + str(ROOT / inc) for inc in config["includes"]] +
        ["-c", str(ROOT / unit["source"]), "-o", str(output / f"{mode}-{unit['name']}.o")]
        for mode, mode_flags in config["configurations"].items() for unit in config["translation_units"]
    ]
    result = output / "result.json"

    def finish(code, reason):
        report["reason"] = reason
        report["native_outputs_after"] = native_outputs()
        report["native_outputs_unchanged"] = report["native_outputs_before"] == report["native_outputs_after"]
        report["finished_utc"] = datetime.now(timezone.utc).isoformat()
        result.write_text(json.dumps(report, indent=2) + "\n")
        print(f"{report['status']}: {reason}\nEvidence: {result}")
        return code

    if report["preflight"]["errors"]:
        return finish(2, "; ".join(report["preflight"]["errors"]))
    authorization = args.dependency_authorization
    if not authorization or not authorization.is_file():
        return finish(2, "SDK execution/first-use dependency setup lacks a recorded lead authorization; no compiler executed")
    report["dependency_authorization"] = {"path": str(authorization.resolve()), "sha256": digest(authorization)}
    # An evidence path records approval; the operator must check its authority/scope.
    # It is not an automatic permission grant merely because a file exists.
    cache.mkdir(parents=True, exist_ok=True)
    temporary = safe_path(str((output / "tmp").relative_to(ROOT)))
    temporary.mkdir(exist_ok=True)
    # Explicit clean child environment prevents inherited compiler/cache hooks.
    env = {"PATH": "/usr/bin:/bin:/usr/sbin:/sbin", "EMSDK_PYTHON": sys.executable}
    env.update({"EMSDK": report["preflight"]["sdk_root"], "EM_CONFIG": report["preflight"]["em_config"],
                "EM_CACHE": str(cache), "EMCC_TEMP_DIR": str(temporary), "TMPDIR": str(temporary),
                "EM_PORTS": str(cache / "ports"), "NODE_COMPILE_CACHE": str(cache / "node_compile_cache"),
                "PYTHONDONTWRITEBYTECODE": "1"})
    report["environment_overrides"] = env.copy()
    version_command = [compiler, "--version"]
    version = subprocess.run(version_command, cwd=ROOT, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (output / "compiler-version.log").write_text(version.stdout)
    report["compiler_version"] = {"command": version_command, "exit_code": version.returncode, "output": version.stdout}
    version_match = re.search(r"^emcc .*?\) (\d+\.\d+\.\d+) \(([0-9a-f]+)\)", version.stdout, re.MULTILINE)
    if version.returncode or not version_match or version_match.group(1) != config['sdk']['version'] or version_match.group(2) != config['sdk']['compiler_revision']:
        return finish(2, "Compiler identity command failed or differs from the approved SDK pin")
    for mode, mode_flags in config["configurations"].items():
        for unit in config["translation_units"]:
            obj = output / f"{mode}-{unit['name']}.o"
            log = output / f"{mode}-{unit['name']}.log"
            command = ([compiler] + config["common_flags"] + config["port_flags"] + mode_flags + unit["flags"] +
                       ["-I" + str(ROOT / inc) for inc in config["includes"]] +
                       ["-c", str(ROOT / unit["source"]), "-o", str(obj)])
            print(shlex.join(command), flush=True)
            source_before = digest(ROOT / unit["source"])
            completed = subprocess.run(command, cwd=ROOT, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            log.write_text(completed.stdout)
            wasm = obj.is_file() and obj.read_bytes()[:8] == b"\x00asm\x01\x00\x00\x00"
            report["runs"].append({"mode": mode, "source": unit["source"], "command": command,
                                   "exit_code": completed.returncode, "diagnostic_log": str(log.relative_to(ROOT)),
                                   "object": str(obj.relative_to(ROOT)), "wasm_object": wasm,
                                   "source_sha256_before": source_before,
                                   "source_sha256_after": digest(ROOT / unit["source"]),
                                   "object_sha256": digest(obj) if obj.is_file() else None,
                                   "status": "PASS" if completed.returncode == 0 and wasm and source_before == digest(ROOT / unit["source"]) else "FAIL"})
    passed = all(run["status"] == "PASS" for run in report["runs"]) and report["native_outputs_before"] == native_outputs()
    report["status"] = "pass" if passed else "fail"
    return finish(0 if passed else 1, "Real engine release/debug object compilation only; see individual diagnostics")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError) as error:
        print(f"Probe error: {error}", file=sys.stderr)
        sys.exit(2)
