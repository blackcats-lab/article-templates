# Dev.to (DEV Community) 用テンプレート

Dev.to に投稿する記事のテンプレート集です。**英語** での執筆を前提にしています。日本語記事をクロスポストする場合は、まず英訳または英語で書き直すことをおすすめします（Dev.to は英語圏のプラットフォームのため）。

## Dev.to 固有の仕様メモ

- **Frontmatter 必須**。形式は以下：

  ```yaml
  ---
  title: "Your Article Title"
  published: false               # true で即公開、false で下書き
  description: "Short description for SEO and social cards"
  tags: javascript, webdev, beginners, tutorial  # 最大4個、カンマ区切り、ハッシュ#は不要
  cover_image: https://example.com/cover.png     # 推奨サイズ 1000x420
  canonical_url: https://your-site.com/post      # 元記事URL（クロスポスト時のSEO重複回避）
  series: "My Series Name"                       # シリーズ化したい場合の文字列
  ---
  ```

- **`tags` は最大4個**。記号・スペース不可。ハッシュ (`#`) は付けない。
- **`cover_image` は 1000x420 推奨**。SNSカードに使われる。
- **`canonical_url`**：他のブログ（自分のサイト、Hashnode、Medium 等）が一次配信元なら、その URL を指定して SEO の重複問題を回避できる。
- **`series`**：同じ文字列を持つ記事が自動でシリーズ化される。連載に便利。
- **Markdown + Liquid tags**：標準 Markdown に加え、Dev.to 独自の埋め込み記法が使える：
  - `{% github user/repo %}` — GitHub リポジトリカード
  - `{% youtube VIDEO_ID %}` — YouTube 動画埋め込み
  - `{% codepen URL %}` — CodePen 埋め込み
  - `{% gist URL %}` — Gist 埋め込み
  - `{% link URL %}` — 内部記事の埋め込みカード
- 投稿手段：Web UI / Forem API / GitHub Actions（CI連携で自動投稿可能）

## 読者層と書き方の傾向

Dev.to は **海外（英語圏）の開発者コミュニティ** で、Zenn に近い性質を持ちます。

- フィード経由の即時リーチが強い（新着記事がトップで露出される）
- **コメント文化が活発**：「First post」「Welcome」「Great post!」などの反応が多い
- 初心者向け（`beginners` タグ）と中上級者向け（`javascript`, `react`, `typescript` など）のバランスが取れている
- 短く、頻繁に投稿する記事も歓迎される（「Today I Learned」系も読まれる）
- **絵文字とインフォーマルなトーンが好まれる**：Zenn より柔らかい印象

## 推奨タグ戦略

`tags` は最大4個までしか付けられないので戦略的に。広く検索される定番タグと、ニッチで競争が少ないタグを組み合わせるのが効果的です。

### 定番タグ（読者が多い）

`javascript`, `webdev`, `programming`, `beginners`, `tutorial`, `python`, `react`, `typescript`, `node`, `css`, `html`, `devops`, `aws`, `discuss`, `productivity`, `career`, `opensource`, `ai`

### 組み合わせ例

- React のチュートリアル → `react`, `javascript`, `webdev`, `beginners`
- 個人開発の話 → `showdev`, `webdev`, `discuss`, `productivity`
- AI/LLM 関連 → `ai`, `machinelearning`, `python`, `tutorial`

## 使い方

1. ジャンルに合ったファイルをコピー
2. Frontmatter を埋める（特に `tags` と `published`）
3. プレースホルダー（`[topic]`, `[XX]` など）を実内容に置き換える
4. 完成したら `published: true` にしてコミット、または Web UI で貼り付け

## テンプレート一覧

| # | Genre | File |
|---|---|---|
| 1 | Tutorial / Getting Started | [01_tutorial.md](./01_tutorial.md) |
| 2 | How-to / Implementation Guide | [02_howto.md](./02_howto.md) |
| 3 | Troubleshooting | [03_troubleshooting.md](./03_troubleshooting.md) |
| 4 | Environment Setup | [04_environment.md](./04_environment.md) |
| 5 | Comparison | [05_comparison.md](./05_comparison.md) |
| 6 | Tips & Tricks | [06_tips.md](./06_tips.md) |
| 7 | Architecture / Design | [07_architecture.md](./07_architecture.md) |
| 8 | Tool Introduction | [08_tool_introduction.md](./08_tool_introduction.md) |
| 9 | I Built X / Show Dev | [09_tried.md](./09_tried.md) |
| 10 | Retrospective / Lessons Learned | [10_retrospective.md](./10_retrospective.md) |
