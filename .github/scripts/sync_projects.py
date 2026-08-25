#!/usr/bin/env python3
"""Sync repo stats (stars/pushed_at/language) into _data/projects_stats.json.

Reads the repo list from _data/projects.yml (simple `repo:` entries) and
queries the GitHub REST API with the workflow's GITHUB_TOKEN.
"""
import json
import os
import re
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LIST_PATH = os.path.join(ROOT, "_data", "projects.yml")
OUT_PATH = os.path.join(ROOT, "_data", "projects_stats.json")

token = os.environ.get("GH_TOKEN", "")


def fetch(repo: str) -> dict:
    req = urllib.request.Request(
        f"https://api.github.com/repos/{repo}",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "User-Agent": "projects-sync",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        d = json.load(r)
    return {
        "name": d.get("name"),
        "description": d.get("description"),
        "language": d.get("language"),
        "stars": d.get("stargazers_count", 0),
        "pushed_at": (d.get("pushed_at") or "")[:10],
        "url": d.get("html_url"),
    }


def main() -> None:
    repos = []
    with open(LIST_PATH, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"-\s*repo:\s*(\S+)", line)
            if m:
                repos.append(m.group(1))

    stats = {}
    for repo in repos:
        try:
            stats[repo] = fetch(repo)
            print(f"ok  {repo}: stars={stats[repo]['stars']} pushed={stats[repo]['pushed_at']}")
        except Exception as e:  # noqa: BLE001 - keep old data on per-repo failure
            print(f"err {repo}: {e}")

    if not stats and os.path.exists(OUT_PATH):
        # 全部拉取失败（如网络/API 故障）时保留旧数据，避免用空文件覆盖
        print("all fetches failed; keeping existing", OUT_PATH)
        return

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"wrote {OUT_PATH} ({len(stats)} repos)")


if __name__ == "__main__":
    main()
