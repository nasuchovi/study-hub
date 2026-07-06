<!-- 無法の国に生まれて — Claude Design 単一添付ブリーフ
     スマホからはこの1枚＋現行ビルド(無法の国に生まれて_v0.8.html)を添付して発注する。
     出典: ds-bundle/ (conventions + 全部品の prompt/d.ts を集約) -->

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

---

# 部品リファレンス（API と使い方）

> 各部品はゲーム本体の実マークアップ/SVG/CSSの忠実な移植。`.jsx`は外部依存の無い自己完結コンポーネント。

---

# Tokens（トークン）

デザインの変更不可の土台。**色は必ず `var(--*)` を使い、生の16進を新規に書かない。**
実体は `tokens/tokens.css`（`styles.css` が `@import`）。

## 配色（ブリーフ§2の確定7色＋支持色）
| 変数 | HEX | 名 | 用途 |
|---|---|---|---|
| `--soot` | #14100c | 煤 | 背景 |
| `--paper` | #221b13 | 古紙 | カード・ボタン地 |
| `--ink` | #d9cfba | 生成り | 本文 |
| `--bone` | #ece2cb | 骨 | 見出し・数値・骰子 |
| `--blood` | #a63d2e | 乾血 | 死・大失敗・運命 |
| `--gold` | #bd9448 | 燻金 | 金銭・業・天寿・伝説 |
| `--candle` | #e0aa60 | 燭光 | 環境光 |
| `--dim` | #8a7f6c | 褪せ | 補助文字・ラベル |
| `--paper2` | #2b231a | — | 押下時の地 |
| `--line` | #3a3126 | 罫 | 枠線 |
| `--sil` | #0c0906 | 影 | シルエット |

## タイポグラフィ
- `--font-serif` = しっぽり明朝（Shippori Mincho, 400/500/700）+ 明朝フォールバック。
- 本文 16px / 行間 1.85。数字・判定値は本文より1〜2段大きく `--bone`。
- 縦書き(`writing-mode:vertical-rl`)は**タイトルと墓碑のみ**。

## 形
- 角丸は `--radius`(2px) を基本に小さく保つ。大きな角丸・グラスモーフィズム・発光は禁止。
- 基準幅 `--app-max`(480px) の縦画面。

---

### 型定義: Emblem.d.ts
```ts
import type { CSSProperties } from "react";

export interface EmblemProps {
  /** 表示幅(px)。既定 104。タイトルは104前後、アプリアイコンは512。 */
  width?: number;
  /** 目(ピップ)の色。既定 #1d150e。 */
  pipColor?: string;
  /** 骰子面の色。既定 #ece2cb（骨）。 */
  faceColor?: string;
  className?: string;
  style?: CSSProperties;
}

export function Emblem(props: EmblemProps): JSX.Element;
export default Emblem;
```

# Emblem（出目2の紋章）

ゲームの核となる紋章。**両方が「1の目」を出した骰子が二つ**、互いに逆へ傾いて並ぶ。
2D6で最悪の出目「2（大失敗）」を意匠化したもの＝「無法の国に生まれた」宿命の象徴。

## 使いどころ
- タイトル画面の主役（縦書きタイトルの上）。
- アプリアイコン（512px。小さくても2つの骰子と各1つの目が読めるよう、周囲に十分な余白を）。
- ローディング／スプラッシュ。

## 使い方
```jsx
<Emblem width={104} />                         // タイトル
<Emblem width={512} />                          // アプリアイコン
<Emblem width={64} faceColor="#bd9448" />       // 燻金の刻印バリエーション（伝説・箔押し表現）
```

