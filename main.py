"""news-image-20261123: validate the rendered front page and copy it out.

The entry image is pre-rendered by render.py; this script only checks the
PNG (magic bytes, IHDR size 1024x1024, SHA-256 digest) and copies it to
MAKEFUN_OUTPUT_DIR (or /output when unset). Standard library only, no
network, no clock, no writes outside the output directory.
"""

import hashlib
import os
import shutil
import struct
import sys
from pathlib import Path

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
EXPECTED_SIZE = (1024, 1024)


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)


def inspect_png(path):
    """Check magic + IHDR and return (width, height, sha256 hex)."""
    blob = path.read_bytes()
    if len(blob) < 33:
        fail(f"source too small to be a PNG: {path}")
    if blob[:8] != PNG_MAGIC:
        fail(f"source is not a PNG file: {path}")
    chunk_len = struct.unpack(">I", blob[8:12])[0]
    chunk_type = blob[12:16]
    if chunk_type != b"IHDR" or chunk_len != 13:
        fail(f"source has no valid IHDR chunk: {path}")
    width, height = struct.unpack(">II", blob[16:24])
    digest = hashlib.sha256(blob).hexdigest()
    return width, height, digest


def main():
    script_dir = Path(__file__).resolve().parent
    source = script_dir / "entry.png"
    if not source.is_file():
        fail(f"source not found: {source}")

    width, height, digest = inspect_png(source)
    if (width, height) != EXPECTED_SIZE:
        fail(f"source is {width}x{height}, expected 1024x1024: {source}")
    print(f"source ok: {width}x{height} sha256 {digest}")

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    destination = Path(output_dir) / "entry.png"
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)

    out_width, out_height, out_digest = inspect_png(destination)
    if (out_width, out_height) != EXPECTED_SIZE or out_digest != digest:
        fail("verification failed: output does not match source")
    print(f"copied and verified {destination} sha256 {out_digest}")


if __name__ == "__main__":
    main()
