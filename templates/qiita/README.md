# Qiita用テンプレート

Qiitaに投稿する記事のテンプレート集です。Claude執筆向けに調整しています。

## Qiita固有の仕様メモ

- **Frontmatter は不要**（タイトル・タグはWeb UIで設定）
- **記事冒頭の h1（`#`）が表示タイトルになる**
- 独自記法：
  - `:::note info` / `:::note warn` / `:::note alert`
  - コードブロックにファイル名指定可：` ```ts:src/index.ts `
  - `@[card](URL)` でリンクカード（旧仕様、現在は単にURL貼り付けでも展開される）
- 投稿手段：Web UI / Qiita CLI（GitHub Actions経由）

## 使い方

1. ジャンルに合ったファイルをコピー
2. `〇〇`, `△△` などのプレースホルダーを実内容に置き換える
3. 「はじめに」直下の生成AI注意書きを残す（AIで書いた場合）
4. Qiitaの新規記事画面に貼り付けて投稿

## テンプレート一覧

| # | ジャンル | ファイル |
|---|---|---|
| 1 | チュートリアル/入門 | [01_tutorial.md](./01_tutorial.md) |
| 2 | ハウツー/実装解説 | [02_howto.md](./02_howto.md) |
| 3 | エラー解決 | [03_troubleshooting.md](./03_troubleshooting.md) |
| 4 | 環境構築 | [04_environment.md](./04_environment.md) |
| 5 | 比較/選定 | [05_comparison.md](./05_comparison.md) |
| 6 | Tips/小ネタ集 | [06_tips.md](./06_tips.md) |
| 7 | 設計/アーキテクチャ | [07_architecture.md](./07_architecture.md) |
| 8 | ツール紹介 | [08_tool_introduction.md](./08_tool_introduction.md) |
| 9 | やってみた/作ってみた | [09_tried.md](./09_tried.md) |
| 10 | 振り返り/学習記録 | [10_retrospective.md](./10_retrospective.md) |
