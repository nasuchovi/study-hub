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
