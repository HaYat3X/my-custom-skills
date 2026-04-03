---
name: readme-generator
description: >
  Gitリポジトリのパスを受け取り、Pythonスクリプトでリポジトリ構造・言語・依存関係を自動解析し、
  プロフェッショナルなREADME.mdを生成するスキル。
  「READMEを作って」「README自動生成」「このリポジトリのREADMEを書いて」
  「readme生成」「ドキュメント自動作成」などのリクエストが来たら必ずこのスキルを使うこと。
  リポジトリパスが指定されていなくても「README作りたい」という意図が読み取れる場合はこのスキルを参照する。
---

# README Generator スキル

Gitリポジトリを解析してREADME.mdを自動生成する。
**Pythonスクリプトで情報収集 → Claude がREADMEを執筆** という2フェーズ構成。

---

## ワークフロー

### Step 1: リポジトリパスの確認

ユーザーからリポジトリのパスを受け取る。

- 指定なし → カレントディレクトリ (`.`) を使う旨を伝えて進める
- 相対パス・絶対パスどちらも可

### Step 2: 解析スクリプトの実行

以下のコマンドでリポジトリを解析する。
スクリプトは **このSKILL.mdと同じディレクトリの `scripts/analyze_repo.py`** にある。

```bash
python <skill_dir>/scripts/analyze_repo.py <repo_path>
```

**スキルディレクトリの特定方法：**
このSKILL.mdのパスから `scripts/analyze_repo.py` の絶対パスを解決すること。
例: SKILL.mdが `/path/to/readme-generator/SKILL.md` なら
スクリプトは `/path/to/readme-generator/scripts/analyze_repo.py`

出力はJSON形式。以下の情報が含まれる：

- `repo_name` : リポジトリ名
- `file_tree` : ディレクトリ構造（深さ3まで）
- `languages` : 使用言語と行数・ファイル数
- `dependencies` : package.json / requirements.txt 等の内容
- `framework_hints` : 検出されたフレームワーク（Next.js, Dockerなど）
- `env_variables` : .env.example から取得した環境変数キー一覧
- `file_counts` : 総ファイル数
- `existing_readme_snippet` : 既存READMEの冒頭（あれば参考に）

### Step 3: 追加情報のヒアリング（任意）

スクリプト結果だけでは分からない情報をユーザーに確認する。
**ただし1〜2個に絞ること。多く聞きすぎない。**

確認候補：

- プロジェクトの目的・コンセプト（スクリプトで読み取れなかった場合）
- バッジを入れるか（CI, coverage, npm versionなど）
- ターゲット読者（社内向け / OSS公開向け / 個人メモ）

### Step 4: README.md の生成

解析結果をもとに README.md を生成する。

#### 出力フォーマット

```markdown
# {プロジェクト名}

> {一行キャッチコピー}

{バッジ（必要な場合）}

## 概要

{プロジェクトの目的・何を解決するか・特徴を2〜4文で}

## 技術スタック

{言語・フレームワーク・主要ライブラリ}

## ディレクトリ構成

{ファイルツリー + 主要ディレクトリの説明}

## セットアップ

{前提条件 → インストール → 環境変数設定 → 起動 の順で}

## 使い方

{基本的な使い方・コマンド例}

## 環境変数

{.env.exampleから検出した変数の説明テーブル（あれば）}

## ライセンス

{LICENSE ファイルがあれば記載、なければ省略}
```

#### 生成ルール

- **言語**: プロジェクトが日本語ベースなら日本語、英語ベース（英語のコメント・変数名が多い）なら英語で出力
- **ディレクトリ構成**: 全ファイルを羅列せず、主要なものだけをコメント付きで
- **セットアップ**: package.json の scripts や requirements.txt から実際のコマンドを推測して記述
- **既存README**: `existing_readme_snippet` がある場合は内容を尊重しつつ拡充する
- **不明な情報**: 「TODO: 〜を記入」と明示してプレースホルダーを入れる

### Step 5: ファイルへの書き出し（確認後）

生成内容をユーザーに見せて確認を取った後、
ユーザーが希望すれば `{repo_path}/README.md` に書き出す。

**重要: 必ず以下の Python コマンドで書き出すこと。**
Claude の Write ツールを使うと Windows 環境で UTF-16 LE になり文字化けが発生するため、
Python で UTF-8 を明示して書き込む。

```bash
python -c "
content = '''{生成したREADMEの内容}'''
with open('{repo_path}/README.md', 'w', encoding='utf-8') as f:
    f.write(content)
print('README.md を UTF-8 で書き出しました')
"
```

既存のREADMEがある場合は**上書き前に必ず確認**を取ること。

---

## エラーハンドリング

| エラー           | 対応                                                 |
| ---------------- | ---------------------------------------------------- |
| パスが存在しない | ユーザーに正しいパスを確認                           |
| Pythonが使えない | スクリプトをスキップし、ディレクトリ一覧ツールで代替 |
| スクリプトエラー | エラー内容を表示し、手動解析に切り替え               |
| 権限エラー       | 読み取り可能なファイルのみで対応                     |

---

## スクリプトの場所

```
readme-generator/
├── SKILL.md          ← このファイル
└── scripts/
    └── analyze_repo.py   ← リポジトリ解析スクリプト
```
