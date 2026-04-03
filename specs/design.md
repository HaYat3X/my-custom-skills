# 設計書: 汎用GISビューワー

作成日: 2026-04-03
ステータス: Draft
参照: [requirements.md](./requirements.md)

---

## 1. アーキテクチャ概要

フロントエンドのみで完結するサーバーレスSPA。ファイル処理はすべてブラウザ内で行い、外部サーバーへのデータ送信は一切行わない。

```
[ユーザー]
    │ ドラッグ&ドロップ / URL入力
    ▼
[Vue 3 SPA]
    ├── FileDropZone（ファイル受け取り・パース）
    │       ├── GeoJSON Parser（ネイティブ）
    │       ├── shpjs（シェープファイル → GeoJSON変換）
    │       └── CSV Parser（papaparse）
    ├── LayerStore（Pinia）
    │       └── Layer[]（id, name, type, visible, style, source）
    └── MapView（OpenLayers ol/Map）
            ├── BaseMapLayer（XYZ/OSM）
            └── VectorLayer[] / TileLayer[]（レイヤーストアと同期）
```

## 2. 技術スタック

| レイヤー         | 技術                    | バージョン | 選定理由                                                 |
| ---------------- | ----------------------- | ---------- | -------------------------------------------------------- |
| UIフレームワーク | Vue 3 (Composition API) | 3.x        | ユーザー指定。リアクティブなレイヤー管理と相性良好       |
| 地図ライブラリ   | OpenLayers              | 9.x        | ユーザー指定。多様なデータソース・プロジェクションに対応 |
| 状態管理         | Pinia                   | 2.x        | Vue 3公式推奨。レイヤーリストの一元管理に最適            |
| ビルドツール     | Vite                    | 5.x        | 高速なHMRと静的ビルド                                    |
| Shapefile解析    | shpjs                   | 4.x        | ブラウザ上でSHP+DBFをGeoJSONに変換                       |
| CSV解析          | papaparse               | 5.x        | 高速・ヘッダー自動検出・文字コード対応                   |
| スタイリング     | Tailwind CSS            | 3.x        | ユーティリティファーストで素早くUI構築                   |

## 3. コンポーネント設計

### App.vue（ルートコンポーネント）

**責務**: レイアウト全体の管理。MapView・サイドパネル・DropZoneを統合する。

```
┌─────────────────────────────────────────┐
│  [Toolbar: ベースマップ切替 / タイルURL追加]    │
├──────────────┬──────────────────────────┤
│  LayerPanel  │       MapView            │
│  (240px)     │   (残り全幅・全高)         │
│              │                          │
│  □ layer1   │    [OpenLayers地図]       │
│  □ layer2   │                          │
│              │                          │
└──────────────┴──────────────────────────┘
      ↑ ドラッグ&ドロップ受付エリア（全体）
```

---

### MapView.vue

**責務**: OpenLayers の `ol/Map` インスタンスを管理。Piniaストアのレイヤーリストを監視し、OLレイヤーと同期する。

```typescript
interface MapViewProps {
  // なし（ストアから直接購読）
}
// emits: なし
// 内部: ol.Map, ol.View, watch(layerStore.layers)
```

**状態管理**: Pinia（layerStore）を購読

---

### LayerPanel.vue

**責務**: レイヤーリストの表示・操作UI（表示切替・削除・並び替え・スタイル編集ボタン）。

```typescript
// layerStore.layers を v-for でレンダリング
// ドラッグソートには VueDraggablePlus を使用
```

---

### StyleEditor.vue（モーダル / スライドオーバー）

**責務**: 選択レイヤーの塗り色・線色・透明度・サイズを編集するUI。

```typescript
interface StyleEditorProps {
  layerId: string;
}
// カラーピッカー: <input type="color">
// 透明度・サイズ: <input type="range">
```

---

### FileDropZone.vue

**責務**: ドラッグ&ドロップイベントを受け取り、ファイル種別を判定してパーサーに渡す。App.vue全体をオーバーレイする透明レイヤー。

```typescript
// dragover → ハイライト表示
// drop → FileList → parseFile(file) → layerStore.addLayer()
```

---

### TileLayerDialog.vue

**責務**: XYZ/WMS URLを入力するモーダルダイアログ。

```typescript
interface TileLayerInput {
  name: string;
  url: string;
  type: "xyz" | "wms";
  wmsLayers?: string; // WMS用
}
```

---

### AttributePopup.vue

**責務**: 地物クリック時の属性情報表示。OpenLayers の Overlay として地図上に配置。

```typescript
interface AttributePopupProps {
  feature: ol.Feature | null;
  coordinate: ol.Coordinate | null;
}
```

## 4. データモデル

### Layer（Piniaストアの中核型）

