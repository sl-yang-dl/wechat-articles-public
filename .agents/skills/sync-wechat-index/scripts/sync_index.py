#!/usr/bin/env python3
"""同步 wechat-articles-public 站点索引。

发布新文章后,在本仓库根目录运行:
  python3 .agents/skills/sync-wechat-index/scripts/sync_index.py sync

子命令:
  migrate   给历史文章补 category 字段到 front matter(一次性)
  thumbs    用 sips 为缺失缩略图的封面生成 covers/thumbs/*.png
  check     检查封面/缩略图/mp_url 缺失
  sync      重建 index.html(分类映射+主题合集)与 README.md(表格/原文/合集)
"""
import os
import re
import sys
import argparse
import subprocess

ART_DIR = "articles/2026"
COVERS = "covers"
THUMBS = "covers/thumbs"
GH_REPO = "sl-yang-dl/wechat-articles-public"

# 合集顺序与对应 emoji(改这里即可调整首页/README 的合集顺序与图标)
CATEGORIES = ["初三冲刺", "错题与学习方法", "父子沟通与情绪", "钱花得值不值", "运营反思"]
EMOJI = {
    "初三冲刺": "🔥",
    "错题与学习方法": "📕",
    "父子沟通与情绪": "💬",
    "钱花得值不值": "💰",
    "运营反思": "🤔",
}
# 仅用于 migrate:历史文章 date -> 分类(一次性补 front matter 后不再需要)
LEGACY = {
    "2026-11-02": "初三冲刺", "2026-11-06": "初三冲刺", "2026-11-09": "初三冲刺",
    "2026-10-12": "错题与学习方法", "2026-10-16": "错题与学习方法", "2026-10-20": "错题与学习方法",
    "2026-10-22": "父子沟通与情绪", "2026-10-24": "父子沟通与情绪", "2026-10-28": "父子沟通与情绪", "2026-11-03": "父子沟通与情绪",
    "2026-10-26": "钱花得值不值", "2026-10-30": "运营反思", "2026-10-14": "运营反思",
}


def parse_front_matter(path):
    text = open(path, encoding="utf-8").read()
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    fm = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" not in line:
                continue
            k, v = line.split(":", 1)
            k, v = k.strip(), v.strip()
            if v.startswith('"') and v.endswith('"'):
                v = v[1:-1]
            fm[k] = v
    return fm, text


def load_articles(repo):
    d = os.path.join(repo, ART_DIR)
    arts = []
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".md"):
            continue
        p = os.path.join(d, fn)
        fm, _ = parse_front_matter(p)
        base = fn[:-3]
        arts.append({
            "file": fn,
            "base": base,
            "title": fm.get("title", ""),
            "date": fm.get("date", ""),
            "mp_url": (fm.get("mp_url", "") or "").strip().strip('"'),
            "category": (fm.get("category", "") or "").strip(),
        })
    arts.sort(key=lambda a: a["date"], reverse=True)
    return arts


def cat_of(a):
    return a["category"] or "随笔"


def link_of(a):
    if a["mp_url"]:
        return a["mp_url"]
    return f"https://github.com/{GH_REPO}/blob/main/{ART_DIR}/{a['file']}"


# ---------------- index.html ----------------
def cats_line(arts):
    parts = []
    for a in sorted(arts, key=lambda a: a["date"]):
        c = cat_of(a)
        if c == "随笔":
            continue
        parts.append(f"{a['date']}:{c}")
    return '{% assign cats = "' + "|".join(parts) + '" | split: "|" %}'


def topics_ul_inner(arts):
    groups = {c: [] for c in CATEGORIES}
    for a in arts:
        c = cat_of(a)
        if c in groups:
            groups[c].append(a)
    lis = []
    for c in CATEGORIES:
        items = groups.get(c, [])
        if not items:
            continue
        items.sort(key=lambda a: a["date"], reverse=True)
        links = [f'<a href="{link_of(a)}" target="_blank" rel="noopener">{a["title"]}</a>' for a in items]
        lis.append(f'    <li><span class="cat">{EMOJI[c]} {c}</span>' + " · ".join(links) + "</li>")
    return "\n".join(lis)


def rebuild_index(repo, arts):
    p = os.path.join(repo, "index.html")
    html = open(p, encoding="utf-8").read()
    html = re.sub(
        r'\{%-?\s*assign\s+cats\s*=\s*".*?"\s*\|\s*split:\s*"\|"\s*-?%\}',
        cats_line(arts), html, flags=re.S)
    html = re.sub(
        r'(<ul class="topics">)(.*?)(</ul>)',
        lambda m: m.group(1) + "\n" + topics_ul_inner(arts) + "\n" + m.group(3),
        html, count=1, flags=re.S)
    open(p, "w", encoding="utf-8").write(html)
    print("updated index.html")


