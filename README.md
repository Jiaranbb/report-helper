# report-helper · 一句话生成深度研究报告

![AI Skill](https://img.shields.io/badge/AI-Skill-111111?style=flat-square)
![Deep Research](https://img.shields.io/badge/Deep-Research-2563EB?style=flat-square)
![PDF Report](https://img.shields.io/badge/PDF-Report-D97706?style=flat-square)
![Codex](https://img.shields.io/badge/Codex-Supported-222222?style=flat-square)
![Claude Code](https://img.shields.io/badge/Claude%20Code-Supported-6B5B95?style=flat-square)
![WeChat](https://img.shields.io/badge/WeChat-evadebot-07C160?style=flat-square&logo=wechat&logoColor=white)
![公众号](https://img.shields.io/badge/%E5%85%AC%E4%BC%97%E5%8F%B7-%E5%98%89%E7%84%B6%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0-07C160?style=flat-square&logo=wechat&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-Jiaranbb-181717?style=flat-square&logo=github&logoColor=white)

[English README](./README.en.md) · [30 秒开始](#30-秒开始) · [示例报告](./examples/中国算力产业链深度分析报告.pdf) · [问题反馈](https://github.com/Jiaranbb/report-helper/issues) · [联系作者](./SUPPORT.md)

**作者 / 联系方式**：嘉然 Jiaran · 公众号：**嘉然学习笔记** · 微信：`evadebot`

`report-helper` 是一个面向深度研究报告写作的 AI Skill。给出研究对象后，它会引导 agent 自动完成资料搜集、来源核查、证据整理、判断形成、审稿和 PDF 生成。

> 从一句话到一份可分享的正式 PDF：有来源、有判断、有排版。

它适合研究产品、公司、人物、概念、产业链、政策或趋势。目标不是生成几段概述，而是尽量跑完一套接近研究写作的流程，产出一份可核查、可阅读、可交付的长篇报告。

## 30 秒开始

把下面这段话直接发给 Codex、Claude Code、OpenClaw 或其他支持 Skill 的 agent：

```text
请从 GitHub 安装 report-helper skill：https://github.com/Jiaranbb/report-helper。安装完成后提醒我按当前工具要求重启或刷新 agent；重启后帮我运行 python3 scripts/check_environment.py 检查环境。
```

如果你的环境支持 `skills` CLI，也可以尝试：

```bash
npx skills add https://github.com/Jiaranbb/report-helper --skill report-helper
```

Codex 用户也可以手动安装：

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo Jiaranbb/report-helper \
  --path . \
  --name report-helper
```

安装完成后，按当前工具要求重启或刷新 agent，让新 skill 生效。

## 核心能力

- 🧭 **一句话启动**：给出研究对象和重点后，自动跑完整报告流程。
- 🔎 **资料搜集详实**：要求先查找最新数据，再进入写作，避免凭旧信息直接开写。
- 🧾 **来源可追溯**：正文关键事实使用 `<sup>a1</sup>` 这类编号，文末按来源等级列出出处。
- 📊 **兼顾定性与定量**：公司研究必须加入成长性、盈利质量、现金流、融资或估值等定量分析。
- 🎨 **PDF 排版设计过**：背景色、字号、行距、标题层级和页脚样式都做过适配，适合直接分享。

## 效果预览

示例由 Codex GPT-5.5 标准速度生成，耗时约 15 分钟。报告质量和所需时间依赖于模型能力、资料可得性、联网检索质量和研究对象复杂度。

运行示例：

![report-helper 运行示例](examples/report-helper-demo.png)

PDF 预览：

![report-helper PDF 预览](examples/report-helper-pdf-preview.png)

示例报告：[`中国算力产业链深度分析报告.pdf`](examples/中国算力产业链深度分析报告.pdf)

## 直接这样用

安装后，对 agent 说：

```text
深度研究中国算力产业链，重点看 2026-2030 年的发展趋势，自动进行。
```

也可以这样描述：

```text
深度研究某家公司，重点看商业模式、增长空间、估值逻辑和风险。

写一份 AI 算力产业发展研究报告。

深入研究某个产品的发展历程、竞争格局和未来演进。
```

默认情况下，`report-helper` 会先让你确认研究范围和执行模式。你可以选择交互模式，分阶段审核研究范围、资料充分性和写作准备；也可以选择 auto 模式，让它在中间自检后一路完成。

## 适合 / 不适合

**✅ 适合**

- 产品、公司、人物、概念、产业链、政策、趋势的深度研究
- 需要公开资料、证据链和来源分级的长篇报告
- 需要正式 PDF 交付物的研究写作任务
- 需要多个 agent 做「同行评审」（Peer Review）的重要议题
- 需要把叙事判断和定量指标放在一起看的公司/行业研究

**❌ 不适合**

- 简单名词解释、几段概述、普通问答
- 不需要联网检索和来源核查的轻量写作
- 投资、法律、医疗等需要专业资质背书的最终决策
- 私有数据未提供、且公开资料无法支撑的精确结论
- 只想要可编辑 Markdown 文稿的交付方式

## 常见使用场景

| 任务 | 推荐说法 |
|------|---------|
| 产业链研究 | `深度研究中国算力产业链，重点看 2026-2030 年发展趋势，自动进行。` |
| 公司研究 | `深度研究某公司，重点看商业模式、增长空间、盈利质量、估值逻辑和风险。` |
| 产品研究 | `深入研究某产品的发展历程、核心能力、用户场景和竞争格局。` |
| 政策研究 | `写一份某政策的深度研究报告，重点看影响路径、受益主体和潜在风险。` |
| 趋势研究 | `生成一份 2026-2030 趋势研究报告，要求有来源、有判断、有观察指标。` |
| 人物研究 | `深度研究某人物，重点看关键经历、决策风格、影响力和争议。` |

## 平台支持

| 平台 | 状态 | 说明 |
|------|------|------|
| Codex | 支持 | 推荐环境；支持安装、检查环境、运行脚本和生成 PDF |
| Claude Code | 支持 | 适合长流程研究、资料搜集和写作迭代 |
| OpenClaw | 可用 | 需要能读取 skill 文件并执行必要 shell 命令 |
| Cursor / 其他本地 agent | 可用 | 需要能读写文件、联网检索并执行 Python 或浏览器渲染 |
| 普通 Chatbot | 不推荐 | 没有文件系统和渲染管线时，难以稳定生成 PDF |

## 首次使用

第一次使用前，建议先完成三件事。

### 1. 检查环境

```bash
python3 scripts/check_environment.py
```

它会检查 Python 版本、`config.local.json`、报告署名、PDF 渲染依赖，以及 Chrome fallback 是否可用。不通过时，按脚本输出补配置或安装依赖。

### 2. 安装 PDF 渲染依赖

如果环境检查提示缺依赖，安装：

```bash
python3 -m pip install markdown weasyprint
```

如果 WeasyPrint 在你的系统上安装或渲染失败，可以安装 Chrome，并在配置里填写 `chrome_path`，使用 Chrome 生成 PDF。

### 3. 指定存放目录和报告署名

复制 `config.example.json` 为 `config.local.json`，然后按自己的需要修改：

```json
{
  "output_dir": "./output",
  "work_dir": "./output/work",
  "intermediate_dir": "./output/intermediate",
  "author": "你的名字或组织名"
}
```

- `output_dir`：最终 PDF 存放目录
- `work_dir`：内部构建稿目录
- `intermediate_dir`：中间研究资料目录
- `author`：报告署名，会显示在 PDF 封面；首次安装时由你填写

## 输出内容

- **PDF 报告**：最终交付物，文件名建议为 `{研究对象}深度研究报告.pdf`
- **中间资料**：资料搜集、来源整理和研究过程记录
- **内部构建稿**：仅作为 PDF 渲染输入，不作为公开交付物
- **可选 log**：如果配置了 log 目录，可在完成后追加记录

PDF 最末尾会追加工具签名：

```text
本报告由 report-helper skill 工具协助生成
开源地址：https://github.com/Jiaranbb/report-helper
交流和建议可联系作者：嘉然 Jiaran（+v: evadebot）
```

## 工作流

`report-helper` 会按 7 步执行：

1. **范围对齐**：确认研究对象、类型、动机、关注点和执行模式。
2. **资料搜集**：优先查找最新官方、监管、财报、原始研究或权威报道。
3. **充分性审计**：检查资料缺口，严重不足时必须补搜。
4. **形成判断**：整理核心判断、证据链和反方观点。
5. **写作成稿**：按报告类型选择结构，公司研究加入定量分析。
6. **审核回炉**：按清单检查事实、来源、结构、口吻、PDF 交付。
7. **生成交付**：输出 PDF，并保留中间资料和必要日志。

## 信息来源规则

正文关键事实判断必须使用上标标注来源等级和编号，例如：

- `<sup>a1</sup>`：A 级，官方/学术一手来源
- `<sup>b4</sup>`：B 级，权威媒体原创报道

文末按等级列出「信息来源与分级」：

- `a`：官方/学术一手，政府机构、监管机构、公司年报和原始研究报告
- `b`：权威媒体原创报道
- `c`：行业媒体/工具商博客
- `d`：软文/服务商自述/不可验证

默认不使用 `c`、`d` 级来源支撑正文判断。

## 目录结构

```text
report-helper/
├── SKILL.md                          ← Skill 入口和核心流程
├── README.md                         ← 中文项目介绍
├── README.en.md                      ← English README
├── SUPPORT.md                        ← 联系方式和支持入口
├── CHANGELOG.md                      ← 更新记录
├── LICENSE                           ← MIT License
├── config.example.json               ← 本地配置模板
├── examples/
│   ├── report-helper-demo.png
│   ├── report-helper-pdf-preview.png
│   └── 中国算力产业链深度分析报告.pdf
├── references/
│   ├── workflow.md                   ← 研究和审计流程
│   ├── report-template.md            ← 报告结构模板
│   ├── source-citation-rules.md      ← 来源分级和编号规则
│   ├── writing-style.md              ← 写作风格
│   ├── adaptations-by-type.md        ← 不同对象类型的适配
│   ├── review-checklist.md           ← 审核清单
│   ├── delivery.md                   ← PDF 生成和交付
│   ├── subagent-research-prompt.md   ← 研究 worker 提示
│   └── gotchas.md                    ← 踩坑记录
└── scripts/
    ├── report_helper_config.py
    ├── check_environment.py
    ├── render_pdf_with_fallback.py
    ├── md_to_pdf.py
    └── append_report_log.py
```

## 质量提醒

- 报告生成质量高度依赖模型能力。推荐使用 Codex GPT-5.5 以获得最佳效果。
- 研究型输出依赖公开资料质量。找不到或无法确认的信息，会被标注为「未搜到 / 存疑」。
- AI 生成报告可能会出错，包括从正确事实中推出错误结论。
- 报告只能作为学习参考，不适合作为投资、法律、医疗等专业决策的唯一依据。
- 建议对重要报告做「同行评审」（Peer Review）：这里的「同行评审」指多个 AI agent 之间互相评审、挑刺、提问，交叉验证事实与推理链。

## FAQ

**为什么一定要先确认研究范围？**

深度报告最容易失败在「题目过宽」或「对象不清」。先对齐范围，可以减少后面资料搜集和写作方向的偏差。

**为什么要强调最新数据？**

产业、公司、政策和技术趋势变化很快。进入写作前必须完成最新数据校验，避免 agent 用旧资料直接写出过时结论。

**可以只要 Markdown 吗？**

公开版默认交付 PDF。内部 Markdown 构建稿主要用于渲染，不作为正式交付物。

**公司研究为什么要加定量分析？**

只写叙事容易变成故事。公司研究默认要求加入成长性、盈利质量、现金流、融资、估值或可比公司等内容；公开数据不足时，要写明缺口和替代观察指标。

**PDF 乱码怎么办？**

先运行 `python3 scripts/check_environment.py` 检查依赖。WeasyPrint 不稳定时，可以配置 Chrome fallback。

**如何更新到最新版本？**

重新安装，或在本地 skill 目录执行 `git pull`。

## 作者与反馈

**嘉然 Jiaran**

- 公众号：**嘉然学习笔记**
- 微信：`evadebot`
- GitHub：https://github.com/Jiaranbb/report-helper
- 支持与反馈：[SUPPORT.md](./SUPPORT.md)
- 问题与建议：[GitHub Issues](https://github.com/Jiaranbb/report-helper/issues)

## License

MIT License. See [LICENSE](LICENSE).
