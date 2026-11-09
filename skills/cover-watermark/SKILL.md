---
name: cover-watermark
description: >-
  给公众号封面图加品牌水印(公众号名 + 搜一搜引导),提升 Google 图片搜索可见性与品牌识别。
  当要为仓库封面批量打水印、或新增文章封面需要统一品牌时使用。
---

# 封面水印

给公众号封面 PNG 加统一的底部半透明水印条:左侧公众号名、右侧搜一搜引导语。
目的是让封面在 Google 图片搜索里也能带品牌、被顺藤摸到号。

## 何时使用

- 用户说"给封面加水印""统一品牌""封面打标"。
- 新增文章、需对 `covers/*.png` 全尺寸封面补水印。
- 需要把"水印"能力沉淀成可复用流程时。

## 步骤

1. 确认范围:**只处理全尺寸封面 `covers/*.png`,跳过 `covers/thumbs/`**(小图 140px 加了也看不清,且 README 表格里应保持干净)。
2. 运行脚本(依赖 Pillow + macOS 中文字体):
   ```bash
   # 单张
   python3 skills/cover-watermark/scripts/watermark.py covers/2026-XX-XX-xxx.png covers/2026-XX-XX-xxx.png
   # 批量(覆盖原位)
   for f in covers/*.png; do [ -f "$f" ] || continue; case "$f" in covers/thumbs/*) continue;; esac; \
     python3 skills/cover-watermark/scripts/watermark.py "$f" "$f"; done
   ```
3. **务必让用户本地打开核对效果**(见下方"注意")。
4. 确认无误后再 `git add` + 提交 + 推送。

## 水印样式(脚本默认值)

- 底部半透明黑条:高度约图高 16%、透明度 ~47%。
- 左:白字主标题(默认 `作业不慌记`)。
- 右:白字副标题(默认 `微信搜一搜 · 看更多陪学日常`)。
- 可用 `--name` / `--sub` 覆盖文案。

## 注意

- **本环境模型无法读取图片**,无法替用户确认美观度。脚本跑完后一定要让用户打开至少一张封面人工核对;不满意可 `git checkout -- covers/` 一键还原。
- 字体写死 macOS 路径 `/System/Library/Fonts/STHeiti Medium.ttc`;换系统需改 `FONT`。
- 不要对 `thumbs/` 小图加水印。
- 水印是破坏性的(直接覆盖原图),依赖 git 可回滚;若想保留原图,先 `cp` 备份。
