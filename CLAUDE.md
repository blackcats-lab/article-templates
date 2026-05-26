# CLAUDE.md

このファイルはClaude（または同等の生成AI）がこのリポジトリのテンプレートを使って記事を執筆するときの指示書です。

## 基本方針

1. **テンプレートの構造を尊重する**：見出し階層、セクションの順序は原則維持する
2. **プレースホルダーを残さない**：`〇〇`, `△△`, `（説明）` などは必ず実内容に置き換える。題材を聞かないと埋まらない場合は、その旨を伝えて確認する
3. **媒体の制約を破らない**：noteで `####` を使う、Zennで Frontmatter を抜く、などはNG（後述）
4. **生成AI利用の注意書きを必ず入れる**：媒体ごとの作法に従い、「はじめに」セクションに配置する
5. **嘘を書かない**：技術的に確信が持てない部分は推測ではなく確認するか、明示的に「未確認」と書く

## 媒体ごとの絶対ルール

### Qiita

- Frontmatter は **不要**（Web UIで設定する想定。タグやタイトルは記事冒頭のh1のみ）
- 以下のQiita独自記法を活用してよい：
  - 注釈ボックス：`:::note info` / `:::note warn` / `:::note alert`
  - コードブロックには言語名を必ず付ける（例：` ```ts `）
  - ファイル名付きコードブロック：` ```ts:src/index.ts `
- 見出しは h1（記事タイトル）+ h2/h3 を中心に使う

### Zenn

- **Frontmatter 必須**。`articles/` 配下に配置する。形式は以下：

  ```yaml
  ---
  title: "記事タイトル"
  emoji: "📝"            # 1文字の絵文字
  type: "tech"          # "tech"(技術記事) または "idea"(アイデア記事)
  topics: ["nextjs", "supabase", "個人開発"]  # 最大5つ、記号・スペース不可
  published: false      # 完成までは false、公開時に true
  ---
  ```

- topics は **記号・スペース禁止**、最大5つまで。
  - C++ → `cpp`、C# → `csharp`、Node.js → `nodejs`、.NET → `dotnet`
  - 「個人開発」「ポエム」のように日本語は可
- ファイル名は `slug` になる：`a-z0-9`、ハイフン`-`、アンダースコア`_`の **12〜50字**
  - テンプレートのファイル名（`09_tried.md`）はジャンル識別用。実投稿時はslugとして適切な名前にリネームする
- Zenn独自記法を活用してよい：
  - メッセージ：`:::message` / `:::message alert`
  - 詳細折りたたみ：`:::details タイトル`
  - リンクカード：URLを単独の行に書くと自動でカード化される

### note

- Frontmatter は **不要**（Web UIで設定）
- **見出しは h2 と h3 のみ**：`#`(h1)はタイトル扱い、`####`以降はh3に変換されるので使わない
- **`:::note info` などの独自記法は使えない**：注意喚起は `> 引用ブロック` か `**太字**` で代替
- リスト・コードブロック・引用は使えるが、装飾は控えめにする
- noteには**目次が自動生成される**（PCのみ）。見出し設計が目次品質に直結する
- 読者は**開発者以外も含む**前提で言葉選びをする：略語の初出は正式名称を添える、専門用語は1行で補足
- 個人開発の場合、**開発の動機・体験・感情**を意識的に盛り込む（noteで読まれる記事の特徴）

### はてなブログ

- Frontmatter は **不要**（カテゴリ・公開設定はWeb UIで設定）
- **Markdownモード前提**：「設定 → 編集モード → Markdownモード」を選択しておくこと
- 見出しは h1（タイトル）+ h2/h3 中心（Qiitaと同じ）
- 独自記法：
  - **目次**：本文中に `[:contents]` を1行で書くと自動生成。前後に空行が必要
  - **脚注**：`((脚注内容))` で文中に挿入。Markdown標準の `[^1]` 形式より安定
- **`:::note info` のような注釈ボックスはない**：`> 引用ブロック` か `**太字**` で代替
- HTMLが混在可（`<details>` などはそのまま書ける、前後に空行が必要）
- 読者はQiitaほど技術特化ではないが、はてブで「バズる」可能性が高い：**主張のあるタイトル**、**読みやすい目次設計** が効く
- トーン：Qiita（硬め）とnote（柔らかめ）の中間。「ブログらしい」体験談を混ぜると刺さる

### Dev.to

- **Frontmatter 必須**。形式は以下：

  ```yaml
  ---
  title: "Article Title"
  published: false               # 完成までは false
  description: "Short SEO description"
  tags: javascript, webdev, tutorial, beginners  # 最大4個、カンマ区切り、ハッシュ#は不要
  cover_image: ""                                # 1000x420 推奨
  canonical_url: ""                              # クロスポスト時のSEO重複回避
  series: ""                                     # シリーズ化したい場合の文字列
  ---
  ```

- **`tags` は最大4個**、ハッシュ`#`不要、記号・スペース不可
- **英語で書くのが原則**：Dev.to は英語圏のコミュニティ。日本語記事のクロスポストなら英訳が必要
- 独自記法（Liquid tags）：
  - `{% github user/repo %}` — GitHubリポジトリカード
  - `{% youtube VIDEO_ID %}` — YouTube埋め込み
  - `{% codepen URL %}` — CodePen埋め込み
  - `{% gist URL %}` — Gist埋め込み
  - `{% link URL %}` — 内部記事カード
- **`canonical_url`** を使って、元記事（自分のサイト / Zenn / Hashnodeなど）をSEO的に正としつつクロスポスト可能
- **`series`** に同じ文字列を指定すると自動でシリーズ化される（連載に便利）
- トーン：Zennより**柔らかくインフォーマル**、絵文字も歓迎される。「Today I Learned」級の短い記事でも歓迎される文化

