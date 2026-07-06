# 無法の国に生まれて — デザインシステム指針

スマホ縦画面（基準幅 480px）のテキスト×2D6ダイス・ローグライク。主題は
**「滅びゆく王国で、蝋燭の灯りで読まれる年代記」**。プレイヤーが見ているのは画面ではなく
**死者の記録簿**。トーンは乾いた・荘厳・救いがない。ホラーでも感傷でもなく、死を事実として記す。

出力は **HTML/CSS/SVG のみ**（画像ファイル不可・単一HTML運用が最終形）。フォントは
Google Fonts の **しっぽり明朝（Shippori Mincho）のみ**。`prefers-reduced-motion` を必ず尊重。

## 使い方・土台（最初に読むもの）
- 全デザインは `styles.css` を受け取る。その `@import` 先 `tokens/tokens.css` に確定トークンが
  CSS変数で入っている。**この変数を必ず使う**（生の16進を新規に書かない）。
- ルート要素は `#app`（`max-width:480px`・縦フレックス・`overflow:hidden`）。画面は
  `.screen`、表示中は `.screen.active`。環境光は `#candle`＋`#grain` を `#app` 直下に置く。
- 運命（不吉な転調）モードは `#app` に `.fate` を付けるだけで、枠・本文・選択肢・骰子が
  赤基調へ切り替わる（`styles.css` にルールあり）。赤文字化の一歩先を作るときも `.fate` を土台に。

## スタイルの流儀（CSSクラス＋トークン変数）
ユーティリティ・フレームワークではない。**素の要素＋少数のクラス＋`var(--*)`** で書く。
新しい色を発明しない。使う変数（`tokens/tokens.css` に実在）:

| 変数 | HEX | 用途 |
|---|---|---|
| `--soot` | #14100c | 背景（煤） |
| `--paper` | #221b13 | カード・ボタン地（古紙） |
| `--paper2` | #2b231a | 押下時の地 |
| `--ink` | #d9cfba | 本文（生成り） |
| `--dim` | #8a7f6c | 補助文字・ラベル |
| `--bone` | #ece2cb | 見出し・数値・骰子（骨） |
| `--blood` | #a63d2e | 死・大失敗・運命（乾血） |
| `--gold` | #bd9448 | 金銭・業・天寿・伝説（燻金） |
| `--line` | #3a3126 | 罫・枠線 |
| `--sil` | #0c0906 | 影・シルエット |
| `--candle` | #e0aa60 | 環境光（燭光） |

主要クラス（`styles.css` に実在）: `.screen` / `.screen.active`、`button`（既定でカード地・
角丸2px・左揃え）、`button .meta`（副文）、`.chip`（`.on`金／`.mate`縁／`.tag`）、
`#statusbar`（齢=骨・銭=金・傷=乾血）、`#event-text`（本文パネル）、`.tomb`（墓碑・
`writing-mode:vertical-rl`、`.cause`乾血／`.rare`金）、`.grave-entry`（年代記の一行）。

## タイポグラフィ
- 和文 `"Shippori Mincho","Hiragino Mincho ProN","Yu Mincho","Noto Serif JP",serif`、
  本文 16px / line-height 1.85。
- 数字・判定値は本文より1〜2段大きく、`--bone` で。
- `writing-mode:vertical-rl`（縦書き）は **タイトルと墓碑だけ**の専用表現。多用しない。

## シグネチャ（4つ。ゲームの魂。必ず活かす）
1. **出目2の紋章** `<Emblem>` — 両方1の目を出した骰子二つ。タイトル・アプリアイコン・
   ローディングの核。
2. **蝋燭の灯り** `<CandleVignette>` — 全画面の微揺ビネット。運命時は赤変。
3. **朱印スタンプ** `<JudgeStamp>` — 判定結果（大成功=金／成功=骨／失敗=褪色／大失敗=乾血）が
   捺される瞬間。
4. **縦書きの墓碑** `<Tombstone>` — 死のたびに生成される年代記。天寿（金）と横死（乾血）の
   差を劇的に。

## やらないこと（厳守）
- クリーム×テラコッタ／黒×蛍光緑／新聞風ヘアラインの「AI定番3種」への回帰。
- 角丸の大きいモダンUI・グラスモーフィズム・ネオン発光。
- 絵文字・洋風ファンタジーの金ピカ装飾・ゴシックホラーの滴る血。
- バナー広告前提の余白設計（広告はリワードのみ・UI外）。
- 過剰アニメーション。動きは **「燭光の揺れ・骰子・朱印」の3箇所のみ**。

## 真実の在り処
- スタイル: `styles.css` とその `@import`（`tokens/tokens.css`）。
- 各部品: `components/<group>/<Name>/` の `.html`（見た目）・`.jsx`（実装）・
  `.prompt.md`（使い方）・`.d.ts`（props）。**要素を組む前にこれらを読む。**

## 最小の作例（この流儀で1画面）
```jsx
<div id="app">
  <CandleVignette />
  <div className="screen active" style={{ justifyContent: "center", gap: 13 }}>
    <Emblem width={104} />
    <div className="game-title">無法の国に生まれて</div>
    <div className="game-sub center">畳の上で死ねた者は、まだいない。</div>
    <hr className="rule" />
    <button>生まれる<span className="meta">生まれは選べない</span></button>
  </div>
</div>
```
色は必ず `var(--*)`、レイアウトの糊も上のクラス語彙で。新しい色名・角丸・発光は足さない。