```typescript
interface Layer {
  id: string; // uuid
  name: string; // ファイル名 or 入力名
  type: "vector" | "tile";
  visible: boolean;
  opacity: number; // 0.0 ~ 1.0
  style: VectorStyle | TileStyle;
  olLayer: ol.layer.Vector | ol.layer.Tile; // OLレイヤー参照
  featureCount?: number; // ベクターレイヤーのみ
}

interface VectorStyle {
  geometryType: "point" | "line" | "polygon";
  fillColor: string; // '#rrggbb'
  strokeColor: string;
  strokeWidth: number;
  pointRadius?: number; // pointのみ
  pointShape?: "circle" | "square";
}

interface TileStyle {
  // タイルはスタイル変更なし（透明度のみLayer.opacityで管理）
}
```

### BaseMap

```typescript
interface BaseMap {
  id: string
  name: string
  url: string             // XYZ URL テンプレート
  attribution: string
}

const DEFAULT_BASEMAPS: BaseMap[] = [
  { id: 'osm', name: 'OpenStreetMap', url: 'https://{a-c}.tile.openstreetmap.org/{z}/{x}/{y}.png', ... },
  { id: 'pale', name: '地理院地図（淡色）', url: 'https://cyberjapandata.gsi.go.jp/xyz/pale/{z}/{x}/{y}.png', ... },
  { id: 'satellite', name: '衛星写真 (ESRI)', url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', ... },
]
```

## 5. ファイルパース処理

APIは存在しないため、ここではパースロジックの設計を記載する。

### src/lib/fileParser.ts

```typescript
async function parseFile(file: File): Promise<ol.source.Vector | null>;

// 判定ロジック
// .geojson / .json  → parseGeoJSON()
// .zip              → parseShapefile() (shpjs)
// .shp              → parseShapefile() (shpjs、.dbfも同時要求 or エラー)
// .csv              → parseCsv() (papaparse + 緯度経度カラム検出)
// それ以外          → エラートースト表示
```

### 緯度経度カラム自動検出ロジック

```typescript
const LAT_CANDIDATES = ["lat", "latitude", "緯度", "y"];
const LNG_CANDIDATES = ["lng", "lon", "longitude", "経度", "x"];
// ヘッダー行を小文字化して候補と照合
```

## 6. ファイル構成

```
gis-viewer/
├── index.html
├── vite.config.ts
├── package.json
├── src/
│   ├── main.ts                  # Vueアプリ初期化・Pinia登録
│   ├── App.vue                  # ルートレイアウト
│   ├── components/
│   │   ├── MapView.vue          # OpenLayers地図本体
│   │   ├── LayerPanel.vue       # レイヤーリスト・操作UI
│   │   ├── StyleEditor.vue      # スタイル編集モーダル
│   │   ├── FileDropZone.vue     # D&Dファイル受付
│   │   ├── TileLayerDialog.vue  # タイルURL入力モーダル
│   │   ├── AttributePopup.vue   # 属性ポップアップ
│   │   └── Toolbar.vue          # ベースマップ切替・タイル追加ボタン
│   ├── stores/
│   │   └── layerStore.ts        # Piniaレイヤーストア
│   ├── lib/
│   │   ├── fileParser.ts        # ファイルパース処理
│   │   ├── styleHelper.ts       # OLスタイル生成ヘルパー
│   │   └── basemaps.ts          # ベースマップ定義
│   └── types/
│       └── layer.ts             # Layer / Style 型定義
```

## 7. セキュリティ考慮事項

- ファイルはすべてクライアントサイドで処理し、外部サーバーへは送信しない
- WMS/XYZ URLは利用者が入力するが、CSPヘッダーでimgソースを制限する（静的ホスティング時）
- ファイルサイズ上限（例: 50MB）をクライアント側で検証し、過大ファイルによるブラウザクラッシュを防ぐ
- シェープファイルZIPの展開はメモリ上のみで行い、ファイルシステムへの書き込みは行わない

## 8. 未解決事項 / 決定が必要な事項

| #    | 事項                                  | 選択肢                                          | 推奨                                    | 期限   |
| ---- | ------------------------------------- | ----------------------------------------------- | --------------------------------------- | ------ |
| D-01 | シェープファイルの文字コード          | UTF-8固定 / CP932自動判定                       | CP932自動判定（日本語データ対応のため） | 実装前 |
| D-02 | 大規模GeoJSON（10万件超）の描画最適化 | WebGLレイヤー使用 / クラスタリング / スコープ外 | スコープ外（将来対応）                  | -      |
| D-03 | アプリのホスティング先                | GitHub Pages / Netlify / ローカル専用           | TBD（要確認）                           | -      |
| D-04 | レイヤーの並び替えUI                  | Vue Draggable Plus / SortableJS直接             | Vue Draggable Plus（Vue 3対応）         | 実装前 |

---

_この文書は `specs/tasks.md` の入力として使用される_