## 約束
- 骰子面は既定で `--bone`(#ece2cb)、目は暗色。背景は必ず `--soot` 系の暗がりに置く
  （紋章が浮くように）。ドロップシャドウは既に内蔵。
- 傾き（-9° / +8°）と2つの目だけ、という最小構成を崩さない。3つ目の骰子や装飾を足さない。
- 金ピカ装飾・発光・絵文字は禁止（指針§やらないこと）。箔押し表現をするなら `faceColor` を
  `--gold` にするに留める。

---

### 型定義: DieFace.d.ts
```ts
import type { CSSProperties } from "react";

export interface DieFaceProps {
  /** 出目 1〜6。既定 1。 */
  n?: 1 | 2 | 3 | 4 | 5 | 6;
  /** 一辺(px)。既定 62。目の大きさは自動追従。 */
  size?: number;
  /** 質感。"bone"=骨彫り(既定) / "obsidian"=黒曜。 */
  variant?: "bone" | "obsidian";
  /** 振動アニメーション。prefers-reduced-motion では自動で止める配慮を忘れずに。 */
  rolling?: boolean;
  className?: string;
  style?: CSSProperties;
}

export function DieFace(props: DieFaceProps): JSX.Element;
export default DieFace;
```

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

---

### 型定義: JudgeStamp.d.ts
```ts
import type { CSSProperties } from "react";

export type JudgeTier = "crit" | "succ" | "fail" | "fumb";

export interface JudgeStampProps {
  /** 判定段階。crit=大成功(金) / succ=成功(骨) / fail=失敗(褪色) / fumb=大失敗(乾血)。既定 succ。 */
  tier?: JudgeTier;
  /** 表示文字の上書き。既定は tier に対応する語（大成功/成功/失敗/大失敗）。 */
  label?: string;
  /** 捺される登場アニメ。prefers-reduced-motion では false に。既定 true。 */
  animate?: boolean;
  className?: string;
  style?: CSSProperties;
}

export function JudgeStamp(props: JudgeStampProps): JSX.Element;
export default JudgeStamp;
```

# JudgeStamp（朱印スタンプ）

2D6判定の結果が、記録簿に捺される瞬間の意匠。骰子が確定した直後、暗転画面の中央上に
大きく回転して現れる。感情の句読点。

## 段階と色（変更不可）
| tier | 語 | 色 | 意味 |
|---|---|---|---|
| `crit` | 大成功 | `--gold` 燻金 | raw=12 または total ≥ 目標+5 |
| `succ` | 成功 | `--bone` 骨 | total ≥ 目標 |
| `fail` | 失敗 | 褪せた乾血 #9a5a44 | 目標未満 |
| `fumb` | 大失敗 | `--blood` 乾血 | raw=2（両1・紋章の目） |

## 使い方
```jsx
<JudgeStamp tier="crit" />                 {/* 大成功（金の朱印） */}
<JudgeStamp tier="fumb" />                 {/* 大失敗（乾血。運命の目） */}
<JudgeStamp tier="succ" label="天寿" />    {/* 死亡画面で語を差し替える応用 */}
```

## 約束
- 枠と文字は同色（縁取りの朱印）。塗り足し・影付きの立体ボタン化をしない。
- わずかに傾ける（-5°）。まっすぐ置くと「捺した」実感が消える。
- 登場アニメ `stampIn` は許可された「朱印」枠の動き。`prefers-reduced-motion` では
  `animate={false}`。
- 絵文字・チェックマーク・星は使わない。語（漢字）そのものが意匠。

---

### 型定義: Scene.d.ts
```ts
import type { CSSProperties } from "react";

export type SceneLocation =
  | "street" | "market" | "dock" | "alley"
  | "temple" | "guild" | "mine" | "field";

export type SceneSky = "morning" | "noon" | "night";

export type SceneFigure = "burly" | "robe" | "merchant" | "cloak" | "down";

export interface SceneProps {
  /** ロケーション。既定 "street"。未知の値は street にフォールバック。 */
  loc?: SceneLocation;
  /** 時刻＝空のグラデ。"night" のみ月が出る。既定 "noon"。 */
  sky?: SceneSky;
  /** 語り手の人影(任意)。"down" は倒れた人（右下）。省略で無し。 */
  figure?: SceneFigure;
  className?: string;
  style?: CSSProperties;
}

export function Scene(props: SceneProps): JSX.Element;
export const SCENE_LOCATIONS: SceneLocation[];
export const SCENE_FIGURES: SceneFigure[];
export default Scene;
```

# Scene（場面）

イベント本文の上に置く、横長(480×130)の小さな影絵。**空のグラデ＋シルエットのロケーション＋
任意の人影**で情景を立ち上げる。写実ではなく、蝋燭で照らされた記憶の輪郭。

## 部品
- **空 `sky`**: `morning`（褐色の暁）/ `noon`（鈍い昼）/ `night`（藍。月が出る）。
- **ロケーション `loc`**: `street` `market` `dock` `alley` `temple` `guild` `mine` `field`。
  全て `--sil`(#0c0906) のシルエット＋窓明かり(#c19a4b の淡い矩形)。
- **人影 `figure`**: `burly`（屈強）/ `robe`（修道）/ `merchant`（商人）/ `cloak`（外套）/
  `down`（倒れた人）。右手(x=400)に立つ。`down` だけ低い位置。

## 使い方
```jsx
<Scene loc="alley" sky="night" figure="cloak" />   {/* 夜の路地に外套の男 */}
<Scene loc="temple" sky="morning" figure="robe" />
<Scene loc="mine" sky="noon" />                     {/* 人影なし＝荒涼 */}
```

## 約束
- 色は `--sil` の影と、窓明かりの弱い金(#c19a4b, opacity 0.2前後)だけ。原色・グラデ発光を足さない。
- 空は3種の既定グラデを使う。虹色や派手な夕焼けにしない（トーンは乾いた・荘厳）。
- 運命イベントでは枠が赤くなる（`#app.fate #scene`）。Scene 自体は変えず、親に `.fate`。
- 人物に顔・表情を描かない。輪郭だけで語る。

---

### 型定義: Tombstone.d.ts
```ts
import type { CSSProperties, ReactNode } from "react";

export interface TombstoneProps {
  /** 碑文本文。死因は <Cause>、稀な伝説は <Rare> で包んで色分けする。 */
  children?: ReactNode;
  /** 最大高。既定 "min(420px,62vh)"。 */
  maxHeight?: string | number;
  className?: string;
  style?: CSSProperties;
}

export function Tombstone(props: TombstoneProps): JSX.Element;
/** 死因(乾血)の色付き断片。 */
export function Cause(props: { children?: ReactNode }): JSX.Element;
/** 伝説(燻金)の色付き断片。 */
export function Rare(props: { children?: ReactNode }): JSX.Element;
export default Tombstone;
```

# Tombstone（墓碑）

死のたびに生成される**縦書きの碑**。死亡画面の感情のピークであり、年代記に積まれていく
一葉。プレイヤーが遺すのは点数ではなく、この文章。

## 版面（守る）
- `writing-mode: vertical-rl`（右→左の縦書き）。縦書きは**タイトルと墓碑だけ**の専用表現。
- 地は `--paper`、枠 `--line`、文字 `--bone`、行間ゆったり(2.3)・字間 .12em。
- **天寿（金）と横死（乾血）の差を劇的に**：安らかな最期は金(`Rare`)を、無惨な死因は
  乾血(`Cause`)を本文に差す。

## 使い方
```jsx
<Tombstone>
  百姓の与作、畳の上で老いて逝く。享年六十一。
  <Rare>――畳の上で死ねた、稀な一人として刻まれる。</Rare>
</Tombstone>

<Tombstone>
  賭場の勝吉、路地裏に転がる。享年二十四。
  <Cause>いかさまの濡れ衣。弁明は拳と棒の雨に掻き消えた。</Cause>
</Tombstone>
```

## 課金コスメのバリエーション方針（発注§5）
碑そのものの意匠替え：`粗石`（既定・素）/ `聖堂式`（枠に細い罫の入れ子）/ `王家の廟`
（金の細縁＋見出しに `--gold`）。地色・縦書き・字間は共通のまま、縁と装飾だけで格を変える。

## 約束
- 死を事実として記す。感傷的な飾り・絵文字・滴る血のイラストは禁止。
- 文字色は骨・乾血・金の3色に限る。読み下しの縦組みを崩さない。

---

### 型定義: CandleVignette.d.ts
```ts
export interface CandleVignetteProps {
  /** 運命モード。灯りが赤へ転じ、揺れが速く不穏になる。既定 false。 */
  fate?: boolean;
  /** 古紙グレインを重ねるか。既定 true。 */
  grain?: boolean;
}

export function CandleVignette(props: CandleVignetteProps): JSX.Element;
export default CandleVignette;
```

# CandleVignette（蝋燭の灯り）

画面全体を包む**環境光**。中央上がわずかに明るく、四隅が沈む楕円ビネットが、ゆっくり
揺れる（蝋燭）。上に薄い古紙グレインを重ねる。プレイヤーが「暗い部屋で一本の蝋燭を頼りに
記録簿を読んでいる」感覚を、全画面で常時支える最重要の質感。

## 置き方
`position: relative` の親（＝`#app`）の**直下に一度だけ**置く。`pointer-events:none` なので
操作を邪魔しない。z-index はグレイン24・灯り25で、UIより手前。

```jsx
<div id="app" style={{ position:"relative", overflow:"hidden" }}>
  <CandleVignette />
  {/* …画面… */}
</div>
```

## 運命モード
不吉な転調では `fate` を立てる。灯りが赤み（乾血）へ寄り、揺れが 4.2s → 1.6s に速まって
息苦しくなる。親要素に `.fate` を付ける設計と対でも良い。

```jsx
<CandleVignette fate />
```

## 約束
- 揺れ(`flicker`)は許可された3つの動きの1つ。`prefers-reduced-motion` では停止（内蔵済み）。
- ビネットは常に**中央上が明るい**。均一な暗幕や、下から光る配置にしない。
- 発光の強い光源・レンズフレア・パーティクルを足さない。あくまで一本の蝋燭。

---

### 型定義: Button.d.ts
```ts
import type { ButtonHTMLAttributes, CSSProperties, ReactNode } from "react";

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  /** ボタン主文。 */
  children?: ReactNode;
  /** 副文（判定条件・注記など）。小さく褪せた色で下段に出る。 */
  meta?: ReactNode;
  disabled?: boolean;
  className?: string;
  style?: CSSProperties;
}

export function Button(props: ButtonProps): JSX.Element;
export default Button;
```

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

---

### 型定義: Chip.d.ts
```ts
import type { CSSProperties, ReactNode } from "react";

export type ChipVariant = "default" | "on" | "mate" | "tag";

export interface ChipProps {
  children?: ReactNode;
  /** default=状態(褪せ) / on=有効な才・業(金) / mate=連れ・縁者(緑) / tag=恒久タグ。 */
  variant?: ChipVariant;
  className?: string;
  style?: CSSProperties;
}

export function Chip(props: ChipProps): JSX.Element;
export default Chip;
```

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

---

### 型定義: StatusBar.d.ts
```ts
import type { CSSProperties, ReactNode } from "react";

export interface StatusBarProps {
  /** 年齢表示（例 "二十九歳"）。骨色で最も目立つ。 */
  age?: ReactNode;
  /** 所持金（例 "38G"）。金色。 */
  money?: ReactNode;
  /** 負傷の数（点灯する乾血の点の数）。既定 0。 */
  injury?: number;
  /** 負傷の上限（点の総数）。既定 4。 */
  injuryMax?: number;
  /** 業の値。 */
  karma?: ReactNode;
  className?: string;
  style?: CSSProperties;
}

export function StatusBar(props: StatusBarProps): JSX.Element;
export default StatusBar;
```

# StatusBar（ステータスバー）

画面最上部の帯。一つの生の残量を一行で示す。**齢＝骨（最重要）**、銭＝金、傷＝乾血の点、
業＝褪せ色。下辺に細い罫(`--line`)。

## 使い方
```jsx
<StatusBar age="二十九歳" money="38G" injury={2} injuryMax={4} karma={4} />
```

## 約束
- 色の意味を固定：齢は `--bone`、銭は `--gold`、負傷の点灯は `--blood`、消灯は #4a4034。
- 数字（齢）は本文より一段大きく。アイコンや絵文字（💰❤️等）を使わず、語と点で示す。
- 情報が増えても一行・両端揃え・折り返しで収める。バー全体を塗らない（罫だけ）。

---

# EventPanel（本文パネル）

出来事の描写を刻む中核パネル。上に語り手（`▸ 名`）と場所、その下に古紙のくぼみへ沈めた
本文。`Scene` の直下、選択肢(`Button`群)の上に置く。

## 使い方
```jsx
<Scene loc="temple" sky="night" figure="robe" />
<EventPanel speaker="老修道士" loc="聖堂・夜">
  施しの粥を巡る諍いが、また始まっていた。老いた修道士は何も言わず、
  ただ床の血を拭くための桶を、こちらへ滑らせた。
</EventPanel>
```

## 約束
- 本文は `--ink`(生成り)、語り手・場所は `--dim`。明朝・行間1.85でゆったり読ませる。
- 内影(`inset` シャドウ)で「刻まれた」質感を保つ。外に浮く影・立体カードにしない。
- 運命イベントでは親 `.fate` により地が暗赤・文字が褪せ赤へ自動転調。パネル側で色を上書きしない。

---

# GraveEntry（年代記の一行）

年代記（墓碑一覧）画面で縦に積む、歴代の死の一行。番号(`no`＝「其の一」等)と、一文の記録。
巻物・過去帳の趣。`Tombstone` が一つの死の碑なら、これはその名簿。

## 使い方
```jsx
<div id="graves-list" style={{ display:"flex", flexDirection:"column", gap:9 }}>
  <GraveEntry no="其の一">
    百姓の与作、畑の傍らで老いて逝く。
    <span style={{ color:"var(--gold)" }}>畳ならぬ土の上、稀な大往生。</span>
  </GraveEntry>
  <GraveEntry no="其の二">
    賭場の勝吉、路地裏に転がる。
    <span style={{ color:"var(--blood)" }}>いかさまの疑いに、拳の雨。</span>
  </GraveEntry>
</div>
```

## 約束
- 死因は乾血(`--blood`)、大往生・伝説は金(`--gold`)。本文は生成り。3色以外を足さない。
- 一行は簡潔に。カードを大きくせず、名簿として淡々と積む（見出し「年代記　―　誰も助からなかった」）。
- 横書き（縦書きは墓碑とタイトルのみ）。
