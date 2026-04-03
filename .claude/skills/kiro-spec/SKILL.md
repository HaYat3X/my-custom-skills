---
name: kiro-spec
description: |
  Kiro-style spec-driven development workflow for Claude Code. Use this skill whenever the user wants to define requirements, design, or break down tasks for a new feature or project — especially when the request is vague or fuzzy. Triggers include: "要件定義したい", "設計してほしい", "新機能を作りたい", "仕様書を作って", "スペック書いて", "何から始めればいい", "タスク分解して", "実装前に整理したい". Also use when the user describes a feature idea with ambiguous scope, or asks Claude Code to "plan before building". This skill ensures Claude always does structured spec work BEFORE writing any implementation code.
---

# Kiro Spec — Spec-Driven Development for Claude Code

Kiro の Spec フローを Claude Code で再現するスキル。
**ふわっとした要件 → 具体的な設計 → タスク一覧** の順番で進め、実装前に必ずspecを固める。

## 鉄則：実装より先にSpecを書く

ユーザーが「作って」と言っても、Specが存在しない場合はまずこのフローを走らせる。
唯一の例外：`specs/` が既に存在し、内容が十分に具体的な場合。

---

## フォルダ構成

プロジェクトルートに以下を生成する：

```
specs/
├── requirements.md   # 要件定義（WHAT）
├── design.md         # 設計（HOW）
└── tasks.md          # タスク分解（TODO）
```

既に `specs/` が存在する場合は上書きせず、差分追記または新機能用サブフォルダを作る：
```
specs/
└── {feature-name}/
    ├── requirements.md
    ├── design.md
    └── tasks.md
```

---

## Phase 1: 要件ヒアリング → requirements.md

### ステップ 1-A: 曖昧な要件を引き出す

ユーザーの発言から以下を抽出・補完する。不足情報は **一度にまとめて** 質問する（何度も往復しない）：

```
ヒアリング項目：
1. 目的・背景（なぜ作るか）
2. ユーザー（誰が使うか）
3. 主要機能（何ができるか）
4. 制約・非機能要件（パフォーマンス、認証、対応環境など）
5. 既存システムとの連携
6. やらないこと（スコープ外）
```

### ステップ 1-B: requirements.md を生成する

詳細フォーマットは `references/requirements-template.md` を参照。

生成後、ユーザーに確認を取る：
> 「requirements.md を生成しました。内容を確認して、修正があれば教えてください。OKなら設計フェーズに進みます。」

---

## Phase 2: 設計 → design.md

requirements.md の内容をもとに設計を行う。

### 技術スタックの判定

`CLAUDE.md` または `package.json` / `pyproject.toml` が存在する場合は必ず読み込み、既存技術スタックに合わせる。

### design.md に含める内容

詳細フォーマットは `references/design-template.md` を参照。

生成後：
> 「design.md を生成しました。アーキテクチャや技術選定に違和感があれば教えてください。OKならタスク分解に進みます。」

---

## Phase 3: タスク分解 → tasks.md

design.md をもとに、**実装可能な最小単位** にタスクを分解する。

### タスク分解の原則

- 1タスク = 1コミットで完結するサイズ
- 依存関係を明示する（「〇〇完了後に着手」）
- 優先度をつける（Must / Should / Could）
- 見積もり時間を記載（任意だが推奨）

詳細フォーマットは `references/tasks-template.md` を参照。

生成後：
> 「tasks.md を生成しました。これで実装準備が整いました。どのタスクから始めますか？」

---

## Phase 4: 実装フェーズへの引き継ぎ

ユーザーが実装タスクを指定したら：

1. `tasks.md` 該当タスクのステータスを `[ ]` → `[x]` に更新
2. 実装を開始する
3. 実装完了後に `tasks.md` を更新する

### CLAUDE.md への自動追記（任意）

プロジェクトルートに `CLAUDE.md` が存在する場合、以下を追記することをユーザーに提案する：

```markdown
## 開発フロー
新機能の追加前に必ず `specs/` 以下にSpec文書を作成すること。
詳細は kiro-spec スキルを参照。
```

---

## エラーパターンと対処

| 状況 | 対処 |
|------|------|
| ユーザーが「とりあえず作って」と言う | 「先にSpecを5分で固めましょう」と提案してPhase 1へ |
| 要件が極端に小さい（1ファイル修正など） | Specは不要、直接実装してよい |
| 既存のSpec文書がある | 読み込んで差分のみ更新する |
| ユーザーがSpecをスキップしたがる | 1度だけ提案し、それでも拒否なら従う |

---

## 参照ファイル

- `references/requirements-template.md` — requirements.md の詳細テンプレ
- `references/design-template.md` — design.md の詳細テンプレ
- `references/tasks-template.md` — tasks.md の詳細テンプレ

各テンプレートは Phase に入ったときに読み込む（最初から全部読まなくてよい）。
