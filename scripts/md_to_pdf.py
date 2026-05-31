#!/usr/bin/env python3
"""
Research report internal Markdown build file → PDF renderer (WeasyPrint version)
用法: python md_to_pdf.py input.md output.pdf [--title "报告标题"] [--author "作者"]

依赖: pip install weasyprint markdown --break-system-packages
说明: markdown 用于内部 Markdown → HTML 转换；HTML 不作为公开交付物。
"""

import sys
import os
import re
import argparse
import tempfile
import html
from pathlib import Path

from report_helper_config import get_config_value

# CSS values follow the report-class PDF layout spec.
CSS_TEMPLATE = """
@page {
    size: A4;
    margin: 28mm 25mm 25mm 25mm;
    background: #F8F8F6;

    @top-center {
        content: "HEADER_TEXT";
        font-family: system-ui, -apple-system, "Helvetica Neue", "PingFang SC", "Hiragino Sans GB", "Noto Sans CJK SC", "Microsoft YaHei", "Droid Sans Fallback", sans-serif;
        font-size: 8pt;
        color: #7B7975;
        border-bottom: 0.5pt solid #E5E3DE;
        padding-bottom: 3mm;
    }

    @bottom-center {
        content: "第 " counter(page) " 页";
        font-family: system-ui, -apple-system, "Helvetica Neue", "PingFang SC", "Hiragino Sans GB", "Noto Sans CJK SC", "Microsoft YaHei", "Droid Sans Fallback", sans-serif;
        font-size: 8pt;
        color: #7B7975;
        border-top: 0.8pt solid #C96442;
        padding-top: 2mm;
    }
}

@page :first {
    @top-center { content: none; }
    @bottom-center { content: none; }
}

html {
    background: #F8F8F6;
}

body {
    font-family: system-ui, -apple-system, "Helvetica Neue", "PingFang SC", "Hiragino Sans GB", "Noto Sans CJK SC", "Microsoft YaHei", "Droid Sans Fallback", sans-serif;
    font-size: 11.5pt;
    line-height: 2.0;
    color: #121212;
    text-align: justify;
    background: #F8F8F6;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
}

/* 封面 */
.cover {
    page-break-after: always;
    text-align: center;
    padding-top: 45%;
}
.cover h1 {
    font-size: 30pt;
    color: #C96442;
    margin-bottom: 10mm;
    font-weight: bold;
    letter-spacing: 2pt;
}
.cover .subtitle {
    font-size: 15pt;
    color: #7B7975;
    margin-bottom: 8mm;
}
.cover .meta {
    font-size: 12pt;
    color: #7B7975;
    margin-bottom: 6mm;
}
.cover .divider {
    width: 60%;
    margin: 10mm auto;
    border: none;
    border-top: 1.5pt solid #C96442;
}

/* 一级标题 */
h1 {
    font-size: 22pt;
    color: #C96442;
    margin: 18mm 0 9mm;
    padding-bottom: 4mm;
    border-bottom: 2pt solid #C96442;
    page-break-before: always;
    font-weight: bold;
    line-height: 1.4;
}

/* 二级标题 */
h2 {
    font-size: 16pt;
    color: #C96442;
    margin: 13mm 0 7mm;
    font-weight: bold;
    line-height: 1.4;
    border-left: 4pt solid #C96442;
    padding-left: 4mm;
}

/* 三级标题 */
h3 {
    font-size: 13.5pt;
    color: #C96442;
    margin: 9mm 0 5mm;
    font-weight: bold;
    line-height: 1.4;
    border-left: 2pt solid #C96442;
    padding-left: 3mm;
}

/* 四级标题 */
h4 {
    font-size: 12pt;
    color: #C96442;
    margin: 7mm 0 4mm;
    font-weight: bold;
    line-height: 1.4;
}

/* 段落 */
p {
    margin: 3mm 0;
    orphans: 3;
    widows: 3;
    color: #121212;
}

/* 引用块 */
blockquote {
    margin: 6mm 0;
    padding: 6mm;
    background: #F0EEE6;
    color: #121212;
    font-size: 11pt;
    line-height: 1.9;
}
blockquote p {
    margin: 2mm 0;
    color: #121212;
}

/* 粗体 */
strong, b {
    font-weight: bold;
    color: #121212;
}

/* 行内代码与代码块 */
code {
    font-family: "SF Mono", "JetBrains Mono", Menlo, Monaco, Consolas, "Droid Sans Fallback", "Courier New", monospace;
    background: #EBE9E2;
    color: #121212;
    padding: 0.8mm 2mm;
    border-radius: 2pt;
    font-size: 10.5pt;
}
pre {
    font-family: "SF Mono", "JetBrains Mono", Menlo, Monaco, Consolas, "Droid Sans Fallback", "Courier New", monospace;
    background: #EBE9E2;
    color: #121212;
    padding: 5mm 6mm;
    border-radius: 3pt;
    font-size: 10.5pt;
    line-height: 1.75;
    margin: 5mm 0;
    overflow-x: auto;
}
pre code {
    background: transparent;
    padding: 0;
    border-radius: 0;
}

/* 表格：无外框、横线分隔、粗体表头 */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 6mm 0;
    font-size: 10.5pt;
    background: transparent;
}
thead th {
    background: transparent;
    color: #121212;
    padding: 4mm 5mm;
    text-align: left;
    font-weight: bold;
    border-bottom: 1pt solid #7B7975;
}
tbody td {
    padding: 4mm 5mm;
    border-bottom: 0.5pt solid #E5E3DE;
    color: #121212;
    line-height: 1.8;
}
tbody tr:last-child td {
    border-bottom: none;
}
tbody tr:nth-child(even) {
    background: transparent;
}

/* 分隔线 */
hr {
    border: none;
    border-top: 0.5pt solid #E5E3DE;
    margin: 7mm 0;
}

/* 列表 */
ul, ol {
    margin: 3mm 0;
    padding-left: 9mm;
    color: #121212;
}
li {
    margin-bottom: 2.5mm;
    color: #121212;
    line-height: 1.9;
}

/* 链接 */
a {
    color: #C96442;
    text-decoration: none;
}

.tool-signature {
    margin-top: 14mm;
    padding-top: 5mm;
    border-top: 0.8pt solid #E5E3DE;
    color: #7B7975;
    font-size: 9.5pt;
    line-height: 1.7;
}
.tool-signature p {
    margin: 1.5mm 0;
    color: #7B7975;
}
"""

