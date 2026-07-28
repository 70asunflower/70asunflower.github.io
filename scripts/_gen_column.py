import json, urllib.request, re, os

URL = "http://127.0.0.1:61513"
TOKEN = "i9am30nj67ei0zgh"
POSTS = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_posts"))
COL = "20260723212036-m7ty290"
PARENT_SLUG = "the-data-center-as-a-computer-ai-guide"
PARENT_TITLE = "《The Data Center as a Computer》AI 导读"

def call(path, payload=None):
    body = json.dumps(payload or {}, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(URL + path, data=body, method="POST")
    req.add_header("Authorization", "Token " + TOKEN)
    req.add_header("Content-Type", "application/json; charset=utf-8")
    with urllib.request.urlopen(req, timeout=30) as r:
        res = json.loads(r.read().decode("utf-8"))
    if res.get("code") != 0:
        raise RuntimeError(f"{path}: {res.get('msg')}")
    return res.get("data")

def export(idv):
    d = call("/api/export/exportMdContent", {"id": idv})
    if isinstance(d, dict):
        return d.get("content") or d.get("data") or ""
    return str(d)

def slugify(title):
    s = title.strip().lower().replace(".", "-")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-")

def chapter_key(title):
    m = re.match(r"^(\d+(?:\.\d+)*)\s", title)
    if not m:
        return (999,)
    return tuple(int(x) for x in m.group(1).split("."))

def relevel_headings(b):
    """Shift all body headings down by 2 (skip code fences).
    Page is H1, chapter title is H2, so body sections must start at H3."""
    out = []; in_fence = False
    for line in b.split("\n"):
        s = line.strip()
        if s.startswith("```"):
            in_fence = not in_fence; out.append(line); continue
        if in_fence:
            out.append(line); continue
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            new_lvl = min(len(m.group(1)) + 2, 6)
            out.append("#" * new_lvl + " " + m.group(2))
        else:
            out.append(line)
    return "\n".join(out)

# 1) fetch all docs under the column folder path
rows = call("/api/query/sql", {"stmt":
    f"SELECT id, content, path, parent_id, created FROM blocks WHERE box='20260704134822-ehljzrc' AND type='d' AND path LIKE '%{COL}/%'"})
children = [r for r in rows if r["id"] != COL]
children.sort(key=lambda r: chapter_key(r["content"]))

print(f"Found {len(children)} child chapters (in book order):")
for r in children:
    print("  ", chapter_key(r["content"]), r["content"], "->", slugify(r["content"]))

# 2) export + build each child post
results = []  # (action, slug, path)
for idx, r in enumerate(children):
    sid = r["id"]
    title = r["content"].strip()
    slug = slugify(title)
    date = f"{r['created'][:4]}-{r['created'][4:6]}-{r['created'][6:8]}"  # YYYY-MM-DD from SiYuan created (YYYYMMDDHHMMSS)
    raw = export(sid)
    # strip SiYuan front matter + leading H1 title
    body = re.sub(r"^---\n.*?\n---\n", "", raw, flags=re.S)
    body = body.lstrip("\n")
    body = re.sub(r"^# .*\n", "", body, count=1)
    body = relevel_headings(body)  # page=H1, chapter=H2 => body sections start at H3
    body = body.lstrip("\n").rstrip() + "\n"

    prev_t, prev_s = (None, None)
    next_t, next_s = (None, None)
    if idx > 0:
        prev_t = children[idx - 1]["content"].strip()
        prev_s = slugify(prev_t)
    if idx < len(children) - 1:
        next_t = children[idx + 1]["content"].strip()
        next_s = slugify(next_t)

    nav_lines = ["**专栏导航**", ""]
    if prev_t:
        nav_lines.append(f"- ← 上一篇：[{prev_t}](/posts/{prev_s}/)")
    nav_lines.append(f"- 返回：[栏目总览](/posts/{PARENT_SLUG}/)")
    if next_t:
        nav_lines.append(f"- 下一篇：[{next_t} →](/posts/{next_s}/)")
    nav = "\n".join(nav_lines)

    post = (
        "---\n"
        f'title: "{title}"\n'
        "author: Fu Qilin\n"
        "categories: [分布式计算]\n"
        "tags: [distributed-computing, datacenter, wsc, ai-infra]\n"
        f"date: {date}\n"
        f'description: "《The Data Center as a Computer》AI 导读专栏正文：{title}。"\n'
        f'excerpt: "《The Data Center as a Computer》AI 导读专栏正文：{title}。"\n'
        "---\n"
        "<!-- markdownlint-disable MD013 MD025 MD033 -->\n"
        "> 📌 本篇是 **《The Data Center as a Computer》AI 导读** 栏目的正文。\n"
        f"> ← [返回栏目总览](/posts/{PARENT_SLUG}/)\n"
        ">\n"
        "> 说明：本栏目正文内容由 AI 根据原书原文生成，请自行甄别内容真实性。\n"
        "\n"
        f"## {title}\n"
        "\n"
        f"{body}\n"
        "\n"
        f"{nav}\n"
    )

    fname = f"{date}-{slug}.md"
    fpath = os.path.join(POSTS, fname)
    action = "new"
    if os.path.exists(fpath):
        with open(fpath, encoding="utf-8") as f:
            old = f.read()
        if old == post:
            action = "unchanged"
        else:
            action = "updated"
    if action != "unchanged":
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(post)
    results.append((action, fname, title))

print("\n=== child post results ===")
for action, fname, title in results:
    print(f"  [{action:9}] {fname}")

# 3) update parent chapter list
parent_path = os.path.join(POSTS, f"2026-07-23-{PARENT_SLUG}.md")
with open(parent_path, encoding="utf-8") as f:
    parent_txt = f.read()
head, sep, tail = parent_txt.partition("## 本栏目正文")
if sep:
    bullets = "\n".join(f"- [{r['content'].strip()}](/posts/{slugify(r['content'].strip())}/)" for r in children)
    new_parent = head + sep + "\n\n" + bullets + "\n"
    if new_parent != parent_txt:
        with open(parent_path, "w", encoding="utf-8") as f:
            f.write(new_parent)
        print(f"\n[updated] parent chapter list -> {len(children)} chapters")
    else:
        print("\n[unchanged] parent chapter list")
else:
    print("\n[WARN] parent has no '## 本栏目正文' section")

print("\nDONE")
