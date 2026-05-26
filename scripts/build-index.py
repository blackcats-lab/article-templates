#!/usr/bin/env python3
"""
build-index.py

articles/ 配下のMarkdownファイルから管理用フロントマターを読み取り、
INDEX.md を自動生成する。

使い方:
    python3 scripts/build-index.py

出力:
    リポジトリルートの INDEX.md を上書き

依存:
    Python 3.8+ の標準ライブラリのみ（PyYAMLなどの追加インストール不要）
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date as Date
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
ARTICLES_DIR = REPO_ROOT / "articles"
INDEX_PATH = REPO_ROOT / "INDEX.md"

PLATFORM_LABEL = {
    "qiita": "Qiita",
    "zenn": "Zenn",
    "note": "note",
    "hatena": "はてなブログ",
    "devto": "Dev.to",
}

STATUS_LABEL = {
    "draft": "📝 下書き",
    "review": "🔍 推敲中",
    "published": "✅ 公開",
}

GENRE_LABEL = {
    "01_tutorial": "チュートリアル",
    "02_howto": "ハウツー",
    "03_troubleshooting": "エラー解決",
    "04_environment": "環境構築",
    "05_comparison": "比較/選定",
    "06_tips": "Tips",
    "07_architecture": "設計/アーキテクチャ",
    "08_tool_introduction": "ツール紹介",
    "09_tried": "やってみた",
    "10_retrospective": "振り返り",
}


@dataclass
class Article:
    """1記事ぶんのメタ情報。"""
    path: Path  # リポジトリルートからの相対パス
    date: str = ""
    platform: str = ""
    genre: str = ""
    theme: list[str] = field(default_factory=list)
    status: str = ""
    url: str = ""
    title: str = ""
    note: str = ""

    @property
    def display_title(self) -> str:
        """表示用タイトル。title未設定時はファイル名から推測。"""
        if self.title:
            return self.title
        return self.path.stem

    @property
    def link(self) -> str:
        """INDEX.mdに書く際のリンク先。公開済みならurl、未公開ならローカルパス。"""
        if self.status == "published" and self.url:
            return self.url
        return self.path.as_posix()


# -------- フロントマター解析 --------

def parse_frontmatter(text: str) -> dict[str, Any]:
    """
    Markdownの先頭YAMLフロントマターをパースして辞書を返す。
    PyYAMLを使わず、テンプレートで実際に使う形式に限って正規表現で解析する。

    対応する形式:
      key: value
      key: "値"
      key: [item1, item2]
      key: ["item1", "item2"]

    コメント行（#で始まる行 / 行末コメント）は無視する。
    """
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not fm_match:
        return {}

    body = fm_match.group(1)
    result: dict[str, Any] = {}

    for raw_line in body.splitlines():
        # 行頭が # のコメント行はスキップ
        line = raw_line.rstrip()
        if not line.strip() or line.strip().startswith("#"):
            continue

        # 行末コメントを削る（"..." の中の # は残したいので簡易判定）
        line = _strip_trailing_comment(line)

        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)$", line)
        if not m:
            continue
        key, value = m.group(1), m.group(2).strip()
        result[key] = _parse_value(value)

    return result


def _strip_trailing_comment(line: str) -> str:
    """文字列リテラル外の # 以降を削る簡易処理。"""
    in_str: str | None = None
    for i, ch in enumerate(line):
        if in_str:
            if ch == in_str and (i == 0 or line[i - 1] != "\\"):
                in_str = None
        else:
            if ch in ('"', "'"):
                in_str = ch
            elif ch == "#":
                return line[:i].rstrip()
    return line


def _parse_value(raw: str) -> Any:
    """YAMLの右辺をPython値に変換する簡易パーサ。"""
    if not raw:
        return ""

    # 配列 [a, b, c] / ["a", "b"]
    if raw.startswith("[") and raw.endswith("]"):
        inner = raw[1:-1].strip()
        if not inner:
            return []
        items = _split_list_items(inner)
        return [_unquote(it.strip()) for it in items]

    # 真偽値
    if raw.lower() in ("true", "false"):
        return raw.lower() == "true"

    return _unquote(raw)


def _split_list_items(s: str) -> list[str]:
    """カンマ区切り、ただしクオート内のカンマは無視する。"""
    items: list[str] = []
    buf = []
    in_str: str | None = None
    for ch in s:
        if in_str:
            buf.append(ch)
            if ch == in_str:
                in_str = None
        else:
            if ch in ('"', "'"):
                in_str = ch
                buf.append(ch)
            elif ch == ",":
                items.append("".join(buf))
                buf = []
            else:
                buf.append(ch)
    if buf:
        items.append("".join(buf))
    return items


def _unquote(s: str) -> str:
    if len(s) >= 2 and s[0] == s[-1] and s[0] in ('"', "'"):
        return s[1:-1]
    return s


# -------- 記事スキャン --------

def collect_articles() -> list[Article]:
    """articles/ 配下のMarkdownを再帰的に集めて Article のリストを返す。"""
    articles: list[Article] = []
    if not ARTICLES_DIR.exists():
        return articles

    for md_path in sorted(ARTICLES_DIR.rglob("*.md")):
        # READMEはスキップ
        if md_path.name.upper().startswith("README"):
            continue

        try:
            text = md_path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError) as e:
            print(f"⚠️  読み込み失敗: {md_path} ({e})", file=sys.stderr)
            continue

        fm = parse_frontmatter(text)
        if not fm:
            print(f"⚠️  frontmatter未検出: {md_path}", file=sys.stderr)
            continue

        rel_path = md_path.relative_to(REPO_ROOT)
        article = Article(
            path=rel_path,
            date=str(fm.get("date", "")),
            platform=str(fm.get("platform", "")),
            genre=str(fm.get("genre", "")),
            theme=_normalize_theme(fm.get("theme", [])),
            status=str(fm.get("status", "")),
            url=str(fm.get("url", "")),
            title=str(fm.get("title", "")),
            note=str(fm.get("note", "")),
        )
        articles.append(article)

    return articles


