# DieFace（骰子）

2D6判定の主役。物質としての重みを持たせる。骨を彫った白い骰子（`bone`）と、黒曜石を磨いた
骰子（`obsidian`）の2質感。目の配置は原典 `PIP_POS` に厳密準拠。

## 使いどころ
- ダイス判定オーバーレイ（暗転した画面中央に2つ並べ、下に計算式、上に朱印）。
- 転がる演出は `rolling` を数百ms入れてから確定目に差し替える。

## 使い方
```jsx
<div className="dice-row" style={{ display:"flex", gap:22 }}>
  <DieFace n={1} />
  <DieFace n={1} />          {/* 出目2＝大失敗。紋章と同じ「両1」 */}
</div>

<DieFace n={4} variant="obsidian" size={72} />
```

## 約束
- 面のグラデ（`radial-gradient` 32%/26%のハイライト）と `box-shadow` が物質感の要。平面の
  ベタ塗りにしない。
- 骨は目が暗色、黒曜は目が骨色（`--ink`）。この反転を守る。
- 動きは「骰子」枠として許可された3箇所の1つ。`prefers-reduced-motion` 時は `rolling` を無効化。
- 発光・ネオン枠・絵文字ダイスは禁止。
