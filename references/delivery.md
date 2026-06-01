# 交付流程

本文件只处理内部构建稿保存、可选日志追加和 PDF 渲染。进入交付阶段后，不再改动核心分析和正文判断；发现事实或结构问题时，回到 `workflow.md` 的审核步骤处理。

## 1. 输出路径

首次使用或环境不明确时，先运行：

```bash
python3 scripts/check_environment.py
```

该脚本会检查 Python 版本、`config.local.json`、报告署名、PDF 渲染依赖，以及 Chrome fallback 是否可用。不通过时，按脚本提示补配置或安装依赖。

默认目录：

```text
./output/
./output/work/
./output/intermediate/
```

路径可以通过 `config.local.json`、`REPORT_HELPER_CONFIG` 指向的 JSON 文件，或环境变量覆盖。优先级是：

```text
脚本内置默认值 → config.local.json / REPORT_HELPER_CONFIG → REPORT_HELPER_* 环境变量
```

支持的环境变量：

- `REPORT_HELPER_OUTPUT_DIR`
- `REPORT_HELPER_WORK_DIR`
- `REPORT_HELPER_INTERMEDIATE_DIR`
- `REPORT_HELPER_LOG_PATH`
- `REPORT_HELPER_LOG_INSERT_AFTER_HEADING`
- `REPORT_HELPER_LOG_INSERT_AFTER_MARKER`
- `REPORT_HELPER_AUTHOR`
- `REPORT_HELPER_SOURCE`
- `REPORT_HELPER_CHROME`
- `REPORT_HELPER_DYLD_FALLBACK`

报告署名来自 `config.local.json` 的 `author` 或 `REPORT_HELPER_AUTHOR`。首次安装时必须让用户填写报告署名，不要默认使用工具作者名。本地绝对路径、账号标识、私有日志标题等个人配置只放在已忽略的 `config.local.json` 或环境变量里。

## 2. 保存内部 Markdown 构建稿

Markdown 是内部构建稿，只用于渲染 PDF。构建稿直接从正文 H1 开始。

默认建议路径：

```text
./output/work/{YYYY-MM-DD}-{topic-slug}-report.md
```

如果配置了 `work_dir`，保存到配置目录。

## 3. 可选日志

如果配置了项目日志，追加一条简洁记录。先确定内部构建稿标题：即 Markdown 文件名去掉 `.md` 后的标题。

如果日志需要插入到某个私有标题下面，把标题写入 `config.local.json` 的 `log_insert_after_heading`，或运行脚本时传 `--insert-after-heading`。共享脚本不能硬编码私有日志标题。

日志示例：

```markdown
## [YYYY-MM-DD] write | {topic} research report completed

{2-5 行：主题、范围、核心结论、交付物}

- [[{note_title}]]
- 中间资料：`./output/intermediate/{topic-slug}-{YYYY-MM-DD}/`
- 交付物：`./output/{研究对象}深度研究报告.pdf`
- {关键发现}
```

脚本示例：

```bash
python scripts/append_report_log.py \
  --log-path ./output/report-log.md \
  --insert-after-heading "" \
  --date YYYY-MM-DD \
  --title "{topic} research report completed" \
  --body "{2-5 line summary}" \
  --link "[[{note_title}]]" \
  --bullet "中间资料：\`./output/intermediate/{topic-slug}-{YYYY-MM-DD}/\`" \
  --bullet "交付物：\`./output/{研究对象}深度研究报告.pdf\`" \
  --bullet "{key finding}"
```

## 4. 渲染 PDF

使用 fallback 渲染脚本：

```bash
python scripts/render_pdf_with_fallback.py \
  ./output/work/{file-name}.md \
  ./output/{研究对象}深度研究报告.pdf \
  --title "{H1 title}" \
  --author "{配置的报告署名}"
```

脚本会先调用 `md_to_pdf.py`。PDF 渲染内部需要把 Markdown 构建稿转成临时 HTML；HTML 只是中间产物，不作为公开交付物。如果 WeasyPrint 失败但已经生成 HTML，则尝试使用 Chrome headless fallback。Chrome 路径可以通过 `REPORT_HELPER_CHROME`、`config.local.json` 的 `chrome_path`，或命令行 `--chrome` 指定。

PDF 最末尾必须追加固定工具签名：

```text
本报告由 report-helper skill 工具协助生成
开源地址：https://github.com/Jiaranbb/report-helper
交流和建议可联系作者：嘉然 Jiaran（+v: evadebot）
```

## 5. 交付物验证

最低检查：

- PDF 文件存在且大小不为 0
- 能读取页数
- 封面标题正确
- 封面作者为配置的报告署名
- 首页视觉上可读
- PDF 最末尾包含固定工具签名

## 6. 最终回复

交付时告诉用户：

- PDF 路径
- 中间资料目录
- 是否追加日志
- PDF 渲染路径：WeasyPrint 或 Chrome fallback
