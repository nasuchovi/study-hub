<!-- このREADMEの先頭ヘッダーは .design-sync/conventions.md 由来（readmeHeader）。以降の部品索引は生成物。 -->

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
  `.screen`、表示中は `.screen.active`。環境光は `<CandleVignette />` を `#app` 直下に置く。
- 運命（不吉な転調）モードは `#app` に `.fate` を付けるだけで、枠・本文・選択肢・骰子が
  赤基調へ切り替わる（`styles.css` にルールあり）。

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
- 和文 `"Shippori Mincho","Hiragino Mincho ProN","Yu Mincho","Noto Serif JP",serif`、本文16px/1.85。
- 数字・判定値は本文より1〜2段大きく `--bone` で。
- `writing-mode:vertical-rl` は **タイトルと墓碑だけ**の専用表現。多用しない。

## シグネチャ（4つ。ゲームの魂。必ず活かす）
1. **出目2の紋章** `<Emblem>` — 両方1の目を出した骰子二つ。
2. **蝋燭の灯り** `<CandleVignette>` — 全画面の微揺ビネット。運命時は赤変。
3. **朱印スタンプ** `<JudgeStamp>` — 大成功=金／成功=骨／失敗=褪色／大失敗=乾血。
4. **縦書きの墓碑** `<Tombstone>` — 天寿(金)と横死(乾血)の差を劇的に。

## やらないこと（厳守）
- クリーム×テラコッタ／黒×蛍光緑／新聞風ヘアラインの「AI定番3種」への回帰。
- 角丸の大きいモダンUI・グラスモーフィズム・ネオン発光。
- 絵文字・洋風ファンタジーの金ピカ装飾・ゴシックホラーの滴る血。
- バナー広告前提の余白設計（広告はリワードのみ・UI外）。
- 過剰アニメーション。動きは **「燭光の揺れ・骰子・朱印」の3箇所のみ**。

---

## 部品一覧

### Foundations
| 部品 | 概要 | パス |
|---|---|---|
| Tokens | 確定7色＋支持色・しっぽり明朝・角丸2px | `components/foundations/Tokens/` |

### Signature（シグネチャ）
| 部品 | 概要 | パス |
|---|---|---|
| Emblem | 出目2の紋章（両1の骰子二つ）。タイトル・アプリアイコン | `components/signature/Emblem/` |
| DieFace | 骰子1面。骨彫り／黒曜の2質感、目1〜6 | `components/signature/DieFace/` |
| JudgeStamp | 朱印（大成功/成功/失敗/大失敗） | `components/signature/JudgeStamp/` |
| Scene | 場面の影絵。空×9ロケーション×人影 | `components/signature/Scene/` |
| Tombstone | 縦書きの墓碑。死因(乾血)／伝説(金) | `components/signature/Tombstone/` |
| CandleVignette | 蝋燭の環境光＋古紙グレイン。運命で赤変 | `components/signature/CandleVignette/` |

### Components（部品）
| 部品 | 概要 | パス |
|---|---|---|
| Button | 選択肢・行動。古紙地・左揃え・副文 | `components/components/Button/` |
| Chip | 状態・連れ・タグの小片 | `components/components/Chip/` |
| StatusBar | 齢(骨)・銭(金)・傷(乾血)・業 | `components/components/StatusBar/` |
| EventPanel | 場所・語り手・本文パネル | `components/components/EventPanel/` |
| GraveEntry | 年代記の一行（過去帳） | `components/components/GraveEntry/` |

## この配布物について
- `styles.css` … 全デザインが受け取る正典スタイル（`@import` で `tokens/` とフォントを含む）。
- `tokens/` … `tokens.css`（CSS変数）と `tokens.json`（構造化）。
- `components/<group>/<Name>/` … `.html`(見た目) / `.jsx`(実装) / `.d.ts`(props) / `.prompt.md`(使い方)。
- 各コンポーネントはゲーム本体 `無法の国に生まれて_v0.8.html` の実マークアップ／SVG／CSSの
  忠実な移植。`.jsx` は外部依存の無い自己完結コンポーネント。
