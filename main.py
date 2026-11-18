#!/usr/bin/env python3
"""news-image-20261117 round 2: write the front page to /output/entry.png.

The image (entry.png) is drawn at build time by build.py with Pillow and
committed beside this program. The grader runs with no network and only
the Python standard library, so this entrypoint simply copies the file.
Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    src = os.path.join(here, "entry.png")
    dst = os.path.join(outdir, "entry.png")
    shutil.copyfile(src, dst)
    with open(dst, "rb") as f:
        head = f.read(8)
    assert head[:4] == b"\x89PNG", "entry.png is not a PNG"
    assert os.path.getsize(dst) <= 1048576, "entry.png over 1 MiB"
    print("wrote %s (%d bytes)" % (dst, os.path.getsize(dst)))


if __name__ == "__main__":
    main()
