---
name: sync-wechat-index
description: >-
  发布公众号新文章到 wechat-articles-public 仓库后,自动同步站点索引。
  当用户说"加了篇新文""同步站点索引""发布后更新首页/README",或往 articles/2026 新增 .md 后使用。
  负责重建 index.html 的分类映射与主题合集、README.md 的文章表格/原文链接/主题合集,并生成封面缩略图、检查缺失项。
---

# 同步站点索引 (sync-wechat-index)

在 `wechat-articles-public` 仓库发布新文章后,用本技能一键把文章挂上首页与 README,避免手工改 `index.html` / `README.md` 出错。

## 何时使用

- 用户在 `articles/2026/` 新增了一篇 `.md`。
- 用户说"同步一下站点""更新首页/README""加完文章帮我挂上"。

## 文章 front matter 约定

每篇文章头部需包含(参考既有文章):

```yaml
---
title: 文章标题
date: 2026-11-11
status: published
mp_url: "https://mp.weixin.qq.com/s/xxxx"   # 公众号发出后回填;留空则合集/表格暂用 GitHub 原稿链接
cover: "covers/2026-11-11-标题.png"          # 2.35:1 封面
summary: 一句话摘要,显示在首页卡片
search_words: 关键词1, 关键词2
category: 初三冲刺   # 可选值见下;缺省归为「随笔」(不进合集)
---
```

`category` 可选值(决定首页卡片标签与合集分组,顺序即合集展示顺序):

- `初三冲刺`
- `错题与学习方法`
- `父子沟通与情绪`
- `钱花得值不值`
- `运营反思`
- (缺省) `随笔` —— 显示「随笔」标签,不进入主题合集

并把封面图放到 `covers/2026-11-11-标题.png`(文件名须与 `.md` 文件名一致,仅后缀不同)。

## 步骤

在仓库根目录执行脚本 `scripts/sync_index.py`(路径相对于本技能目录):

1. **(首次/补历史) 迁移分类** —— 仅当历史文章还没有 `category` 字段时跑一次:
   ```bash
   python3 .agents/skills/sync-wechat-index/scripts/sync_index.py migrate
   ```
   它会按日期把 `初三冲刺` 等分类写回各文章 front matter(一次性,之后无需再跑)。

2. **生成缩略图**(封面有了但 `covers/thumbs/` 还没有时):
   ```bash
   python3 .agents/skills/sync-wechat-index/scripts/sync_index.py thumbs
   ```
   用 macOS `sips` 把 `covers/*.png` 缩到最长边 600,输出到 `covers/thumbs/`。

3. **同步索引**(核心,每次发新文后跑):
   ```bash
   python3 .agents/skills/sync-wechat-index/scripts/sync_index.py sync
   ```
   自动重建:
   - `index.html` 的 `cats` 分类映射(第 23 行)与「按主题看」合集(第一个 `<ul class="topics">`)。
   - `README.md` 的「文章(公众号)」表格、「主题合集」、「原文(仓库 .md 草稿)」链接列表。
   - 文章卡片本身由 Jekyll 遍历 `articles/2026` 自动生成,无需手改。

4. **检查缺失项**:
   ```bash
   python3 .agents/skills/sync-wechat-index/scripts/sync_index.py check
   ```
   列出哪些文章缺封面 / 缩略图 / `mp_url`。`mp_url` 为空时合集与表格会暂用 GitHub 原稿链接,公众号发出后回填 `mp_url` 再跑一次 `sync` 即可。

5. **提交公众号 → 回填 `mp_url` → 再跑一次 `sync` → `git add -A && git commit && git push`**。

## 备注 / 常见坑

- 首页卡片缩略图读取 `cover` 字段并替换 `covers/` → `covers/thumbs/`,所以 `cover` 字段必须带 `.png` 且 `covers/thumbs/` 下有同名图,否则卡片破图。
- 合集顺序、emoji 在脚本顶部的 `CATEGORIES` / `EMOJI` 常量里改,改完重跑 `sync`。
- 分类信息是唯一事实来源(文章 front matter 的 `category` 字段),不要再手改 `index.html` 的 `cats` 字符串。
- 本技能仅适用于本仓库结构,无泛用性,故放在工程内 `.agents/skills/` 而非全局。
