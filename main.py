# news-image-20261117 entry (Python 3.13, standard library only): copy the
# vendored front-page image beside this file to /output/entry.png. The image
# sums up Tuesday 17 November 2026 in 30 verified stories across six
# continents, with a pinned world map. No network is used. Run it with:
#   mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
import hashlib
import os
import shutil

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
DST = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


os.makedirs(os.path.dirname(DST), exist_ok=True)
shutil.copyfile(SRC, DST)
if sha256(SRC) != sha256(DST):
    raise SystemExit("entry.png copy failed sha256 verification")
print(f"wrote {DST} ({os.path.getsize(DST)} bytes)")
