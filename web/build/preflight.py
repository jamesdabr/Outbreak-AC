#!/usr/bin/env python3
"""Read-only SDK inspection. Never installs, downloads, or executes SDK code."""
import argparse
import json
import os
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]
CONFIG = Path(__file__).with_name("probe-config.json")


def inspect_sdk(sdk_root=None):
    config = json.loads(CONFIG.read_text())
    requested = sdk_root or os.environ.get("EMSDK")
    if requested:
        root = Path(requested).expanduser().resolve()
        compiler_dir = root / "upstream/emscripten"
    else:
        emcc = shutil.which("emcc")
        compiler_dir = (Path(emcc).resolve().parent if emcc else
                        Path(config["sdk"]["default_root"]) / "upstream/emscripten")
        root = compiler_dir.parent.parent
    errors = []
    tools = {}
    for name in config["sdk"]["required_tools"]:
        path = compiler_dir / name
        tools[name] = str(path)
        if not path.is_file() or not os.access(path, os.X_OK):
            errors.append(f"Missing executable {name}: {path}")
    version_file = compiler_dir / "emscripten-version.txt"
    version_text = version_file.read_text().strip() if version_file.is_file() else None
    version = version_text.strip('\"') if version_text else None
    if version != config["sdk"]["version"]:
        errors.append(f"SDK version: expected {config['sdk']['version']}, found {version!r} ({version_file})")
    em_config = root / ".emscripten"
    if not em_config.is_file():
        errors.append(f"Missing existing local SDK configuration: {em_config}; no automatic activation permitted")
    # Do not execute emcc --version here: first use can initialize SDK state.
    return {
        "scope": config["scope"], "status": "ready_for_authorized_probe" if not errors else "missing_prerequisites",
        "sdk_root": str(root), "compiler_dir": str(compiler_dir), "tools": tools,
        "sdk_version_file": str(version_file), "sdk_version": version,
        "expected_sdk": config["sdk"], "em_config": str(em_config),
        "release_metadata_verified_locally": False,
        "compiler_version_executed": False,
        "dependencies_verified": False,
        "effective_flags": config["common_flags"] + config["port_flags"],
        "errors": errors,
        "next_step": "Provide the approved pinned SDK and a lead-recorded dependency/setup authorization before compiler execution. Preflight performs no acquisition or port checks."
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sdk-root", help="Existing emsdk root (otherwise EMSDK, PATH, then task-local root)")
    parser.add_argument("--json", action="store_true", help="Print machine-readable report to stdout")
    args = parser.parse_args()
    report = inspect_sdk(args.sdk_root)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"T016: {report['status']} (expected Emscripten {report['expected_sdk']['version']})")
        print(f"SDK root: {report['sdk_root']}")
        for error in report["errors"]:
            print(f"ERROR: {error}")
        print(report["next_step"])
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
