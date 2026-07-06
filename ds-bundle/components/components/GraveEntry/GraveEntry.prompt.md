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