TOOL_SIGNATURE_HTML = """
<section class="tool-signature">
  <p>本报告由 report-helper skill 工具协助生成</p>
  <p>开源地址：https://github.com/Jiaranbb/report-helper</p>
  <p>交流和建议可联系作者：嘉然 Jiaran（+v: evadebot）</p>
</section>
"""


def escape_css_content(value):
    """Escape dynamic text inserted into a CSS content string."""
    return str(value).replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")


def prepare_for_pdf(md_text):
    """PDF 专用的 Markdown 预处理，删掉笔记系统独占的结构性元素。

    做三件事：
    1. 剥掉 H1 下方「研究时间 / 相关索引」那个预置 blockquote。
    2. 把「## 一句话定义」或「## 一句话结论」章节转成 blockquote（去掉标题）。
    3. 只砍掉章节标题里的内部工作前缀。
    """
    # Step 1: 剥掉开头的笔记元信息 blockquote
    lines = md_text.split('\n')
    out = []
    i = 0
    preamble_stripped = False
    while i < len(lines):
        line = lines[i]
        if not preamble_stripped and line.lstrip().startswith('>'):
            j = i
            block_lines = []
            while j < len(lines) and (lines[j].lstrip().startswith('>') or lines[j].strip() == ''):
                block_lines.append(lines[j])
                j += 1
                if j < len(lines) and not lines[j].lstrip().startswith('>') and lines[j].strip() != '':
                    break
            block_text = '\n'.join(block_lines)
            if '研究时间' in block_text or '相关索引' in block_text:
                i = j
                while i < len(lines) and lines[i].strip() == '':
                    i += 1
                preamble_stripped = True
                continue
        out.append(line)
        i += 1
    md_text = '\n'.join(out)

    # Step 2: 把「## 一句话定义 / 一句话结论」章节转成 blockquote
    pattern = re.compile(
        r'^##\s+(?:一句话定义|一句话结论)\s*\n+(.+?)(?=\n##\s|\n---\s*$|\Z)',
        flags=re.MULTILINE | re.DOTALL
    )

    def to_blockquote(m):
        body = m.group(1).rstrip()
        quoted = []
        for ln in body.split('\n'):
            quoted.append('> ' + ln if ln.strip() else '>')
        return '\n'.join(quoted) + '\n'

    md_text = pattern.sub(to_blockquote, md_text)

    # Step 3: 砍掉历史版本可能写入的内部方法标题前缀，但保留正式报告的「一、报告摘要」这类编号
    md_text = re.sub(
        r'^(##\s+)[一二三四五六七八九十\d]+、\s*(?:时间线检查|同期格局检查|判断合成|竞品场景判断)\s*[:：]?\s*',
        r'\1',
        md_text,
        flags=re.MULTILINE
    )

    return md_text


