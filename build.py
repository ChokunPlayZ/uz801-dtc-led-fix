#!/usr/bin/env python3
"""Compile the LED-only correction against an operator-supplied Linux DTB."""

import argparse
from pathlib import Path
import shutil
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--original", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True, help="New directory; existing paths are refused")
    args = parser.parse_args()
    original = args.original.resolve()
    if not original.is_file():
        parser.error("Supply the original Linux DTB for your confirmed board/kernel")
    dtc = shutil.which("dtc")
    if dtc is None:
        parser.error("dtc is required")
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    subprocess.run([dtc, "-q", "-I", "dtb", "-O", "dts", "-o", str(output / "original.dts"), str(original)], check=True)
    source = Path(__file__).resolve().parent / "stock-leds.dts"
    target = output / "msm8916-uz801-stock-leds.dtb"
    subprocess.run([dtc, "-q", "-i", str(output), "-I", "dts", "-O", "dtb", "-o", str(target), str(source)], check=True)
    print(f"Built {target}. No device contacted or boot configuration changed.")


if __name__ == "__main__":
    main()
