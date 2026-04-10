---
title: "Building a Python CLI Tool in 30 Minutes"
author: Fu Qilin
categories: [Coding]
tags: [python, cli, automation]
date: 2026-04-05
---

## The Goal

Build a command-line tool that batch-renames files using a pattern. Something like:

```bash
myrename ./photos --pattern "vacation_{i:03d}.jpg" --start 1
```

## Step 1: argparse Setup

```python
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Batch rename files")
    parser.add_argument("directory", help="Target directory")
    parser.add_argument("--pattern", required=True, help="Rename pattern")
    parser.add_argument("--start", type=int, default=1, help="Start index")
    parser.add_argument("--dry-run", action="store_true", help="Preview only")
    return parser.parse_args()
```

## Step 2: Core Logic

```python
from pathlib import Path

def rename_files(directory, pattern, start, dry_run=False):
    files = sorted(Path(directory).iterdir())
    for i, f in enumerate(files, start=start):
        new_name = pattern.format(i=i)
        new_path = f.parent / new_name
        if dry_run:
            print(f"{f.name} → {new_name}")
        else:
            f.rename(new_path)
```

## Step 3: Entry Point

```python
if __name__ == "__main__":
    args = parse_args()
    rename_files(args.directory, args.pattern, args.start, args.dry_run)
```

## Result

```
$ myrename ./photos --pattern "trip_{i:03d}.jpg" --dry-run
IMG_001.JPG → trip_001.jpg
IMG_002.JPG → trip_002.jpg
IMG_003.JPG → trip_003.jpg
```

30 minutes, one file, a useful tool. 🎉
