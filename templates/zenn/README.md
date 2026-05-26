# Zenn用テンプレート

Zennに投稿する記事のテンプレート集です。Qiita版をベースに、Zenn固有の Frontmatter と独自記法に対応させています。

## Zenn固有の仕様メモ

- **Frontmatter 必須**：`title` / `emoji` / `type` / `topics` / `published` の5項目
- **ファイル名 = slug**：`a-z0-9`、ハイフン`-`、アンダースコア`_` の **12〜50字**
  - テンプレートは `01_tutorial.md` のような識別用の名前。実投稿時は適切なslugにリネーム
  - 例：`my-first-nextjs-app.md`
- **topics（タグ）**：最大5個、記号・スペース不可
  - C++ → `cpp`、C# → `csharp`、Node.js → `nodejs`、.NET → `dotnet`
- **type**：`tech`（技術記事）または `idea`（アイデア記事）
- **emoji**：1文字の絵文字（アイキャッチに使われる）
- 独自記法：
  - メッセージ：`:::message` / `:::message alert`
  - 詳細折りたたみ：`:::details タイトル`
  - リンクカード：URLを単独の行に書くと自動展開
- 投稿手段：
  - Web UI（直接記事を作る）
  - GitHub連携（リポジトリの `articles/` 配下を自動同期）
  - Zenn CLI（ローカル執筆 → GitHub連携）

## このリポジトリと Zenn CLI の関係

`zenn/articles/` 配下にmd ファイルを置く構造は、Zenn CLIと互換です。  
Zenn CLI を使う場合は、`zenn/` ディレクトリ自体を `npx zenn init` した Zenn 専用リポジトリと見立てることもできます（ただしこのテンプレートリポジトリ自体は Zenn 連携用ではなく、原稿テンプレート集として使う想定）。

## 使い方

1. ジャンルに合ったファイルをコピー
2. ファイル名を slug にリネーム（必要に応じて）
3. Frontmatter を埋める（特に `topics` と `published`）
4. プレースホルダーを実内容に置き換える
5. `published: true` にして投稿

## テンプレート一覧

`articles/` 配下にあります。

| # | ジャンル | ファイル |
|---|---|---|
| 1 | チュートリアル/入門 | [articles/01_tutorial.md](./articles/01_tutorial.md) |
| 2 | ハウツー/実装解説 | [articles/02_howto.md](./articles/02_howto.md) |
| 3 | エラー解決 | [articles/03_troubleshooting.md](./articles/03_troubleshooting.md) |
| 4 | 環境構築 | [articles/04_environment.md](./articles/04_environment.md) |
| 5 | 比較/選定 | [articles/05_comparison.md](./articles/05_comparison.md) |
| 6 | Tips/小ネタ集 | [articles/06_tips.md](./articles/06_tips.md) |
| 7 | 設計/アーキテクチャ | [articles/07_architecture.md](./articles/07_architecture.md) |
| 8 | ツール紹介 | [articles/08_tool_introduction.md](./articles/08_tool_introduction.md) |
| 9 | やってみた/作ってみた | [articles/09_tried.md](./articles/09_tried.md) |
| 10 | 振り返り/学習記録 | [articles/10_retrospective.md](./articles/10_retrospective.md) |
