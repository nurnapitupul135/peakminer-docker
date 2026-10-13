#!/usr/bin/env python3
import hashlib
import os
import sys
import subprocess

URL = os.environ.get("PEAK_URL", "").strip()
ARCHIVE = os.environ.get("PEAK_FILE", "peakminer.tar.gz").strip()
EXPECTED_SHA256 = os.environ.get("PEAK_SHA256", "").strip()
RAW_ARGS = os.environ.get("PEAK_ARGS", "").strip()

def run(cmd):
    print("+ " + " ".join(cmd), flush=True)
    subprocess.check_call(cmd)

def sha256_of_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()

def find_miner_binary():
    if os.path.exists("./peakminer"):
        return "./peakminer"

    for root, _, files in os.walk("."):
        if "peakminer" in files:
            return os.path.join(root, "peakminer")

    return ""

def main():
    if not URL:
        print("PEAK_URL environment variable is required.", file=sys.stderr)
        sys.exit(2)

    if not os.path.exists(ARCHIVE):
        run(["wget", "-O", ARCHIVE, URL])
    else:
        print(f"{ARCHIVE} already exists; skipping download.", flush=True)

    if EXPECTED_SHA256:
        actual = sha256_of_file(ARCHIVE)
        print(f"Expected SHA256: {EXPECTED_SHA256}", flush=True)
        print(f"Actual SHA256:   {actual}", flush=True)
        if actual.lower() != EXPECTED_SHA256.lower():
            print("Checksum mismatch. Aborting.", file=sys.stderr)
            sys.exit(3)
        print("Checksum OK.", flush=True)

    if os.path.exists(ARCHIVE):
        run(["tar", "xzf", ARCHIVE])

    miner = find_miner_binary()
    if not miner:
        print("Could not find peakminer binary after extraction.", file=sys.stderr)
        sys.exit(4)

    os.chmod(miner, 0o755)

    if not RAW_ARGS:
        print("PEAK_ARGS is empty. No miner command will be executed.", file=sys.stderr)
        sys.exit(5)

    argv = [miner] + RAW_ARGS.split()
    print("Executing:", " ".join(argv), flush=True)
    os.execv(miner, argv)

if __name__ == "__main__":
    main()