# ---------------- README.md ----------------
def replace_section(text, header, new_body):
    """用 new_body 替换 header 标题下、到下一个 '## ' 或 '---' 之间的内容。"""
    lines = text.split("\n")
    res, i, n = [], 0, len(lines)
    while i < n:
        line = lines[i]
        if line.strip() == header:
            res.append(line)
            i += 1
            while i < n and not (lines[i].startswith("## ") or lines[i].strip() == "---"):
                i += 1
            res.extend(new_body)
            if res and res[-1] != "":
                res.append("")
            continue
        res.append(line)
        i += 1
    return "\n".join(res)


def table_body(arts):
    rows = ["| 日期 | 标题 | 封面 |", "| --- | --- | --- |"]
    for a in arts:
        title_md = f'[{a["title"]}]({link_of(a)})'
        thumb = f'[<img src="covers/thumbs/{a["base"]}.png" width="140" alt="封面">](covers/{a["base"]}.png)'
        rows.append(f'| {a["date"]} | {title_md} | {thumb} |')
    return rows


def topics_body(arts):
    groups = {c: [] for c in CATEGORIES}
    for a in arts:
        c = cat_of(a)
        if c in groups:
            groups[c].append(a)
    rows = [f"换个角度看这 {len(arts)} 篇（点击跳转公众号）：", ""]
    for c in CATEGORIES:
        items = groups.get(c, [])
        if not items:
            continue
        items.sort(key=lambda a: a["date"], reverse=True)
        links = [f'[{a["title"]}]({link_of(a)})' for a in items]
        rows.append(f'- {EMOJI[c]} **{c}**：' + " · ".join(links))
    return rows


def source_body(arts):
    rows = ["点击在新窗口打开仓库内的 .md 源文件（文件名以日期开头，已按时间倒序排列）：", ""]
    for a in arts:
        rows.append(f'- <a href="{ART_DIR}/{a["file"]}" target="_blank">{a["file"]}</a>')
    return rows


def rebuild_readme(repo, arts):
    p = os.path.join(repo, "README.md")
    md = open(p, encoding="utf-8").read()
    md = replace_section(md, "## 文章（公众号）", table_body(arts))
    md = replace_section(md, "## 主题合集", topics_body(arts))
    md = replace_section(md, "## 原文（仓库 .md 草稿）", source_body(arts))
    open(p, "w", encoding="utf-8").write(md)
    print("updated README.md")


# ---------------- 其它 ----------------
def make_thumbs(repo):
    src = os.path.join(repo, COVERS)
    dst = os.path.join(repo, THUMBS)
    os.makedirs(dst, exist_ok=True)
    for fn in os.listdir(src):
        if not fn.lower().endswith(".png"):
            continue
        out = os.path.join(dst, fn)
        if os.path.exists(out):
            continue
        try:
            subprocess.run(["sips", "-Z", "600", os.path.join(src, fn), "--out", out],
                           check=True, capture_output=True)
            print("thumb:", fn)
        except Exception as e:  # noqa
            print("thumb FAILED:", fn, e)


def migrate(repo):
    d = os.path.join(repo, ART_DIR)
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".md"):
            continue
        p = os.path.join(d, fn)
        text = open(p, encoding="utf-8").read()
        m = re.match(r"^(---\s*\n)(.*?)(\n---\s*\n)", text, re.S)
        if not m:
            print("no front matter:", fn)
            continue
        block = m.group(2)
        if re.search(r"^category\s*:", block, re.M):
            continue
        dm = re.search(r"^date:\s*(\S+)", block, re.M)
        date = dm.group(1) if dm else ""
        cat = LEGACY.get(date)
        if not cat:
            print("skip (no legacy cat):", fn)
            continue
        if re.search(r"^status:", block, re.M):
            block = re.sub(r"^(status:.*)$", r"\1\ncategory: " + cat, block, flags=re.M)
        else:
            block = re.sub(r"^(date:.*)$", r"\1\ncategory: " + cat, block, flags=re.M)
        open(p, "w", encoding="utf-8").write(m.group(1) + block + m.group(3) + text[m.end():])
        print("category =", cat, fn)


def check(repo, arts):
    for a in arts:
        cover = os.path.join(repo, COVERS, a["base"] + ".png")
        thumb = os.path.join(repo, THUMBS, a["base"] + ".png")
        warn = []
        if not os.path.exists(cover):
            warn.append("封面缺失")
        if not os.path.exists(thumb):
            warn.append("缩略图缺失")
        if not a["mp_url"]:
            warn.append("mp_url 空(合集/表格暂用原稿链接)")
        if warn:
            print(f"- {a['date']} {a['title']}: {', '.join(warn)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["sync", "migrate", "thumbs", "check"])
    ap.add_argument("--repo", default=".")
    args = ap.parse_args()
    repo = args.repo
    if args.cmd == "migrate":
        migrate(repo)
        return
    if args.cmd == "thumbs":
        make_thumbs(repo)
        return
    arts = load_articles(repo)
    if args.cmd == "check":
        check(repo, arts)
        return
    if args.cmd == "sync":
        rebuild_index(repo, arts)
        rebuild_readme(repo, arts)
        print("done. 缺失项:")
        check(repo, arts)


if __name__ == "__main__":
    main()
