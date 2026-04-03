# タスク一覧: 汎用GISビューワー

作成日: 2026-04-03
参照: [requirements.md](./requirements.md) / [design.md](./design.md)

## 進捗サマリー

- 総タスク数: 18
- 完了: 0 / 18
- Must: 12件 / Should: 4件 / Could: 2件
- 合計見積もり: 約20〜26時間

---

## タスク一覧

### Phase 1: 基盤整備

- [ ] **T-01** 〔Must〕プロジェクト初期化
  - 内容: `npm create vite@latest gis-viewer -- --template vue-ts` でVue 3 + TypeScript + Viteプロジェクトを作成。Tailwind CSS・Pinia・OpenLayersをインストール
  - 成果物: `package.json`, `vite.config.ts`, `tailwind.config.js`
  - 見積: 30min
  - 依存: なし

- [ ] **T-02** 〔Must〕型定義ファイルの作成
  - 内容: `src/types/layer.ts` に `Layer`, `VectorStyle`, `TileStyle`, `BaseMap` インターフェースを定義する
  - 成果物: `src/types/layer.ts`
  - 見積: 30min
  - 依存: T-01完了後

- [ ] **T-03** 〔Must〕Piniaレイヤーストアの実装
  - 内容: `src/stores/layerStore.ts` に `layers[]` の追加・削除・表示切替・スタイル更新・並び替えアクションを実装する
  - 成果物: `src/stores/layerStore.ts`
  - 見積: 1h
  - 依存: T-02完了後

- [ ] **T-04** 〔Must〕ベースマップ定義とOLマップ初期化
  - 内容: `src/lib/basemaps.ts` に3種のベースマップを定義。`MapView.vue` でOLマップを初期化してOSMを表示する
  - 成果物: `src/lib/basemaps.ts`, `src/components/MapView.vue`（骨格）
  - 見積: 1h
  - 依存: T-01完了後

### Phase 2: ファイル読み込み

- [ ] **T-05** 〔Must〕GeoJSONパーサーの実装
  - 内容: `src/lib/fileParser.ts` にGeoJSON読み込み処理を実装。`ol/format/GeoJSON` でパースし `ol.source.Vector` を返す
  - 成果物: `src/lib/fileParser.ts`（GeoJSON部分）
  - 見積: 1h
  - 依存: T-03完了後

- [ ] **T-06** 〔Must〕シェープファイルパーサーの実装
  - 内容: `shpjs` を使いZIPまたはSHP+DBFをGeoJSONに変換してOLソースを生成する。文字コードCP932の自動判定も実装
  - 成果物: `src/lib/fileParser.ts`（SHP部分）
  - 見積: 2h
  - 依存: T-05完了後

- [ ] **T-07** 〔Must〕CSVパーサーの実装
  - 内容: `papaparse` でCSVをパース。緯度経度カラムを自動検出してポイントフィーチャーを生成する
  - 成果物: `src/lib/fileParser.ts`（CSV部分）
  - 見積: 1h
  - 依存: T-05完了後

- [ ] **T-08** 〔Must〕ドラッグ&ドロップUIの実装
  - 内容: `FileDropZone.vue` で dragover/drop イベントを処理。ファイル種別を判定してfileParser経由でレイヤーをストアに追加する。ドロップ中の視覚フィードバック（ハイライト）も実装
  - 成果物: `src/components/FileDropZone.vue`
  - 見積: 1.5h
  - 依存: T-05, T-06, T-07完了後

- [ ] **T-09** 〔Must〕タイルレイヤー追加ダイアログの実装
  - 内容: `TileLayerDialog.vue` でXYZ/WMS URLを入力・バリデーションしてOLタイルレイヤーをストアに追加する
  - 成果物: `src/components/TileLayerDialog.vue`
  - 見積: 1.5h
  - 依存: T-03完了後

### Phase 3: 地図連携・レイヤー管理

- [ ] **T-10** 〔Must〕ストア→OLマップのレイヤー同期
  - 内容: `MapView.vue` で `layerStore.layers` を `watch` し、追加・削除・表示切替・順序変更をOLマップに反映する
  - 成果物: `src/components/MapView.vue`（同期処理追加）
  - 見積: 2h
  - 依存: T-04, T-03完了後