def _normalize_theme(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


# -------- INDEX.md レンダリング --------

def render_index(articles: list[Article]) -> str:
    lines: list[str] = []
    lines.append("# 記事一覧 (INDEX)")
    lines.append("")
    lines.append(
        "このファイルは `scripts/build-index.py` で自動生成されています。"
        "手で編集しないでください。"
    )
    lines.append("")
    lines.append(_summary_block(articles))
    lines.append("")
    lines.append(_section_by_theme(articles))
    lines.append("")
    lines.append(_section_by_date(articles))
    lines.append("")
    lines.append(_section_by_platform(articles))
    lines.append("")
    lines.append(_section_by_status(articles))
    lines.append("")
    return "\n".join(lines)


def _summary_block(articles: list[Article]) -> str:
    total = len(articles)
    pub = sum(1 for a in articles if a.status == "published")
    draft = sum(1 for a in articles if a.status == "draft")
    review = sum(1 for a in articles if a.status == "review")

    return (
        "## サマリー\n\n"
        f"- 総記事数：**{total}**\n"
        f"- 公開済み：{pub}\n"
        f"- 推敲中：{review}\n"
        f"- 下書き：{draft}\n"
    )


def _section_by_theme(articles: list[Article]) -> str:
    by_theme: dict[str, list[Article]] = defaultdict(list)
    for a in articles:
        themes = a.theme if a.theme else ["（テーマ未設定）"]
        for t in themes:
            by_theme[t].append(a)

    if not by_theme:
        return "## テーマ別\n\n（記事がありません）\n"

    lines = ["## テーマ別", ""]
    for theme in sorted(by_theme.keys()):
        items = sorted(by_theme[theme], key=lambda a: a.date, reverse=True)
        lines.append(f"### {theme} ({len(items)}件)")
        lines.append("")
        for a in items:
            lines.append(_article_bullet(a))
        lines.append("")
    return "\n".join(lines)


def _section_by_date(articles: list[Article]) -> str:
    by_month: dict[str, list[Article]] = defaultdict(list)
    for a in articles:
        if a.date and len(a.date) >= 7:
            ym = a.date[:7]  # YYYY-MM
        else:
            ym = "（日付不明）"
        by_month[ym].append(a)

    if not by_month:
        return "## 日付別\n\n（記事がありません）\n"

    lines = ["## 日付別", ""]
    for ym in sorted(by_month.keys(), reverse=True):
        items = sorted(by_month[ym], key=lambda a: a.date, reverse=True)
        lines.append(f"### {ym} ({len(items)}件)")
        lines.append("")
        lines.append("| 日付 | タイトル | 媒体 | ジャンル | ステータス |")
        lines.append("|---|---|---|---|---|")
        for a in items:
            lines.append(_article_row(a))
        lines.append("")
    return "\n".join(lines)


def _section_by_platform(articles: list[Article]) -> str:
    by_platform: dict[str, list[Article]] = defaultdict(list)
    for a in articles:
        by_platform[a.platform or "（媒体不明）"].append(a)

    if not by_platform:
        return "## 媒体別\n\n（記事がありません）\n"

    lines = ["## 媒体別", ""]
    for pf in sorted(by_platform.keys()):
        label = PLATFORM_LABEL.get(pf, pf)
        items = sorted(by_platform[pf], key=lambda a: a.date, reverse=True)
        lines.append(f"### {label} ({len(items)}件)")
        lines.append("")
        for a in items:
            lines.append(_article_bullet(a))
        lines.append("")
    return "\n".join(lines)


def _section_by_status(articles: list[Article]) -> str:
    by_status: dict[str, list[Article]] = defaultdict(list)
    for a in articles:
        by_status[a.status or "（ステータス不明）"].append(a)

    lines = ["## ステータス別", ""]
    for status in ["draft", "review", "published"]:
        items = by_status.get(status, [])
        if not items:
            continue
        items = sorted(items, key=lambda a: a.date, reverse=True)
        label = STATUS_LABEL.get(status, status)
        lines.append(f"### {label} ({len(items)}件)")
        lines.append("")
        for a in items:
            lines.append(_article_bullet(a))
        lines.append("")
    return "\n".join(lines)


def _article_bullet(a: Article) -> str:
    """箇条書き1行ぶんを生成。"""
    pf = PLATFORM_LABEL.get(a.platform, a.platform or "?")
    genre = GENRE_LABEL.get(a.genre, a.genre or "?")
    status = STATUS_LABEL.get(a.status, a.status or "?")
    title = a.display_title
    link = a.link
    date = a.date or "----------"
    themes = ", ".join(a.theme) if a.theme else "-"
    return f"- `{date}` [{title}]({link}) — {pf} / {genre} / {status} / テーマ: {themes}"


def _article_row(a: Article) -> str:
    """テーブル1行ぶんを生成。"""
    pf = PLATFORM_LABEL.get(a.platform, a.platform or "?")
    genre = GENRE_LABEL.get(a.genre, a.genre or "?")
    status = STATUS_LABEL.get(a.status, a.status or "?")
    title = a.display_title
    link = a.link
    return f"| {a.date or '-'} | [{title}]({link}) | {pf} | {genre} | {status} |"


# -------- main --------

def main() -> int:
    articles = collect_articles()
    output = render_index(articles)
    INDEX_PATH.write_text(output, encoding="utf-8")
    print(f"✅ {INDEX_PATH.relative_to(REPO_ROOT)} を生成しました（{len(articles)}件）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
