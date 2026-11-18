#!/usr/bin/env python3
"""Copy entry.png to /output/entry.png (make.fun news-image-20261117 r3).

Python 3.13 standard library only. No network access.
Deterministic: running twice produces byte-identical output.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST = "/output/entry.png"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    if not os.path.isfile(SRC):
        print(f"missing {SRC}; run build.py first", file=sys.stderr)
        return 1
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    shutil.copyfile(SRC, DST)
    print(f"copied {SRC} -> {DST}")
    print(f"bytes={os.path.getsize(DST)} sha256={sha256(DST)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