- [ ] **T-11** 〔Must〕レイヤーパネルの実装
  - 内容: `LayerPanel.vue` でレイヤーリストを表示。表示/非表示チェックボックス・削除ボタン・スタイル編集ボタンを実装。VueDraggablePlusで並び替えを実装
  - 成果物: `src/components/LayerPanel.vue`
  - 見積: 2h
  - 依存: T-03完了後

- [ ] **T-12** 〔Must〕属性ポップアップの実装
  - 内容: `MapView.vue` にOLのクリックイベントハンドラを追加。`AttributePopup.vue` をOL Overlayとして配置し、クリックしたフィーチャーの属性を表示する
  - 成果物: `src/components/AttributePopup.vue`, `MapView.vue`（更新）
  - 見積: 2h
  - 依存: T-10完了後

### Phase 4: スタイル・ベースマップ

- [ ] **T-13** 〔Must〕OLスタイルヘルパーの実装
  - 内容: `src/lib/styleHelper.ts` に `VectorStyle` からOLの `ol/style/Style` オブジェクトを生成するヘルパー関数を実装
  - 成果物: `src/lib/styleHelper.ts`
  - 見積: 1.5h
  - 依存: T-02完了後

- [ ] **T-14** 〔Must〕スタイル編集UIの実装
  - 内容: `StyleEditor.vue` でカラーピッカー（`<input type="color">`）・透明度スライダー・サイズスライダーを実装。変更即時反映
  - 成果物: `src/components/StyleEditor.vue`
  - 見積: 2h
  - 依存: T-13, T-11完了後

- [ ] **T-15** 〔Should〕ベースマップ切替UIの実装
  - 内容: `Toolbar.vue` にベースマップセレクターを追加。OSM・地理院（淡色）・衛星写真を切り替え可能にする
  - 成果物: `src/components/Toolbar.vue`, `src/components/MapView.vue`（更新）
  - 見積: 1h
  - 依存: T-04完了後

### Phase 5: 品質向上・仕上げ

- [ ] **T-16** 〔Should〕エラーハンドリングとユーザーフィードバック
  - 内容: ファイルパース失敗・対応外形式・サイズ超過時のトーストエラー通知を実装。ローディングスピナーも追加
  - 成果物: `src/components/Toast.vue`（または既存ライブラリ活用）
  - 見積: 1h
  - 依存: T-08完了後

- [ ] **T-17** 〔Should〕ファイルサイズ上限チェック
  - 内容: 50MB超のファイルをドロップした際に警告を表示して処理をスキップする。T-16のエラーハンドリングと統合
  - 成果物: `src/lib/fileParser.ts`（バリデーション追加）
  - 見積: 30min
  - 依存: T-16完了後

- [ ] **T-18** 〔Could〕レイヤーのズームフィット機能
  - 内容: レイヤーパネルの「ズーム」ボタンクリックで地図がそのレイヤーの範囲にフィットする
  - 成果物: `src/components/LayerPanel.vue`（更新）, `src/components/MapView.vue`（更新）
  - 見積: 1h
  - 依存: T-11, T-10完了後

- [ ] **T-19** 〔Could〕フィーチャー件数・Geometry種別の表示
  - 内容: レイヤーパネルに「1,234件 / ポリゴン」のようなメタ情報を表示する
  - 成果物: `src/components/LayerPanel.vue`（更新）
  - 見積: 30min
  - 依存: T-11完了後

---

## 優先度の定義

| 優先度 | 意味 |
|--------|------|
| Must | リリース必須。これがないと機能しない |
| Should | 重要だが一時的に省略可能 |
| Could | あると嬉しいが後回しでよい |

## タスク更新ルール

実装完了時は `[ ]` → `[x]` に変更する。
途中で仕様変更があった場合は tasks.md を更新してから実装を続ける。

## 実装推奨順序

```
T-01 → T-02 → T-03 → T-04（並行可）
         ↓
T-13 → T-05 → T-06 → T-07 → T-08
         ↓               ↓
      T-09            T-10 → T-12
                        ↓
                      T-11 → T-14
                        ↓
                      T-15 → T-16 → T-17 → T-18, T-19
```
