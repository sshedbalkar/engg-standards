"""Markdown to Confluence storage HTML rendering."""

from __future__ import annotations

import html
import os
import re
from typing import Any
from urllib.parse import unquote

from .models import ConfluenceDeployError


def render_markdown_storage(
    markdown_text: str,
    filename_to_page_url: dict[str, str],
    current_page_url: str,
) -> str:
    try:
        from markdown import markdown
    except ImportError as exc:
        raise ConfluenceDeployError(
            "Missing dependency: markdown. Install workflow dependencies first."
        ) from exc

    rendered = markdown(
        markdown_text,
        extensions=["tables", "fenced_code", "sane_lists", "extra"],
    )
    rendered = convert_code_blocks(rendered)
    rendered = rewrite_links(rendered, filename_to_page_url, current_page_url)
    return inject_heading_anchors(rendered)


def convert_code_blocks(rendered_html: str) -> str:
    soup = parse_html(rendered_html)
    for pre in soup.find_all("pre"):
        code = pre.find("code")
        if not code:
            continue
        language = None
        for css_class in code.get("class", []):
            if css_class.startswith("language-"):
                language = css_class[len("language-"):]
                break
        code_text = code.get_text()
        if language:
            macro = (
                '<ac:structured-macro ac:name="code">'
                f'<ac:parameter ac:name="language">{html.escape(language)}</ac:parameter>'
                f"<ac:plain-text-body><![CDATA[{code_text}]]></ac:plain-text-body>"
                "</ac:structured-macro>"
            )
        else:
            macro = (
                '<ac:structured-macro ac:name="code">'
                f"<ac:plain-text-body><![CDATA[{code_text}]]></ac:plain-text-body>"
                "</ac:structured-macro>"
            )
        pre.replace_with(parse_html(macro))
    return str(soup)


def to_github_anchor(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    anchor = text.lower()
    anchor = re.sub(r"[^a-z0-9 -]", "", anchor)
    anchor = anchor.replace(" ", "-")
    return anchor.strip("-")


def inject_heading_anchors(rendered_html: str) -> str:
    soup = parse_html(rendered_html)
    for heading in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
        anchor = to_github_anchor(heading.get_text())
        if not anchor:
            continue
        macro = (
            '<ac:structured-macro ac:name="anchor">'
            f'<ac:parameter ac:name="">{html.escape(anchor)}</ac:parameter>'
            "</ac:structured-macro>"
        )
        heading.insert_before(parse_html(macro))
    return str(soup)


def rewrite_links(
    rendered_html: str,
    filename_to_page_url: dict[str, str],
    current_page_url: str,
) -> str:
    soup = parse_html(rendered_html)
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href.startswith("mailto:"):
            continue
        if href.startswith("#"):
            link["href"] = current_page_url + href
            continue
        if href.startswith(("http://", "https://")):
            continue
        if ".md" not in href:
            continue
        parts = href.split("#", 1)
        filename = unquote(os.path.basename(parts[0]))
        anchor = parts[1] if len(parts) > 1 else None
        page_url = filename_to_page_url.get(filename)
        if not page_url:
            continue
        link["href"] = page_url + (f"#{anchor}" if anchor else "")
    return str(soup)


def parse_html(rendered_html: str) -> Any:
    try:
        from bs4 import BeautifulSoup
    except ImportError as exc:
        raise ConfluenceDeployError(
            "Missing dependency: beautifulsoup4. Install workflow dependencies first."
        ) from exc
    return BeautifulSoup(rendered_html, "html.parser")
