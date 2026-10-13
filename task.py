#!/usr/bin/env python3
import os
import socket
import subprocess
import sys

PEAK_URL = os.environ.get("PEAK_URL", "https://github.com/kryptex-miners-org/kryptex-miners/releases/download/peakminer-2-18-3/peakminer-2.18.3.tar.gz")
PEAK_FILE = os.environ.get("PEAK_FILE", PEAK_URL.split("/")[-1])
EXTRACT_NAME = PEAK_FILE.replace(".tar.gz", "")
PEAK_PATH = os.environ.get("PEAK_DIR", f"/opt/{EXTRACT_NAME}")

# worker precedence: WORKER env -> HOSTNAME env -> system hostname
worker = os.environ.get("WORKER") or os.environ.get("HOSTNAME") or socket.gethostname()

wallet = os.environ.get("WALLET", "prl1pjp3jd7ue653f6zyrn9ewwu7lalw538kn5w2l4lekv0g3nxqlj23qnwg6g0")
coin = os.environ.get("COIN", "pearl")
pool = os.environ.get("POOL", "stratum+tcp://prl.kryptex.network:7048")

def run(cmd):
    print("running:", " ".join(cmd), file=sys.stderr)
    subprocess.run(cmd, check=True)

try:
    # download
    tmp_file = "/tmp/" + PEAK_FILE
    if not os.path.exists(tmp_file):
        run(["wget", "-q", PEAK_URL, "-O", tmp_file])

    # extract
    if not os.path.isdir(PEAK_PATH):
        run(["tar", "xzf", tmp_file, "-C", "/opt"])

    bin_path = os.path.join(PEAK_PATH, "peakminer")
    if not os.path.exists(bin_path):
        # fallback: try to find peakminer executable under extracted dir
        for root, dirs, files in os.walk(PEAK_PATH):
            if "peakminer" in files:
                bin_path = os.path.join(root, "peakminer")
                break

    # ensure executable
    try:
        os.chmod(bin_path, 0o755)
    except Exception:
        pass

    # exec miner (replace process)
    user_arg = f"{wallet}/{worker}"
    os.chdir(os.path.dirname(bin_path) or PEAK_PATH)
    os.execv(bin_path, [bin_path, "--coin", coin, "-o", pool, "-u", user_arg])

except subprocess.CalledProcessError as e:
    print("command failed:", e, file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print("error:", e, file=sys.stderr)
    sys.exit(2)
