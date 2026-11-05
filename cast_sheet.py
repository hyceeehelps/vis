#!/usr/bin/env python3
"""Generate cast_sheet.png — the one-image "no drift" QC for the recurring cast.

    python3 cast_sheet.py [out.png]

Run after any edit to cast_defs.py. Every character is drawn in a neutral pose from
the same code path scenes use, so if the sheet looks right, the episode looks right.
"""
import sys
import cast_engine

if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else 'cast_sheet.png'
    print(cast_engine.cast_sheet(path=out))
