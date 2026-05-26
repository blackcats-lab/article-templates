# article-templates

> Claudeで Qiita / Zenn / note / はてなブログ / Dev.to の5媒体に技術記事を書くための、テンプレート + 記事管理基盤。

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Template](https://img.shields.io/badge/template-repository-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

## これは何？

複数のブログプラットフォームに技術記事を投稿したい個人開発者のための、**執筆テンプレート集 + 記事管理基盤** です。GitHubの「Use this template」ボタンから自分のリポジトリにコピーして使います。

主な特徴：

- **5媒体 × 10ジャンル = 50テンプレート** をプリセット。媒体ごとの記法・読まれ方の違いに合わせて個別に書き分けてあります
- **Claude（または他の生成AI）に渡す `CLAUDE.md` を同梱**。プロンプトに「このリポジトリの CLAUDE.md を読んで書いて」と書くだけで、媒体仕様を守った記事を生成できます
- **記事管理は Markdown + YAMLフロントマター + Pythonスクリプト2本** のみ。データベースもSaaSも使いません。Git で完結します
- **依存ゼロ**。Python 3.8+ の標準ライブラリだけで動きます（PyYAML不要）

## 向いている人 / 向いていない人

### こんな人に向いています

- 個人開発の話を **複数のブログ媒体に出したい** 開発者
- **Claude や他のAIで記事執筆を効率化したい** 人
- **記事を Git で管理したい**（バージョン管理・履歴・ローカル編集）人
- **設定やUIに振り回されたくない**、ファイルベースが好きな人

### こんな人には不向き

- WYSIWYG エディタで書きたい人 → 各媒体の公式エディタを使ったほうが速いです
- 商用ブログ・企業オウンドメディアの運用 → CMS（WordPress, Contentful等）が向いています
- 1媒体しか使わない人 → 媒体公式のCLIや投稿フォームで十分です（Zennだけなら [Zenn CLI](https://zenn.dev/zenn/articles/zenn-cli-guide)）
- Markdown が苦手な人

## クイックスタート（5分で1本目の記事を起こす）

### Step 1: テンプレートからリポジトリを作る

このページ右上の **「Use this template」** ボタンから自分のリポジトリを作成し、ローカルに clone します。

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

### Step 2: Python が入っていることを確認

```bash
python3 --version
# Python 3.8 以上であればOK
```

### Step 3: 最初の記事を起こす

`zenn` で「やってみた」記事を書きたい場合の例：

```bash
python3 scripts/new-article.py zenn 09_tried my-first-article \
    --theme "個人開発,テスト" \
    --title "初めての記事"
```

`articles/drafts/2026-05-26-my-first-article-zenn.md` が生成されます（管理用フロントマター入り）。

### Step 4: Claudeに執筆を依頼する

Claude（Web版・Claude Code・Cursor 等）で以下のように依頼します：

```
このリポジトリの CLAUDE.md を読んで、
articles/drafts/2026-05-26-my-first-article-zenn.md の本文を書いて。

題材：（あなたが書きたいことを書く）
```

媒体仕様は CLAUDE.md に集約されているので、Claude はそれを読んで Zenn の作法に沿って書いてくれます。

### Step 5: 公開と整理

完成して媒体に投稿したら：

```bash
# status: published に書き換え、url に公開URLを記入したあと
mv articles/drafts/2026-05-26-my-first-article-zenn.md articles/published/

# INDEX.md を再生成
python3 scripts/build-index.py
```

これでルートの `INDEX.md` に公開記事の一覧が反映されます。

## できること（機能一覧）

- ✅ 5媒体 × 10ジャンル = 50種類のテンプレートから記事を生成
- ✅ 各媒体の Frontmatter・独自記法・読者層に最適化されたテンプレート
- ✅ Claudeへの執筆指示書（`CLAUDE.md`）を同梱
- ✅ 管理用フロントマターによる記事メタデータの一元管理
- ✅ テーマタグ・日付・媒体・ステータスの4軸での記事一覧自動生成
- ✅ ステータスでの物理的なフォルダ分離（`drafts/` と `published/`）
- ✅ 同じネタを複数媒体に展開するための `related:` フィールド
- ✅ Python標準ライブラリのみで動作（依存ゼロ）

## 対応プラットフォーム

| 項目 | Qiita | Zenn | note | はてな | Dev.to |
|---|---|---|---|---|---|
| メタ情報 | なし | YAML必須 | なし | なし | YAML必須 |
| 見出し | h1〜h6 | h1〜h6 | h2・h3のみ | h1〜h6 | h1〜h6 |
| 独自記法 | `:::note info` | `:::message` | なし | `[:contents]` `((脚注))` | Liquid tags |
| GitHub連携 | なし | あり | なし | API経由 | API経由 |
| 言語 | 日本語 | 日本語 | 日本語 | 日本語 | **英語** |
| 読者層 | 業務開発者・検索流入 | 開発者コミュニティ・深掘り | 開発者以外含む・ストーリー | バズ流入・主張系 | 海外開発者・即時リーチ |

媒体ごとの詳細仕様は各 `templates/<platform>/README.md` を参照してください。

## 10ジャンル

| # | ジャンル | ファイル名 | 用途 |
|---|---|---|---|
| 1 | チュートリアル/入門 | `01_tutorial.md` | 技術の基本をゼロから解説 |
| 2 | ハウツー/実装解説 | `02_howto.md` | 特定機能の実装方法を解説 |
| 3 | エラー解決 | `03_troubleshooting.md` | エラーの原因と解決策を共有 |
| 4 | 環境構築 | `04_environment.md` | 開発環境のセットアップ手順 |
| 5 | 比較/選定 | `05_comparison.md` | ツールやライブラリの比較 |
| 6 | Tips/小ネタ集 | `06_tips.md` | 便利テクニックのまとめ |
| 7 | 設計/アーキテクチャ | `07_architecture.md` | DB設計やシステム設計の解説 |
| 8 | ツール紹介 | `08_tool_introduction.md` | ライブラリやツールの紹介 |
| 9 | やってみた/作ってみた | `09_tried.md` | 個人開発や技術検証の記録 |
| 10 | 振り返り/学習記録 | `10_retrospective.md` | 経験からの学びをまとめる |

ジャンルの選び方は `templates/_shared/genres.md` に詳しく書いてあります。

## ディレクトリ構成

```
article-templates/
├── README.md                  ← このファイル
├── CLAUDE.md                  ← Claudeへの執筆指示書（媒体仕様の集約）
├── INDEX.md                   ← 自動生成される記事一覧
├── templates/                 ← テンプレート（執筆の元ネタ）
│   ├── _shared/               ←   共通の執筆ガイド、ジャンル定義
│   ├── qiita/                 ←   Qiita用 10ジャンル
│   ├── zenn/articles/         ←   Zenn用 10ジャンル（Zenn CLI互換構造）
│   ├── note/                  ←   note用 10ジャンル
│   ├── hatena/                ←   はてなブログ用 10ジャンル
│   └── devto/                 ←   Dev.to用 10ジャンル（英語）
├── articles/                  ← 執筆した記事を置く場所
│   ├── README.md              ←   記事管理の規約
│   ├── drafts/                ←   執筆中・推敲中
│   └── published/             ←   公開済み
└── scripts/
    ├── new-article.py         ← テンプレから新規記事を起こす
    └── build-index.py         ← INDEX.md を再生成する
```

## 使い方（詳細）

### 新規記事の作成

```bash
python3 scripts/new-article.py <platform> <genre> <slug> [options]
```

引数：

- `<platform>`: `qiita` / `zenn` / `note` / `hatena` / `devto`
- `<genre>`: `01_tutorial` 〜 `10_retrospective`
- `<slug>`: ファイル名末尾になる識別子。`a-z0-9-` のみ

オプション：

- `--theme "tag1,tag2,tag3"`: テーマタグ（カンマ区切り、複数指定可、日本語OK）
- `--title "記事タイトル"`: Zenn / Dev.toの場合はfrontmatterに反映される
- `--date YYYY-MM-DD`: 日付の上書き（デフォルトは今日）

実行すると `articles/drafts/YYYY-MM-DD-<slug>-<platform>.md` が生成されます。

### 記事のステータス遷移

`status` フィールドを書き換えながら進めます：

```
draft（執筆中） → review（推敲中） → published（公開済み）
```

公開したら `articles/drafts/` から `articles/published/` にファイルを移動します。

### 媒体ごとの投稿時の扱い

| 媒体 | 管理用frontmatterの扱い |
|---|---|
| Qiita | **削除して** から投稿 |
| Zenn | そのまま（GitHub連携可、`templates/zenn/articles/` 経由） |
| note | **削除して** から投稿 |
| はてなブログ | **削除して** から投稿。`[:contents]` は残す |
| Dev.to | そのままでOK（未知のキーは無視される） |

詳しくは `articles/README.md` を参照してください。

### 同じネタを複数媒体に展開する

1本のネタを複数媒体に出すときは、コピペではなく **媒体ごとに書き直す** ことを推奨します。各記事の `related:` フィールドに対応記事のファイル名を入れておくと、関連が追跡できます。

```yaml
related: ["2026-05-23-my-app-qiita", "2026-05-23-my-app-zenn"]
```

`CLAUDE.md` に「Qiita版 → Zenn版に書き直す」のような媒体間変換のチェックポイントも記載されています。

### INDEX.mdの再生成

```bash
python3 scripts/build-index.py
```

ルートの `INDEX.md` が再生成されます。以下の4軸で記事一覧が出力されます：

- テーマ別
- 日付別（年月ごと）
- 媒体別
- ステータス別

## Claudeとの連携

このプロジェクトの肝は、**`CLAUDE.md` に媒体仕様を集約することで、AIに毎回ルールを説明しなくて済む** 点です。

### 基本のプロンプトテンプレート

```
このリポジトリの CLAUDE.md を読んで、
articles/drafts/<ファイル名>.md の本文を書いて。

題材：<書きたい内容を一段落で>
```

これだけで、Claude は媒体仕様（Frontmatter、独自記法、見出し階層、トーン）を守って書いてくれます。

### 媒体間の書き直しを依頼する場合

```
articles/published/2026-05-23-react-tips-qiita.md をベースに、
note版を articles/drafts/ に作成して。
媒体に合わせてトーンと構造を書き直して。
```

### Claude Code / Cursor との相性

このリポジトリは `CLAUDE.md` パターンを採用しているため、Claude Code、Cursor、Continue.dev など、**プロジェクトルートの規約ファイルを参照するツール全般** と相性が良いです。

### 他のAI（GPT, Gemini等）でも使える？

`CLAUDE.md` という名前ですが、中身は単なるMarkdownの執筆ガイドです。GPT-4 や Gemini 等にも「このファイルの規約に従って書いて」と渡せば動作します。ファイル名を変えたい場合は次のセクション「カスタマイズ」を参照してください。

## カスタマイズ

### 使わない媒体を削除する

たとえば「Dev.toは使わない」場合：

1. `templates/devto/` ディレクトリを削除
2. `scripts/new-article.py` の `VALID_PLATFORMS` から `"devto"` を削除
3. `scripts/build-index.py` の `PLATFORM_LABEL` から `"devto"` を削除
4. `CLAUDE.md` の Dev.to 関連セクションを削除（任意）

### 新しい媒体を追加する

たとえば Hashnode を追加したい場合：

1. `templates/hashnode/` ディレクトリを作って10ジャンルのMarkdownを置く（Dev.to版をコピーして調整するのが楽）
2. `scripts/new-article.py` の `VALID_PLATFORMS` に `"hashnode"` を追加
3. Hashnodeが既存frontmatterを持つ場合、`_build_article` の分岐に追加
4. `scripts/build-index.py` の `PLATFORM_LABEL` にラベルを追加
5. `CLAUDE.md` に Hashnode 固有のルールを追記

### ジャンルを増やす/減らす

`scripts/new-article.py` の `VALID_GENRES` を編集し、対応するMarkdownファイルを各 `templates/<platform>/` に追加/削除します。

### CLAUDE.md の中身を自分用にカスタマイズする

- 自分の書き方の好み（一人称、文体、絵文字の有無）を「基本方針」に追記
- よく使う題材ドメイン（フロントエンド、データ分析等）に応じて言葉遣いを調整
- AI注意書きの文面を変える

### 他のAIに使わせるためにファイル名を変える

`CLAUDE.md` を `AI_GUIDE.md` や `.cursorrules` などに名前変更してもOK。  
ただしリポジトリ内の参照（README、各READMEなど）も合わせて修正してください。

## FAQ

### Q. Claude 以外でも使えますか？

A. はい。`CLAUDE.md` は単なるMarkdownの執筆ガイドです。GPT-4、Gemini、Claude以外のLLM全般で「このファイルの規約に従って書いて」と指示すれば動きます。

### Q. 日本語以外の媒体は対応していますか？

A. 現状は日本語4媒体（Qiita / Zenn / note / はてな） + 英語1媒体（Dev.to）です。他言語の媒体に対応したい場合は「カスタマイズ」の手順で追加できます。

### Q. Zenn CLI との連携は？

A. `templates/zenn/articles/` を Zenn の `articles/` と同名にしてあるので、Zenn CLI 用リポジトリとして使うこともできます。執筆した Zenn 記事を `templates/zenn/articles/` にコピーすれば、Zenn の GitHub 連携でデプロイされます（同期スクリプトは未提供。必要に応じて作成してください）。

### Q. GitHub Actions で INDEX.md を自動更新したい

A. 標準では用意していませんが、`.github/workflows/` に以下のような YAML を置けば実現できます：

```yaml
name: Update INDEX
on:
  push:
    paths: ['articles/**']
jobs:
  update-index:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python3 scripts/build-index.py
      - run: |
          git config user.name "github-actions"
          git config user.email "actions@github.com"
          git add INDEX.md
          git diff --cached --quiet || git commit -m "chore: update INDEX.md"
          git push
```

### Q. 既存のブログ記事を取り込めますか？

A. はい。`articles/published/YYYY-MM-DD-<slug>-<platform>.md` に管理用frontmatterを付けて配置すれば、`build-index.py` で一覧に取り込まれます。`new-article.py` で空の記事を作って中身を入れ替えるのが楽です。

### Q. 商用利用していいですか？

A. MITライセンスなので、商用・非商用問わず自由に使えます。

## コントリビューション

Issue・PRは歓迎します。

- **媒体追加の提案**：新しいプラットフォームのテンプレートを足したい場合は、まず Issue でユースケースを共有してください
- **テンプレート改善**：既存テンプレートの構造改善、プレースホルダーの追加など
- **バグ報告**：スクリプトの不具合、誤字など

大きな変更を入れる前に Issue で議論できると嬉しいです。

## ライセンス

[MIT](./LICENSE)
