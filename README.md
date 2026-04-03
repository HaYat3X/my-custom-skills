# my-custom-skills

> Claude Code をもっと便利に — 日常業務に特化したカスタムスキル集

## 概要

このリポジトリは [Claude Code](https://claude.ai/code) 向けのカスタムスキル（スラッシュコマンド）をまとめたものです。
Notion の要約・Python コードレビュー・README 自動生成・自己紹介文の作成など、日常的なエンジニア業務を効率化するスキルを収録しています。
スキルは `.md` ファイルとして管理されており、Claude Code の `skillsDirectories` に登録するだけで即座に利用できます。

## スキル一覧

| スキル名 | コマンド | 概要 |
|----------|----------|------|
| Notion Summarizer | `/notion` | Notion ページの URL を渡すと内容を日本語で要約する |
| Python 新人コードレビュー | `/python-review-beginner` | 初心者・新人エンジニア向けに PEP8・可読性・バグを日本語でレビュー |
| README Generator | `/readme-generator` | Git リポジトリを自動解析してプロフェッショナルな README.md を生成 |
| 自己紹介ジェネレーター | `/self-introduction` | 場面に合わせた自己紹介文（丁寧版・カジュアル版など）を生成 |

## ディレクトリ構成

```
my-custom-skills/
├── CLAUDE.md                          # Claude Code 向けのリポジトリ説明
├── README.md                          # このファイル
└── .claude/
    ├── settings.json                  # Claude Code 設定
    └── skills/
        ├── notion/
        │   └── SKILL.md               # Notion 要約スキル
        ├── python-review-beginner/
        │   └── SKILL.md               # Python コードレビュースキル
        ├── readme-generator/
        │   ├── SKILL.md               # README 生成スキル
        │   └── scripts/
        │       └── analyze_repo.py    # リポジトリ解析スクリプト
        └── self-introduction/
            └── SKILL.md               # 自己紹介生成スキル
```

## セットアップ

### 前提条件

- [Claude Code](https://claude.ai/code) がインストール済みであること
- Python 3.x（`readme-generator` スキルを使用する場合）

### インストール

1. このリポジトリをクローンします。

   ```bash
   git clone <リポジトリURL>
   ```

2. Claude Code の設定ファイル (`~/.claude/settings.json`) にスキルディレクトリを登録します。

   ```json
   {
     "skillsDirectories": [
       "/path/to/my-custom-skills/.claude/skills"
     ]
   }
   ```

3. Claude Code を再起動すると、スキルが利用可能になります。

## 使い方

Claude Code のプロンプトでスラッシュコマンドを入力するだけです。

```
/notion https://www.notion.so/your-page-url
/python-review-beginner
/readme-generator ./my-project
/self-introduction
```

### 各スキルの詳細

#### `/notion`

Notion MCP が接続済みの状態で使用します。URL を渡すとページ内容を取得し、目的・主要ポイント・詳細メモの形式で日本語要約を出力します。

#### `/python-review-beginner`

Python コードを貼り付けると、PEP8 準拠・可読性・バグの 3 観点でレビューします。良い点の指摘と改善例をセットで提示するため、学習用途にも最適です。

#### `/readme-generator`

リポジトリパスを指定すると、ファイル構成・使用言語・依存関係を自動解析し、README.md を生成・書き出しします。

#### `/self-introduction`

名前・職業・スキル・利用場面などをヒアリングし、丁寧版・カジュアル版・短文版など複数バリエーションの自己紹介文を生成します。

## スキルの追加方法

1. `.claude/skills/` 配下に新しいディレクトリを作成します。
2. `SKILL.md` を以下のフォーマットで作成します。

   ```markdown
   ---
   name: skill-name
   description: スキルの一行説明（スキルピッカーに表示されます）
   ---

   スキルのプロンプト内容をここに書きます。
   ```

3. Claude Code を再起動すると `/skill-name` として利用可能になります。
