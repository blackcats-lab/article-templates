# articles/ — 執筆記事の管理

このディレクトリは、執筆した（執筆中の）記事を管理する場所です。テンプレート（`templates/`）と分離されています。

## ディレクトリの考え方

- **`drafts/`**：執筆中・レビュー待ち・媒体未確定の記事
- **`published/`**：すでに媒体に投稿済みの記事

執筆が完了して媒体に公開したら、`drafts/` から `published/` に移動します。**ステータスで物理的にフォルダを分ける** ことで、Claudeへの指示や grep が楽になります。

日付・テーマ・媒体での分類は、**フォルダではなくフロントマターのメタ情報** で管理します。理由は以下のとおり：

- 1本の記事が複数テーマに属することは普通にある（タグなら多重所属が自然）
- 日付フォルダで切ると、年月をまたぐ大型記事や下書きの扱いが面倒になる
- 分類軸を後から変えたくなったとき、フォルダ移動より frontmatter 書き換えのほうが安全
- INDEX生成スクリプトが「テーマ別」「日付別」「媒体別」を**動的に組み直せる**

## ファイル命名規則

```
YYYY-MM-DD-{slug}-{platform}.md
```

例：

- `2026-05-23-supabase-auth-howto-zenn.md`
- `2026-05-20-react-rendering-tips-qiita.md`
- `2026-04-15-my-task-app-launch-note.md`

ルール：

- 日付は **執筆開始日**（後で公開しても変えない／変えると順序が崩れる）
- slug は `a-z0-9-` のみ（Zennのslug規則と互換にしておくと流用が楽）
- platform は `qiita` / `zenn` / `note` のいずれか

## 管理用フロントマター

すべての記事ファイルの先頭に、以下のフロントマターを付けます。

```yaml
---
# === 管理用メタ情報 ===
date: 2026-05-23
platform: zenn
genre: 09_tried
theme: ["個人開発", "Supabase", "認証"]
status: draft        # draft / review / published
url: ""              # 公開後に記入
related: []          # 同テーマで複数媒体に出した場合の対応記事ファイル名
note: ""             # 自分用メモ（任意）
# === ここから下は Zenn のみ Zenn 公式 frontmatter を併記 ===
title: "Supabaseで認証を実装する"
emoji: "🔐"
type: "tech"
topics: ["supabase", "認証", "nextjs"]
published: false
---
```

### 各フィールドの意味

| フィールド | 必須 | 説明 |
|---|---|---|
| `date` | ✅ | 執筆開始日（`YYYY-MM-DD`） |
| `platform` | ✅ | `qiita` / `zenn` / `note` / `hatena` / `devto` |
| `genre` | ✅ | テンプレート由来のジャンル（`01_tutorial` 〜 `10_retrospective`） |
| `theme` | ✅ | テーマタグの配列。日本語可、複数指定可。これが**主たる分類軸** |
| `status` | ✅ | `draft`（執筆中）／`review`（推敲中）／`published`（公開済み） |
| `url` |  | 公開後のURL。INDEX.mdで「記事を読む」リンクになる |
| `related` |  | 同テーマで複数媒体に出した場合、対応記事のファイル名（拡張子なし）を配列で |
| `note` |  | 自分用メモ。INDEX.mdには出力されない |

## 媒体ごとの投稿時の扱い

### Qiita

管理用フロントマターは投稿時に **削除** してください（Qiita側で frontmatter を解釈しないので、邪魔になる）。

### Zenn

管理用フロントマターは Zenn の公式 frontmatter と **併記** します。Zenn は未知のキーを無視するので動作上は問題ありません。  
GitHub連携で Zenn にデプロイする場合は、`templates/zenn/articles/` 配下にこのファイルを **コピー** で配置します。

### note

管理用フロントマターは投稿時に **削除** してください。note は frontmatter を表示してしまうため、必ず削る必要があります。

### はてなブログ

管理用フロントマターは投稿時に **削除** してください。記事冒頭の `[:contents]`（目次）はそのまま残します。Markdownモードでの投稿が前提です。

### Dev.to

管理用フロントマターは Dev.to の公式 frontmatter と **併記** したまま投稿しても問題ありません（未知のキーは無視されます）。GitHub Actions と Forem API を使った自動投稿でも、未知のキーは無視される設計です。気になる場合は手動で削っても可。

## ワークフロー

```
1. テンプレートを選ぶ
   └─ templates/{platform}/{genre}.md

2. 新規記事を作成
   └─ scripts/new-article.sh で半自動生成
      → articles/drafts/2026-05-23-supabase-auth-howto-zenn.md

3. Claudeに執筆を依頼

4. 推敲してstatusをreviewに

5. 媒体に投稿（管理用frontmatterの扱いは媒体ごとに対応）

6. status: published に変更、urlを記入

7. articles/drafts/ から articles/published/ に移動

8. scripts/build-index.py で INDEX.md を再生成
```

## 検索の仕方

INDEX.mdに頼らずgrepしたい場合：

```bash
# 「Supabase」をテーマに含む記事を探す
grep -r "theme:.*Supabase" articles/

# Zenn媒体の公開済み記事
grep -r "status: published" articles/published/ | grep -l "platform: zenn"

# 2026年5月の記事
ls articles/*/2026-05-*.md
```
