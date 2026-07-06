# Button（ボタン／選択肢）

行動・選択肢の基本要素。全幅・**左揃え**・古紙地(`--paper`)・角丸わずか(2px)。主文の下に
小さな副文(`meta`)で判定条件や注記を添えるのが本作の型。

## 使い方
```jsx
<Button meta="生まれは選べない">生まれる</Button>
<Button meta="体 vs 目標6／成功で実り" onClick={roll}>畑を打つ</Button>
<Button disabled meta="路銀が足りない">都へ出る</Button>

{/* 2択を横並びにするときは親を grid に */}
<div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:8 }}>
  <Button>受ける</Button><Button>断る</Button>
</div>
```

## 約束
- 中央揃えにしない（本作は左揃えの帳面の趣）。大きな角丸・影付き立体・グラデ塗りにしない。
- 主要な選択肢は縦積み（`gap:8`）、二択のみ grid 2列。
- 運命イベント下では親 `.fate` により地が暗赤・文字が褪せ赤へ自動転調（`styles.css`）。
  ボタン側で色を上書きしない。
- 無効は `disabled`（opacity .35）。色を変えて無効を表現しない。