def md_to_html(md_text, title="Research Report", subtitle="",
               meta_line="", author=""):
    """将 Markdown 转为带封面的 HTML"""

    md_text = prepare_for_pdf(md_text)

    # 用 markdown 库转换正文
    import markdown

    html_body = markdown.markdown(
        md_text,
        extensions=['tables', 'fenced_code', 'nl2br'],
        output_format='html5'
    )

    # 移除正文中的第一个 h1（会用在封面上）
    first_h1_match = re.search(r'<h1>(.*?)</h1>', html_body)
    if first_h1_match:
        extracted_title = first_h1_match.group(1)
        if not title or title in ("Research Report", "深度研究报告"):
            title = extracted_title
        html_body = html_body.replace(first_h1_match.group(0), '', 1)

    # 替换 CSS 中的页眉占位符
    header_text = f"{title}  |  {subtitle}" if subtitle else title
    css = CSS_TEMPLATE.replace("HEADER_TEXT", escape_css_content(header_text))

    # 构建封面
    safe_title = html.escape(title)
    safe_subtitle = html.escape(subtitle)
    safe_meta_line = html.escape(meta_line)
    safe_author = html.escape(author)
    subtitle_html = f"<div class='subtitle'>{safe_subtitle}</div>" if subtitle else ""
    author_html = f"<div class='meta'>作者: {safe_author}</div>" if author else ""
    cover_html = f"""
    <div class="cover">
        <h1 style="page-break-before: avoid; border: none;">{safe_title}</h1>
        {subtitle_html}
        {"<div class='meta'>" + safe_meta_line + "</div>" if meta_line else ""}
        <hr class="divider">
        {author_html}
    </div>
    """

    full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <style>{css}</style>
</head>
<body>
{cover_html}
{html_body}
{TOOL_SIGNATURE_HTML}
</body>
</html>"""

    return full_html


def main():
    parser = argparse.ArgumentParser(description="Research report internal Markdown build file to PDF")
    parser.add_argument("input", help="输入的内部 Markdown 构建稿路径")
    parser.add_argument("output", help="输出的 PDF 文件路径")
    parser.add_argument("--title", default=None, help="报告标题")
    parser.add_argument("--subtitle", default="", help="副标题（默认空，不显示）")
    parser.add_argument("--author", default=get_config_value("author", ""), help="报告署名")
    parser.add_argument("--html-output", default="", help="临时 HTML 输出路径；默认写入系统临时目录")
    parser.add_argument("--keep-html", action="store_true", help="保留临时 HTML 文件")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        md_text = f.read()

    # 提取元信息
    meta_line = ""
    for line in md_text.split("\n"):
        stripped = line.strip().lstrip(">").strip()
        if "研究时间" in stripped or "所属领域" in stripped or "研究对象类型" in stripped:
            meta_line = stripped
            break

    html = md_to_html(md_text, title=args.title or "Research Report", subtitle=args.subtitle, meta_line=meta_line, author=args.author)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if args.html_output:
        html_path = Path(args.html_output)
    else:
        fd, tmp_path = tempfile.mkstemp(prefix=f"{output_path.stem}-", suffix=".html")
        os.close(fd)
        html_path = Path(tmp_path)
    html_path.parent.mkdir(parents=True, exist_ok=True)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"[OK] HTML 已生成: {html_path}")

    # 转 PDF
    from weasyprint import HTML
    HTML(string=html).write_pdf(str(output_path))
    if not args.keep_html:
        html_path.unlink(missing_ok=True)
    size_kb = os.path.getsize(output_path) / 1024
    print(f"[OK] PDF 已生成: {output_path} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
