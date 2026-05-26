#!/usr/bin/env python3
"""
new-article.py

テンプレートから新規記事ファイルを作成し、articles/drafts/ に配置する。
管理用フロントマターを自動付与する。

使い方:
    python3 scripts/new-article.py <platform> <genre> <slug> [--theme tag1,tag2]

例:
    python3 scripts/new-article.py zenn 09_tried supabase-auth-howto \\
        --theme 個人開発,Supabase,認証

オプション:
    --theme   テーマタグをカンマ区切りで指定（後で frontmatter を手で編集してもOK）
    --date    日付を上書き（YYYY-MM-DD）。デフォルトは今日
    --title   タイトル（Zennのみ frontmatter に埋め込まれる）
"""

from __future__ import annotations

import argparse
import sys
from datetime import date as DateCls
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = REPO_ROOT / "templates"
DRAFTS_DIR = REPO_ROOT / "articles" / "drafts"

VALID_PLATFORMS = ["qiita", "zenn", "note", "hatena", "devto"]
VALID_GENRES = [
    "01_tutorial", "02_howto", "03_troubleshooting", "04_environment",
    "05_comparison", "06_tips", "07_architecture", "08_tool_introduction",
    "09_tried", "10_retrospective",
]


def main() -> int:
    args = parse_args()

    # 入力チェック
    if args.platform not in VALID_PLATFORMS:
        print(f"❌ platformは {VALID_PLATFORMS} のいずれか", file=sys.stderr)
        return 1
    if args.genre not in VALID_GENRES:
        print(f"❌ genreは {VALID_GENRES} のいずれか", file=sys.stderr)
        return 1
    if not _is_valid_slug(args.slug):
        print("❌ slugは a-z0-9- のみ使用可", file=sys.stderr)
        return 1

    # テンプレート読み込み
    template_path = _resolve_template_path(args.platform, args.genre)
    if not template_path.exists():
        print(f"❌ テンプレートが見つかりません: {template_path}", file=sys.stderr)
        return 1

    template_text = template_path.read_text(encoding="utf-8")

    # 出力先パス
    date_str = args.date or DateCls.today().isoformat()
    filename = f"{date_str}-{args.slug}-{args.platform}.md"
    out_path = DRAFTS_DIR / filename

    if out_path.exists():
        print(f"❌ 既に存在します: {out_path}", file=sys.stderr)
        print("   別のslugを使うか、既存ファイルを削除してください", file=sys.stderr)
        return 1

    # frontmatter付与
    final_text = _build_article(
        template_text=template_text,
        platform=args.platform,
        genre=args.genre,
        date_str=date_str,
        theme=args.theme,
        title=args.title,
    )

    DRAFTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path.write_text(final_text, encoding="utf-8")

    print(f"✅ 作成しました: {out_path.relative_to(REPO_ROOT)}")
    print()
    print("次のステップ:")
    print(f"  1. {out_path.relative_to(REPO_ROOT)} を開いて執筆する")
    print("  2. 完成したらClaudeに整形を依頼する")
    print("  3. 公開したら status: published に変更し、urlを記入")
    print(f"  4. ファイルを articles/published/ に移動")
    print("  5. python3 scripts/build-index.py で INDEX.md を更新")
    return 0


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="テンプレートから新規記事を作成する",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="例: python3 scripts/new-article.py zenn 09_tried my-app --theme 個人開発,Next.js",
    )
    p.add_argument("platform", help=f"媒体: {'/'.join(VALID_PLATFORMS)}")
    p.add_argument("genre", help="ジャンル（例: 09_tried）")
    p.add_argument("slug", help="記事のスラッグ（a-z0-9-）")
    p.add_argument("--theme", default="", help="テーマタグ（カンマ区切り）")
    p.add_argument("--date", default="", help="日付（YYYY-MM-DD）デフォルトは今日")
    p.add_argument("--title", default="", help="記事タイトル")
    return p.parse_args()


