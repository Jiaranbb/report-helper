# report-helper｜深度研究报告生成助手

`report-helper` 是一个面向长篇研究报告写作的 AI Skill。它适合用来研究一个产品、公司、人物、概念、产业链、政策或趋势，并产出一份有资料来源、有判断、有排版的正式报告。

它的目标不是给出几段概述，而是完成一套更接近研究写作的流程：先明确研究范围，再搜集和核查资料，整理证据链，形成核心判断，最后生成 PDF 文档和 EPUB 电子书。

## 适合用来做什么

- 产品、公司、人物、概念的深度研究
- 产业链、政策、趋势、年度展望类研究报告
- 需要较长篇幅、可追溯来源和 PDF / EPUB 成品的分析文章
- 需要把资料搜集、判断形成、正文写作和交付整理放在同一流程里的研究任务

## 你会得到什么

- 一份排版后的 PDF 报告
- 一份 EPUB 电子书，可导入微信读书打开阅读
- 一组中间研究资料，方便回看来源、缺口和判断依据
- 一份信息来源列表，标注关键资料来自一手、二手还是存疑来源

## 如何使用

在支持 Skills 的 AI 工具里，说出类似下面的需求即可：

- `深度研究 DeepSeek`
- `写一份 AI 算力产业发展研究报告`
- `深入研究某个产品的发展历程和竞争格局`
- `生成一份 2026-2030 趋势研究报告`

默认情况下，`report-helper` 会先让你确认研究范围和执行模式。你可以选择交互模式，分阶段审核研究范围、资料充分性和写作准备；也可以选择 auto 模式，让它在中间自检后一路完成。

## 首次使用

第一次使用前，建议先完成三件事。

### 1. 检查环境

先运行环境检查：

```bash
python3 scripts/check_environment.py
```

它会检查 Python 版本、`config.local.json`、报告署名、交付格式、PDF 渲染依赖，以及 Chrome fallback 是否可用。不通过时，按脚本输出补配置或安装依赖。

### 2. 安装依赖

如果环境检查提示缺依赖，安装：

```bash
python3 -m pip install markdown weasyprint
```

这里的 `markdown` 不是交付 HTML 用的，而是 PDF 渲染链路里的内部转换依赖：内部 Markdown 构建稿会先转成临时 HTML，再由 WeasyPrint 或 Chrome 生成 PDF。HTML 不作为公开交付物提供。

EPUB 生成只依赖 Python 标准库，也可以安装 `markdown` 获得更完整的排版转换。PDF 生成需要 `markdown`，并使用 WeasyPrint 或 Chrome fallback 渲染。

如果 WeasyPrint 在你的系统上安装或渲染失败，可以安装 Chrome，并在配置里填写 `chrome_path`，让 PDF 使用 Chrome fallback。

### 3. 指定存放目录和报告署名

复制 `config.example.json` 为 `config.local.json`，然后按自己的需要修改目录：

```json
{
  "output_dir": "./output",
  "work_dir": "./output/work",
  "intermediate_dir": "./output/intermediate",
  "author": "你的名字或组织名"
}
```

- `output_dir`：最终 PDF / EPUB 存放目录
- `work_dir`：内部构建稿目录
- `intermediate_dir`：中间研究资料目录
- `author`：报告署名，会显示在 PDF 封面和 EPUB 元数据里；首次安装时由你填写

### 4. 指定交付格式

公开版支持三种交付方式：

```json
{
  "delivery_formats": ["pdf", "epub"]
}
```

- 只要 PDF：`["pdf"]`
- 只要 EPUB：`["epub"]`
- 两个都要：`["pdf", "epub"]`

也可以在每次发起任务时直接说明：`只要 PDF`、`只要 EPUB`、`PDF 和 EPUB 都要`。EPUB 文件可以导入微信读书打开阅读。

## 使用提醒

