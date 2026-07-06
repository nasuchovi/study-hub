// ステータスバー — 齢・銭・傷・業を一行に。原典 #statusbar を忠実移植。
// 齢は骨(--bone)、銭は金(--gold)、傷は乾血の点、で色の意味を固定。
export function StatusBar({ age, money, injury = 0, injuryMax = 4, karma, className, style }) {
  const dots = [];
  for (let i = 0; i < injuryMax; i++) {
    dots.push(
      <i key={i} style={{ fontStyle: "normal", color: i < injury ? "var(--blood)" : "#4a4034" }}>●</i>
    );
  }
  return (
    <div
      className={className}
      style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "baseline",
        borderBottom: "1px solid var(--line)",
        padding: "0 2px 7px",
        fontSize: 13,
        color: "var(--dim)",
        letterSpacing: ".03em",
        flexWrap: "wrap",
        gap: "2px 8px",
        ...style,
      }}
    >
      {age != null && <span style={{ color: "var(--bone)", fontSize: 14.5 }}>{age}</span>}
      {money != null && <span style={{ color: "var(--gold)" }}>{money}</span>}
      <span>傷 {dots}</span>
      {karma != null && <span>業 {karma}</span>}
    </div>
  );
}

export default StatusBar;
