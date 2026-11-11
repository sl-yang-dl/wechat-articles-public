# SEO 提交指南（让搜索引擎收录本站）

本仓库已生成 `sitemap.xml` 与 `robots.txt`。下面三步把站点提交给搜索引擎，**提交 ≠ 立刻收录，但不提交新站基本没人爬**。

> 站点地址：`https://sl-yang-dl.github.io/wechat-articles-public/`
> Sitemap：`https://sl-yang-dl.github.io/wechat-articles-public/sitemap.xml`

---

## 1. 百度搜索资源平台（家长搜育儿主力，务必提交）

1. 打开 <https://ziyuan.baidu.com/> → 注册/登录百度账号。
2. 站点管理 → 添加网站 → 填上面「站点地址」→ 选「主域」或「目录」均可（这里是子目录，选目录）。
3. **验证站点**：选「HTML 标签验证」，把百度给的 `<meta>` 代码发给我，我加进 `_layouts/default.html` 的 `<head>` 里，push 后即可通过；或用「CNAME 验证」（需独立域名，暂无则跳过）。
4. 验证通过后 → 左侧「普通收录」→「sitemap」→ 提交上面 Sitemap 地址。
5. 可选：「资源提交 → 自动推送」把那段 JS 也发我，我嵌进 `default.html`，以后发新文自动通知百度。

> 百度对 GitHub Pages 的 `github.io` 域名信任度一般，若后续绑定独立域名（如 `zuoyebuhuang.com`），收录会明显更好。

---

## 2. Google Search Console（国际/香港用户、索引质量高）

1. 打开 <https://search.google.com/search-console/> → 登录 Google 账号。
2. 添加资源 → 选「网址前缀」→ 填「站点地址」。
3. **验证**：选「HTML 标记」复制 `<meta>` 发我，我加进 `<head>`；或选「Google Analytics」（若已用）。
4. 左侧「站点地图」→ 粘贴 `sitemap.xml` 的完整地址 → 提交。
5. 提交后看「网址检查」输入站点地址，可手动「请求编入索引」加速首轮抓取。

---

## 3. Bing Webmaster（含国内必应，可顺手做）

1. 打开 <https://www.bing.com/webmasters/> → 登录微软账号。
2. 添加站点 → 填「站点地址」→ 验证（同样用 `<meta>` 方式，发我加进 `<head>`）。
3. 左侧「Sitemaps」→ 提交 Sitemap 地址。
4. （可选）IndexNow：发新文时推送，需独立域名支持，暂可跳过。

---

## 验证是否生效

提交后通常 1–14 天开始有数据。验证方法：

- 百度：`site:sl-yang-dl.github.io/wechat-articles-public` 看是否出现。
- Google：Search Console →「效果」报告看曝光/点击。
- 判断标准（之前定的）：先搜「作业不慌记 错题」能出来，再慢慢搜「初三数学 取值范围 家长陪伴」能出来，就算跑通。前期吃长尾词「具体场景 + 家长情绪 + 解法」，别追大词。

---

## 需要我配合时

验证用的 `<meta>` 代码或自动推送 JS，贴给我，我加进 `_layouts/default.html` 的 `<head>` 并 push。
