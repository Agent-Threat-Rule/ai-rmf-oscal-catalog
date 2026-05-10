"""
Validate the generated catalog against the official OSCAL v1.2.2 catalog JSON schema.

Uses ajv-cli (Node.js) under the hood because OSCAL's schema includes ECMA-262
regex constructs (e.g., \\p{L} Unicode property classes) that Python's stdlib
re module does not support. ajv-cli is invoked via npx with ajv-formats so that
date-time, uri, and email formats are actually validated (not silently ignored).

Usage:
    python3 src/validate.py
"""

import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO / "schemas" / "oscal_catalog_schema.json"
CATALOG_PATH = REPO / "catalogs" / "ai-rmf-v0.4.json"
LOCAL_AJV = REPO / "node_modules" / ".bin" / "ajv"


def main() -> int:
    if LOCAL_AJV.exists():
        ajv = str(LOCAL_AJV)
    else:
        if shutil.which("npx") is None:
            print("FAIL ajv not installed and npx unavailable; run 'npm install' first")
            return 2
        ajv = None

    if ajv is not None:
        cmd = [ajv, "validate"]
    else:
        cmd = ["npx", "--yes", "ajv-cli@5", "validate"]
    cmd += [
        "-s", str(SCHEMA_PATH),
        "-d", str(CATALOG_PATH),
        "-c", "ajv-formats",
        "--strict=false",
        "--spec=draft7",
    ]

    proc = subprocess.run(cmd, capture_output=True, text=True)

    # ajv prints "X valid" or detailed errors. Surface the result without the
    # noisy "unknown format ..." warnings that come from the schema itself.
    stderr_lines = [
        line for line in (proc.stderr or "").splitlines()
        if line.strip()
        and "unknown format" not in line
        and not line.startswith("npm warn")
    ]
    stdout = (proc.stdout or "").strip()

    if proc.returncode == 0 and "valid" in stdout:
        print(f"OK schema valid: {CATALOG_PATH.name}")
        return 0

    print(f"FAIL schema validation failed (exit {proc.returncode})")
    if stdout:
        print("stdout:")
        for line in stdout.splitlines():
            print(f"  {line}")
    if stderr_lines:
        print("stderr (filtered):")
        for line in stderr_lines[:40]:
            print(f"  {line}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
