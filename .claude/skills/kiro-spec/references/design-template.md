# design.md テンプレート

以下のフォーマットで `specs/design.md` を生成する。
**必ず `specs/requirements.md` を読み込んでから生成すること。**

---

## テンプレート本文

```markdown
# 設計書: {機能名 / プロジェクト名}

作成日: {YYYY-MM-DD}
ステータス: Draft / Review / Approved
参照: [requirements.md](./requirements.md)

---

## 1. アーキテクチャ概要

{全体構成を一言で説明}

```
{ASCIIアート or テキストでのシステム構成図}

例:
[Browser] → [Next.js Frontend] → [API Routes] → [Notion API]
                                              ↘ [ChromaDB]
```

## 2. 技術スタック

| レイヤー | 技術 | バージョン | 選定理由 |
|---------|------|-----------|---------|
| Frontend | {例: Next.js} | {例: 14.x} | {理由} |
| Backend | {例: FastAPI} | {例: 0.110} | {理由} |
| DB | {例: ChromaDB} | {例: 0.4.x} | {理由} |
| 認証 | {例: NextAuth.js} | {例: 5.x} | {理由} |

## 3. コンポーネント設計

### {コンポーネント名A}

**責務**: {このコンポーネントが担う責任}

**インターフェース**:
```typescript
// 例
interface {ComponentName}Props {
  {propName}: {type}
}
```

**状態管理**: {useState / Zustand / Context など}

---

### {コンポーネント名B}

...

## 4. データモデル

### {エンティティ名}

```typescript
interface {EntityName} {
  id: string
  {field}: {type}
  createdAt: Date
  updatedAt: Date
}
```

**Notion対応** (Notionをバックエンドとして使う場合):

| フィールド | Notion プロパティ型 | 備考 |
|-----------|-------------------|------|
| id | title | |
| {field} | {type} | |

## 5. API設計

### エンドポイント一覧

| メソッド | パス | 説明 | 認証 |
|---------|------|------|------|
| GET | /api/{resource} | {一覧取得} | 必要 |
| POST | /api/{resource} | {作成} | 必要 |
| PATCH | /api/{resource}/{id} | {更新} | 必要 |
| DELETE | /api/{resource}/{id} | {削除} | 必要 |

### リクエスト/レスポンス例

```typescript
// POST /api/{resource}
// Request
{
  "{field}": "{value}"
}

// Response 200
{
  "id": "xxx",
  "{field}": "{value}",
  "createdAt": "2024-01-01T00:00:00Z"
}
```

## 6. ファイル構成

```
{新規追加・変更するファイルのみ記載}

src/
├── app/
│   └── {path}/
│       ├── page.tsx        # {説明}
│       └── components/
│           └── {Name}.tsx  # {説明}
├── lib/
│   └── {name}.ts           # {説明}
└── types/
    └── {name}.ts           # {説明}
```

## 7. セキュリティ考慮事項

- {考慮事項1}
- {考慮事項2}

## 8. 未解決事項 / 決定が必要な事項

| # | 事項 | 選択肢 | 推奨 | 期限 |
|---|------|--------|------|------|
| D-01 | {事項} | A / B | A | {日付} |

---

_この文書は `specs/tasks.md` の入力として使用される_
```

---

## 生成時の注意点

- 既存プロジェクトの場合は `package.json` / `CLAUDE.md` を必ず確認して技術スタックを合わせる
- コンポーネント設計はReactの場合はコンポーネント単位、バックエンドの場合はモジュール単位で書く
- 「未解決事項」は正直に書く。わからないことを隠さない
- ASCIIアート構成図は簡易でよいが必ず入れる（視覚的理解のため）