## 生成AI利用の注意書き

「はじめに」セクションの直下、媒体ごとに以下の形で挿入する：

### Qiita 用

```
:::note info
当記事は生成AIによって執筆しています。内容の正確性には十分注意を払っていますが、誤った情報が含まれている可能性があります。実際にご利用の際は、公式ドキュメント等もあわせてご確認ください。
:::
```

### Zenn 用

```
:::message
当記事は生成AIによって執筆しています。内容の正確性には十分注意を払っていますが、誤った情報が含まれている可能性があります。実際にご利用の際は、公式ドキュメント等もあわせてご確認ください。
:::
```

### note / はてなブログ 用（引用ブロックで代替）

```
> **生成AIによる執筆について**
> 当記事は生成AIによって執筆しています。内容の正確性には十分注意を払っていますが、誤った情報が含まれている可能性があります。実際にご利用の際は、公式ドキュメント等もあわせてご確認ください。
```

### Dev.to 用（英語、引用ブロック）

```
> **AI-generated content notice**
> This article was written with the help of generative AI. While care has been taken to ensure accuracy, some errors may exist. Please verify critical details against official documentation.
```

## ジャンル選定（迷ったとき）

- 「Xを使ってYを作る手順」→ `02_howto.md`
- 「Xのエラーで詰まって解決した」→ `03_troubleshooting.md`
- 「個人開発で○○というアプリを作った」→ `09_tried.md`
- 「Xを半年使った所感」→ `10_retrospective.md`
- 「AとBで迷った末にAを選んだ理由」→ `05_comparison.md`

詳細は `templates/_shared/genres.md` を参照。

## 媒体間の書き直し（同じネタを別媒体に出すとき）

ユーザーが「このQiita記事をnote用に書き直して」のように依頼した場合：

1. **元の媒体のテンプレート構造を理解する**（h1の数、独自記法の使用箇所、frontmatterの有無）
2. **目的の媒体のテンプレート構造に置き換える**：

   **記法変換マトリックス**

   | From → To | Frontmatter | 独自記法 | 見出し | 言語 |
   |---|---|---|---|---|
   | → Qiita | 削除 | `:::note info` 系に変換 | そのまま | 日本語 |
   | → Zenn | 追加（title/emoji/type/topics/published） | `:::message` / `:::details` に変換 | そのまま | 日本語 |
   | → note | 削除 | 引用ブロック `>` か太字に変換 | h4以降をh3に集約 | 日本語、平易に |
   | → はてな | 削除、目次 `[:contents]` 追加 | 引用ブロックか太字に変換、脚注は `((...))` も可 | そのまま | 日本語 |
   | → Dev.to | 追加（title/published/description/tags/cover_image） | Liquid tags（`{% github %}` 等）に変換 | そのまま | **英語に翻訳** |

3. **トーンを調整する**：
   - **Qiita**：問題解決ベース、検索流入の読者を想定し結論を先出し
   - **Zenn**：技術コミュニティ向け、深掘りや背景の説明を厚く
   - **note**：個人の体験・感情・動機を厚く、専門用語を平易に
   - **はてな**：QiitaとnoteのMix、主張のあるタイトル、目次設計を意識
   - **Dev.to**：Zennより柔らかくインフォーマル、絵文字も歓迎、短くてもOK

## 記事管理用フロントマターの扱い

`articles/` 配下の記事ファイルには **管理用フロントマター** が付いている場合がある（`scripts/new-article.py` で生成された記事）。Claude が記事を編集する際の扱いは以下：

- **管理用フロントマターは触らない**：`date`, `platform`, `genre`, `theme`, `status`, `url`, `related`, `note` のフィールドは原則 Claude からは変更しない。ユーザーが明示的に変更を依頼した場合のみ書き換える
- **公式 frontmatter は触ってよい**：Zenn の `title` / `emoji` / `topics`、Dev.to の `title` / `tags` / `description` / `cover_image` などはユーザーの題材に合わせて埋める
- **ファイル冒頭の構造**：
  - Qiita / Note / はてな：`---` で囲まれた管理用 frontmatter → 本文（h1 から）
  - Zenn：`---` で囲まれた frontmatter（管理用 + Zenn 公式併記）→ 本文（h2 から、h1 は frontmatter の title が担う）
  - Dev.to：`---` で囲まれた frontmatter（管理用 + Dev.to 公式併記）→ 本文（h2 から、h1 は frontmatter の title が担う）

`status` の値が `draft` / `review` / `published` のどれであっても、Claude は依頼されたタスクをそのまま実行する（status を見て勝手に挙動を変えない）。

## チェックリスト（生成後の最終確認）

執筆後、以下を確認してから出力する：

- [ ] プレースホルダー（`〇〇`, `△△`, `[topic]`, `[XX]` などの英語も）が残っていない
- [ ] 媒体固有のルール違反がない：
  - Zenn → `topics` の形式（記号スペース不可、最大5）
  - note → `####` 以降の見出し不使用
  - はてな → `[:contents]` の前後に空行
  - Dev.to → `tags` 最大4個、ハッシュ`#`なし、本文が英語
- [ ] 生成AIの注意書きが「はじめに」直下に入っている（媒体ごとに適切な形式で）
- [ ] コードブロックに言語指定がある
- [ ] 参考リンクのURLが実在する／プレースホルダーになっていない
- [ ] ファイル名（Zenn / Dev.toならslug、それ以外は元のジャンル名でOK）
- [ ] 管理用 frontmatter（`articles/` 配下の場合）を不用意に削除・変更していない
