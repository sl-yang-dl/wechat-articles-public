# 微信贴图｜给孩子报的班，是买给我自己的

> 5 张图（1080×1080），`img/tz-01..05.png`。
> 与公众号同一天发；贴图不导流回文章，只导关注。

---

**标题**（贴图也带标题，别留空）

```
给孩子报的班，是买给我自己的
```

**正文**（约 130 字，直接贴）

```
晚上八点，电脑上又在喊"扣666"，孩子咔咔敲键盘。

我们家现在网课和辅导班都还在上。

怎么判断一个班是孩子在上，还是你买的心安？
看三点：
不用你问，他会不会主动提一句课上的事；
做作业时，突然说这题老师课上讲过；
你少盯一半，他能不能照常上课、交作业。

三条一条都不中，这课买的就是心安。

这笔账，我认了。
```

---

## 图片顺序

| 序 | 版式 | 作用 | 内容 | 图 |
|---|---|---|---|---|
| 1 | `--note` | 钩子 | 给孩子报的班，是买给我自己的 | tz-01 |
| 2 | `--note` | 场景 | 晚上八点，电脑喊"扣666"，孩子咔咔敲键盘 | tz-02 |
| 3 | `--list` | 给东西 | 三条标准（主动提 / 做题时说起 / 少盯还能照常） | tz-03 |
| 4 | `--note` | 扎一下 | 三条一条都不中／就是买给你的 | tz-04 |
| 末 | `--follow` | 落点 | 价值主张 + 二维码 + 作业不慌记 | tz-05 |

## 改了什么（对应源稿 10-25 定稿）

- **三条标准整组换掉**：旧的「课前主动开电脑 / 课后说出一个点 / 下次还愿不愿意去」是**意愿题**，
  答得再好也验证不了。新的三条全是**可观察的行为**，而且都能在生活里撞见。
- **第 4 张从 `--quote` 换成 `--note`**：旧版居中细字、四周全空，在信息流里等于没有。
  现在和第 1 张同一套大字，读者划到第 4 张还能站住。
- **第 3 张第 3 条压到 19 字**（原句「照常上课、交作业、改错」会被截成省略号）。
  **清单卡上一出现省略号，整张就废了**——读者会以为是自己没看清，然后划走。

## 出图命令

```bash
T="dist/2026-10-26-我们家的网课和辅导班/tiezi"
python3 .agents/skills/tiezi-images/scripts/make_cards.py --note --chip "报班真相" \
  --title "给孩子报的班，\n是买给我自己的" --subtitle "不是买成绩，是买心安" \
  --palette "$T/palette.json" --footer "作业不慌记" --out "$T/img/tz-01.png"

python3 .agents/skills/tiezi-images/scripts/make_cards.py --note --chip "晚八点" \
  --title "电脑上又在喊\n扣 666" --subtitle "孩子咔咔敲键盘" \
  --palette "$T/palette.json" --footer "作业不慌记" --out "$T/img/tz-02.png"

python3 .agents/skills/tiezi-images/scripts/make_cards.py --list --title "怎么判断班是谁在上" \
  --item "不用你问，他会不会主动提一句课上的事" \
  --item "做作业时，突然说这题老师课上讲过" \
  --item "你少盯一半，他能不能照常上课、交作业" \
  --palette "$T/palette.json" --footer "作业不慌记" --out "$T/img/tz-03.png"

python3 .agents/skills/tiezi-images/scripts/make_cards.py --note --chip "扎一下" \
  --title "三条一条都不中\n就是买给你的" --subtitle "买的是心安，不是成绩" \
  --palette "$T/palette.json" --footer "作业不慌记" --out "$T/img/tz-04.png"

python3 .agents/skills/tiezi-images/scripts/make_cards.py --follow \
  --palette "$T/palette.json" --out "$T/img/tz-05.png"
```
