# Chip（チップ／タグ）

現在の状態・連れ・恒久タグを示す極小の枠。ステータスの下、`#tag-row` に横並びで置く。

## バリエーション
- `default` … 一時的な状態（飢え・病など）。褪せた色。
- `on` … 有効な才能・業（金）。「効いている」ものを金で立てる。
- `mate` … 連れ・縁者（緑がかった色）。
- `tag` … 生涯にわたる恒久タグ（刻印など）。

## 使い方
```jsx
<div style={{ display:"flex", gap:5, flexWrap:"wrap" }}>
  <Chip>飢え</Chip>
  <Chip variant="on">賭博の才</Chip>
  <Chip variant="mate">連れ・おぬい</Chip>
  <Chip variant="tag">廃坑の刻印</Chip>
</div>
```

## 約束
- 極小(11px)・角丸2px・縁取りのみ。塗り潰したバッジ・丸ピル・発光にしない。
- 4系統の色分けを守り、新色を足さない。数が多い時は折り返す（`flex-wrap`）。
