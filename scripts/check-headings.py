#!/usr/bin/env python3
"""Guardrail: ensure no post body contains a stray H1 (# ) heading.

The Chirpy theme already renders the page title as the single <h1> from the
front matter `title:` field. Any `# ` heading inside a post body therefore
produces a SECOND <h1> on the page -> broken document outline / a11y / SEO.

This script scans every _posts/*.md, strips YAML front matter, ignores fenced
code blocks, and fails (exit 1) if any H1 is found in a body. Session headings
must start at H2 (## ). Column chapters keep their title at H2; the generator
already re-levels SiYuan exports by +2 so the body sections land at H3+.

Usage: python scripts/check-headings.py
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS = os.path.join(ROOT, "_posts")
NL = chr(10)

H1_LINE = re.compile(r"^#\s+\S")
FENCE = re.compile(r"^\s*```")
FM_SPLIT = re.compile(r"^---\s*" + NL, re.M)


def body_of(path):
    txt = open(path, encoding="utf-8").read()
    # Strip front matter if present (delimited by a leading --- line).
    if txt.lstrip().startswith("---"):
        parts = FM_SPLIT.split(txt, maxsplit=1)
        # parts[0] is text before first ---, parts[1] is inside+after fm
        if len(parts) >= 2:
            # drop the front matter block up to the closing ---
            rest = parts[1].split(NL, 1)
            txt = rest[1] if len(rest) > 1 else ""
    return txt


def find_stray_h1(path):
    body = body_of(path)
    in_fence = False
    hits = []
    for i, line in enumerate(body.splitlines(), 1):
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if H1_LINE.match(line):
            hits.append((i, line.strip()))
    return hits


def main():
    files = sorted(glob.glob(os.path.join(POSTS, "*.md")))
    offenders = {}
    for f in files:
        hits = find_stray_h1(f)
        if hits:
            offenders[os.path.basename(f)] = hits

    if not offenders:
        print("OK: 0 stray H1 headings in any post body.")
        return 0

    total = sum(len(v) for v in offenders.values())
    print(f"FAIL: {total} stray H1 heading(s) in {len(offenders)} post(s):")
    for name, hits in offenders.items():
        print(f"  {name}")
        for ln, txt in hits[:5]:
            print(f"    L{ln}: {txt[:80]}")
        if len(hits) > 5:
            print(f"    ... +{len(hits) - 5} more")
    print("\nFix: re-level the body headings down by 1 (## -> ### ...), "
          "skipping code fences, so no # heading remains in the body.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
