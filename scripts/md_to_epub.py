#!/usr/bin/env python3
"""Render a report-helper internal Markdown build file to EPUB."""

from __future__ import annotations

import argparse
import html
import mimetypes
import re
import uuid
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from md_to_pdf import prepare_for_pdf
from report_helper_config import get_config_value


CSS = """
body {
  font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Noto Sans CJK SC", sans-serif;
  line-height: 1.85;
  color: #121212;
}
h1, h2, h3, h4 {
  line-height: 1.35;
  margin-top: 1.4em;
}
h1 { font-size: 1.8em; }
h2 { font-size: 1.45em; }
h3 { font-size: 1.2em; }
blockquote {
  margin: 1em 0;
  padding-left: 1em;
  border-left: 0.2em solid #c96442;
  color: #555;
}
table {
  border-collapse: collapse;
  width: 100%;
}
th, td {
  border-bottom: 1px solid #ddd;
  padding: 0.4em;
  vertical-align: top;
}
code, pre {
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
}
.tool-signature {
  margin-top: 2em;
  padding-top: 1em;
  border-top: 1px solid #ddd;
  color: #666;
  font-size: 0.9em;
}
"""

TOOL_SIGNATURE_HTML = """
<section class="tool-signature">
  <p>本报告由 report-helper skill 工具协助生成</p>
  <p>开源地址：https://github.com/Jiaranbb/report-helper</p>
  <p>交流和建议可联系作者：嘉然 Jiaran（+v: evadebot）</p>
</section>
"""


def extract_title(md_text: str, fallback: str) -> str:
    for line in md_text.splitlines():
        match = re.match(r"^#\s+(.+?)\s*$", line)
        if match:
            return match.group(1).strip()
    return fallback


def simple_markdown_to_html(md_text: str) -> str:
    """Small fallback for helpfully shaped EPUBs when python-markdown is unavailable."""
    blocks: list[str] = []
    list_items: list[str] = []

    def inline_html(text: str) -> str:
        escaped = html.escape(text)
        escaped = re.sub(
            r"&lt;sup&gt;([a-d]\d+)&lt;/sup&gt;",
            r"<sup>\1</sup>",
            escaped,
            flags=re.IGNORECASE,
        )
        escaped = re.sub(r"&lt;br\s*/?&gt;", "<br />", escaped, flags=re.IGNORECASE)
        return escaped

    def flush_list() -> None:
        nonlocal list_items
        if list_items:
            blocks.append("<ul>" + "".join(list_items) + "</ul>")
            list_items = []

    for raw_line in md_text.splitlines():
        line = raw_line.rstrip()
        if not line:
            flush_list()
            continue
        heading = re.match(r"^(#{1,4})\s+(.+)$", line)
        if heading:
            flush_list()
            level = len(heading.group(1))
            blocks.append(f"<h{level}>{inline_html(heading.group(2))}</h{level}>")
            continue
        if line.startswith("- "):
            list_items.append(f"<li>{inline_html(line[2:])}</li>")
            continue
        if line.startswith(">"):
            flush_list()
            blocks.append(f"<blockquote>{inline_html(line.lstrip('> ').strip())}</blockquote>")
            continue
        flush_list()
        blocks.append(f"<p>{inline_html(line)}</p>")

    flush_list()
    return "\n".join(blocks)


def markdown_to_html(md_text: str) -> str:
    try:
        import markdown
    except ModuleNotFoundError:
        return simple_markdown_to_html(md_text)
    return markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "nl2br"],
        output_format="xhtml",
    )


def xhtml_document(title: str, body: str) -> str:
    return f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-CN" lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <title>{html.escape(title)}</title>
  <link rel="stylesheet" type="text/css" href="style.css" />
</head>
<body>
{body}
</body>
</html>
"""


def nav_document(title: str) -> str:
    escaped_title = html.escape(title)
    return f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="zh-CN" lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <title>{escaped_title}</title>
</head>
<body>
  <nav epub:type="toc" id="toc">
    <h1>{escaped_title}</h1>
    <ol>
      <li><a href="content.xhtml">{escaped_title}</a></li>
    </ol>
  </nav>
</body>
</html>
"""


def opf_document(title: str, author: str, identifier: str) -> str:
    escaped_title = html.escape(title)
    escaped_author = html.escape(author)
    modified = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    creator = f"    <dc:creator>{escaped_author}</dc:creator>\n" if escaped_author else ""
    return f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="book-id">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="book-id">urn:uuid:{identifier}</dc:identifier>
    <dc:title>{escaped_title}</dc:title>
    <dc:language>zh-CN</dc:language>
{creator.rstrip()}
    <meta property="dcterms:modified">{modified}</meta>
  </metadata>
  <manifest>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav" />
    <item id="content" href="content.xhtml" media-type="application/xhtml+xml" />
    <item id="style" href="style.css" media-type="text/css" />
  </manifest>
  <spine>
    <itemref idref="content" />
  </spine>
</package>
"""


def write_epub(input_path: Path, output_path: Path, title: str, author: str) -> None:
    md_text = input_path.read_text(encoding="utf-8")
    body_md = prepare_for_pdf(md_text)
    book_title = title or extract_title(body_md, "Research Report")
    body_html = markdown_to_html(body_md) + TOOL_SIGNATURE_HTML
    identifier = str(uuid.uuid4())

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_path, "w") as epub:
        epub.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        epub.writestr(
            "META-INF/container.xml",
            """<?xml version="1.0" encoding="utf-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml" />
  </rootfiles>
</container>
""",
        )
        epub.writestr("OEBPS/content.opf", opf_document(book_title, author, identifier))
        epub.writestr("OEBPS/nav.xhtml", nav_document(book_title))
        epub.writestr("OEBPS/content.xhtml", xhtml_document(book_title, body_html))
        epub.writestr("OEBPS/style.css", CSS)

    mimetypes.add_type("application/epub+zip", ".epub")


def main() -> int:
    parser = argparse.ArgumentParser(description="Research report internal Markdown build file to EPUB")
    parser.add_argument("input", type=Path, help="内部 Markdown 构建稿路径")
    parser.add_argument("output", type=Path, help="输出的 EPUB 文件路径")
    parser.add_argument("--title", default="", help="书名；默认使用 Markdown H1")
    parser.add_argument("--author", default=get_config_value("author", ""), help="报告署名")
    args = parser.parse_args()

    write_epub(args.input, args.output, args.title, args.author)
    size_kb = args.output.stat().st_size / 1024
    print(f"[OK] EPUB 已生成: {args.output} ({size_kb:.1f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