- 报告生成质量高度依赖模型能力。推荐使用 Codex GPT-5.5 以获得最佳效果。
- 研究型输出依赖公开资料质量。找不到或无法确认的信息，会被标注为「未搜到 / 存疑」。
- AI 生成报告可能会出错，包括从正确事实中推出错误结论。报告只能作为学习参考，不适合作为投资、法律、医疗等专业决策的唯一依据。
- 建议对重要报告做「同行评审」（Peer Review）：这里的「同行评审」指多个 AI agent 之间互相评审、挑刺、提问，交叉验证事实与推理链。
- 如果你有指定目录、重点问题、字数、读者对象或交付格式，请在一开始说明。

## 作者

**嘉然 Jiaran**

- 公众号：**嘉然学习笔记**
- 微信：`evadebot`
- GitHub：https://github.com/Jiaranbb/report-helper

---

# report-helper

`report-helper` is a portable research-report skill. It helps an agent run web research, audit source quality, write a long-form report, review it, and render PDF plus EPUB deliverables.

## What It Produces

- PDF report
- EPUB ebook that can be imported into WeChat Reading
- Optional intermediate research notes and internal build logs

## Quality And Review

Report quality depends heavily on model capability. Codex GPT-5.5 is recommended for best results.

AI-generated reports can still be wrong, including drawing incorrect conclusions from correct facts. Treat outputs as learning references, and use PR-style "peer review" between multiple AI agents to challenge assumptions, ask hard questions, and verify reasoning.

## Typical Trigger

Use this skill when the user asks for:

- `deep research on X`
- `深度研究 X`
- `industry research report`
- `development research report`
- a long-form report about a product, company, person, policy, trend, concept, or value chain

## Configuration

Copy `config.example.json` to `config.local.json` for your own defaults. Do not commit `config.local.json`.

Resolution order:

1. built-in script defaults
2. `config.local.json`, or the JSON file pointed to by `REPORT_HELPER_CONFIG`
3. `REPORT_HELPER_*` environment variables

The scripts also support environment variables:

- `REPORT_HELPER_OUTPUT_DIR`
- `REPORT_HELPER_WORK_DIR`
- `REPORT_HELPER_INTERMEDIATE_DIR`
- `REPORT_HELPER_DELIVERY_FORMATS`
- `REPORT_HELPER_AUTHOR`
- `REPORT_HELPER_LOG_PATH`
- `REPORT_HELPER_LOG_INSERT_AFTER_HEADING`
- `REPORT_HELPER_LOG_INSERT_AFTER_MARKER`
- `REPORT_HELPER_SOURCE`
- `REPORT_HELPER_CHROME`
- `REPORT_HELPER_DYLD_FALLBACK`

## Dependencies

Run the environment check first:

```bash
python3 scripts/check_environment.py
```

Install Python dependencies for PDF rendering and richer EPUB conversion:

```bash
python3 -m pip install markdown weasyprint
```

The `markdown` package is used as an internal Markdown-to-HTML conversion step for PDF rendering; HTML is not a public deliverable. If WeasyPrint is unavailable, install Chrome and set `chrome_path` in `config.local.json` or `REPORT_HELPER_CHROME` for PDF fallback rendering.

Choose deliverables with `delivery_formats` in `config.local.json`:

```json
{
  "author": "Your Name or Organization",
  "delivery_formats": ["pdf", "epub"]
}
```

`author` is the report byline shown in the PDF cover and EPUB metadata. Use `["pdf"]`, `["epub"]`, or `["pdf", "epub"]` for deliverables. EPUB files can be imported into WeChat Reading. Final PDF/EPUB files append a fixed report-helper signature with the open-source URL and maintainer contact.

## Scripts

```bash
python scripts/check_environment.py
python scripts/render_pdf_with_fallback.py output/work/example.md output/Example深度研究报告.pdf --title "Example Report"
python scripts/md_to_epub.py output/work/example.md output/Example深度研究报告.epub --title "Example Report"
python scripts/append_report_log.py --date 2026-01-01 --title "Example report completed" --body "Short summary"
```

## Public Sharing Notes

Before publishing your fork, scan shared files for absolute local paths, account names, personal workflow notes, private log headings, and account-specific URLs. Keep local override files such as `.env`, `config.local.json`, and generated output out of Git.

## 关于作者

**嘉然 Jiaran**

- 公众号：**嘉然学习笔记**
- 微信：`evadebot`
- GitHub：https://github.com/Jiaranbb/report-helper
