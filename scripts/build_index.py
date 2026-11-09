#!/usr/bin/env python3
"""从 articles/2026/*.md 的 frontmatter 生成静态站点 index.html。

用法:
  python3 scripts/build_index.py

生成根目录 index.html:封面卡片 + 摘要 + 分类合集 + 关注入口。
GitHub Pages 直接托管此静态文件,无需 Jekyll,零构建风险。
新增文章后重跑本脚本即可。
"""
import os
import re
import glob

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ART_DIR = os.path.join(REPO, "articles", "2026")
SITE_URL = "https://sl-yang-dl.github.io/wechat-articles-public/"
REPO_URL = "https://github.com/sl-yang-dl/wechat-articles-public"

# 分类合集: 按文件日期前缀归类(与 README 合集保持一致)
CATEGORIES = [
    ("🔥 初三冲刺", ["2026-11-02", "2026-11-06", "2026-11-09"]),
    ("📕 错题与学习方法", ["2026-10-12", "2026-10-16", "2026-10-20"]),
    ("💬 父子沟通与情绪", ["2026-10-22", "2026-10-24", "2026-10-28", "2026-11-03"]),
    ("💰 钱花得值不值", ["2026-10-26"]),
    ("🤔 运营反思", ["2026-10-30", "2026-10-14"]),
]


def parse_frontmatter(text):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    fm = {}
    if not m:
        return fm
    for line in m.group(1).splitlines():
        mm = re.match(r"^([\w-]+):\s*(.*)$", line)
        if not mm:
            continue
        key, val = mm.group(1), mm.group(2).strip()
        val = val.strip('"').strip("'").rstrip(",").strip()
        fm[key] = val
    return fm


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def main():
    arts = []
    for path in glob.glob(os.path.join(ART_DIR, "*.md")):
        with open(path, encoding="utf-8") as f:
            fm = parse_frontmatter(f.read())
        if not fm.get("title"):
            continue
        fm["_file"] = os.path.basename(path)
        arts.append(fm)
    arts.sort(key=lambda a: a.get("date", ""), reverse=True)

    cards = []
    for a in arts:
        cover = a.get("cover", "")
        title = esc(a.get("title", ""))
        summary = esc(a.get("summary", ""))
        mp = a.get("mp_url", "#")
        draft = f"{REPO_URL}/blob/main/articles/2026/{a['_file']}"
        cards.append(f"""
      <article class="card">
        <a class="thumb" href="{mp}" target="_blank" rel="noopener">
          <img src="{cover}" alt="{title}" loading="lazy">
        </a>
        <div class="body">
          <h3><a href="{mp}" target="_blank" rel="noopener">{title}</a></h3>
          <p>{summary}</p>
          <div class="links">
            <a class="btn" href="{mp}" target="_blank" rel="noopener">读公众号原文</a>
            <a class="btn ghost" href="{draft}" target="_blank" rel="noopener">看草稿</a>
          </div>
        </div>
      </article>""")

    # 分类合集(只列有文章的分类)
    cat_html = []
    by_date = {a["_file"][:10]: a for a in arts}
    for name, dates in CATEGORIES:
        items = []
        for d in dates:
            a = by_date.get(d + "-")
            # 文件名形如 2026-11-02-xxx.md, 前缀 2026-11-02-
            a = next((x for x in arts if x["_file"].startswith(d + "-")), None)
            if not a:
                continue
            items.append(
                f'<a href="{a.get("mp_url","#")}" target="_blank" rel="noopener">{esc(a.get("title",""))}</a>'
            )
        if items:
            cat_html.append(f'      <li><b>{name}</b>：{" · ".join(items)}</li>')

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="作业不慌记 · 一个爸爸陪娃整理作业与错题的公开草稿。微信搜一搜「作业不慌记」关注公众号。作业不慌，错题不慌，成长不慌。">
<title>作业不慌记 · 陪娃整理作业与错题的公开草稿</title>
<style>
  :root {{ --ink:#222; --muted:#666; --line:#eee; --brand:#e8543f; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif; color:var(--ink); background:#fafafa; line-height:1.6; }}
  a {{ color:inherit; text-decoration:none; }}
  .wrap {{ max-width:960px; margin:0 auto; padding:0 16px; }}
  header.hero {{ background:linear-gradient(135deg,#fff7f4,#fdeee9); border-bottom:1px solid var(--line); }}
  .hero .wrap {{ display:flex; align-items:center; gap:24px; padding:28px 16px; flex-wrap:wrap; }}
  .hero h1 {{ margin:0 0 6px; font-size:26px; }}
  .hero p {{ margin:0; color:var(--muted); }}
  .hero .qr {{ width:120px; height:120px; border-radius:10px; border:1px solid var(--line); }}
  .search {{ background:var(--brand); color:#fff; border-radius:12px; padding:14px 18px; margin:18px 0; font-size:15px; }}
  .search b {{ font-size:17px; }}
  h2 {{ font-size:20px; margin:28px 0 12px; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(260px,1fr)); gap:16px; }}
  .card {{ background:#fff; border:1px solid var(--line); border-radius:14px; overflow:hidden; display:flex; flex-direction:column; }}
  .card .thumb img {{ width:100%; height:150px; object-fit:cover; display:block; }}
  .card .body {{ padding:12px 14px 14px; display:flex; flex-direction:column; gap:8px; flex:1; }}
  .card h3 {{ margin:0; font-size:16px; line-height:1.4; }}
  .card p {{ margin:0; color:var(--muted); font-size:13px; flex:1; }}
  .links {{ display:flex; gap:8px; }}
  .btn {{ background:var(--brand); color:#fff; padding:7px 12px; border-radius:8px; font-size:13px; }}
  .btn.ghost {{ background:#fff; color:var(--brand); border:1px solid var(--brand); }}
  ul.topics {{ list-style:none; padding:0; margin:0; }}
  ul.topics li {{ padding:8px 0; border-bottom:1px solid var(--line); font-size:14px; }}
  ul.topics a:hover {{ color:var(--brand); }}
  footer.cta {{ background:#fff; border-top:1px solid var(--line); margin-top:32px; }}
  .cta .wrap {{ padding:24px 16px; text-align:center; }}
  .cta img {{ width:130px; height:130px; border-radius:10px; border:1px solid var(--line); margin-top:10px; }}
</style>
</head>
<body>
<header class="hero">
  <div class="wrap">
    <div>
      <h1>作业不慌记</h1>
      <p>一个父亲，陪孩子整理作业和错题的地方。<br>好大儿14岁，闺女4岁。作业不慌，错题不慌，成长不慌。</p>
    </div>
    <img class="qr" src="assets/gh_qrcode.jpg" alt="作业不慌记 公众号二维码">
  </div>
</header>

<div class="wrap">
  <div class="search">🔍 <b>微信搜一搜：作业不慌记</b>　打开微信 → 发现 → 搜一搜 → 输入「作业不慌记」→ 关注公众号</div>

  <h2>全部文章（点击读公众号原文）</h2>
  <div class="grid">{''.join(cards)}
  </div>

  <h2>按主题看</h2>
  <ul class="topics">
{''.join(cat_html)}
  </ul>
</div>

<footer class="cta">
  <div class="wrap">
    <p>作业不慌，错题不慌，成长不慌。</p>
    <p>微信搜一搜「<b>作业不慌记</b>」即可关注；或扫码：</p>
    <img src="assets/gh_qrcode.jpg" alt="作业不慌记 公众号二维码">
  </div>
</footer>
</body>
</html>
"""
    out = os.path.join(REPO, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"generated {out} ({len(arts)} articles)")


if __name__ == "__main__":
    main()