def _is_valid_slug(slug: str) -> bool:
    if not slug:
        return False
    return all(c.isalnum() and c.isascii() and c.islower() or c == "-" for c in slug)


def _resolve_template_path(platform: str, genre: str) -> Path:
    if platform == "zenn":
        return TEMPLATES_DIR / "zenn" / "articles" / f"{genre}.md"
    return TEMPLATES_DIR / platform / f"{genre}.md"


def _build_article(
    *,
    template_text: str,
    platform: str,
    genre: str,
    date_str: str,
    theme: str,
    title: str,
) -> str:
    """テンプレートに管理用frontmatterを差し込む。"""
    theme_list = _format_theme_list(theme)
    title_for_fm = title or ""

    if platform in ("zenn", "devto"):
        # Zenn / Dev.to のテンプレートは既に公式frontmatterを持つので、
        # その内側に管理用フィールドを追加する形で再構築
        return _inject_into_existing_frontmatter(
            template_text=template_text,
            platform=platform,
            date_str=date_str,
            genre=genre,
            theme_list=theme_list,
            title=title_for_fm,
        )
    else:
        # Qiita / Note / はてな は frontmatter がないので、先頭に管理用 frontmatter を付与
        return _prepend_management_frontmatter(
            template_text=template_text,
            platform=platform,
            date_str=date_str,
            genre=genre,
            theme_list=theme_list,
        )


def _format_theme_list(theme: str) -> str:
    """カンマ区切りテーマをYAML配列形式の文字列に。"""
    if not theme:
        return "[]"
    items = [t.strip() for t in theme.split(",") if t.strip()]
    quoted = [f'"{t}"' for t in items]
    return "[" + ", ".join(quoted) + "]"


def _prepend_management_frontmatter(
    *, template_text: str, platform: str, date_str: str, genre: str, theme_list: str
) -> str:
    fm = (
        "---\n"
        "# === 管理用メタ情報（投稿時は削除すること） ===\n"
        f"date: {date_str}\n"
        f"platform: {platform}\n"
        f"genre: {genre}\n"
        f"theme: {theme_list}\n"
        "status: draft\n"
        'url: ""\n'
        "related: []\n"
        'note: ""\n'
        "---\n\n"
    )
    return fm + template_text


def _inject_into_existing_frontmatter(
    *,
    template_text: str,
    platform: str,
    date_str: str,
    genre: str,
    theme_list: str,
    title: str,
) -> str:
    """既存frontmatterを持つテンプレ（Zenn / Dev.to）に管理用フィールドを混ぜ込む。"""
    import re

    # 既存frontmatterを抽出
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", template_text, re.DOTALL)
    if not m:
        # frontmatterが見つからなければ通常版にフォールバック
        return _prepend_management_frontmatter(
            template_text=template_text,
            platform=platform,
            date_str=date_str,
            genre=genre,
            theme_list=theme_list,
        )

    existing_fm = m.group(1)
    body = template_text[m.end():]

    # タイトルが指定されていればテンプレートのtitle行を置換
    if title:
        existing_fm = re.sub(
            r'^title:\s*".*?"$',
            f'title: "{title}"',
            existing_fm,
            count=1,
            flags=re.MULTILINE,
        )

    # 公式frontmatterのラベル（コメント）
    official_label = {
        "zenn": "# === Zenn公式 frontmatter ===",
        "devto": "# === Dev.to公式 frontmatter ===",
    }.get(platform, "# === 公式 frontmatter ===")

    new_fm = (
        "---\n"
        "# === 管理用メタ情報 ===\n"
        f"date: {date_str}\n"
        f"platform: {platform}\n"
        f"genre: {genre}\n"
        f"theme: {theme_list}\n"
        "status: draft\n"
        'url: ""\n'
        "related: []\n"
        'note: ""\n'
        f"{official_label}\n"
        f"{existing_fm}\n"
        "---\n\n"
    )
    return new_fm + body


if __name__ == "__main__":
    sys.exit(main())
