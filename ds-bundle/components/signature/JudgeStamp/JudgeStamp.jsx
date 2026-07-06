// 朱印スタンプ — 判定結果が捺される瞬間の意匠。
// 色・寸法・傾きは原典 無法の国に生まれて_v0.8.html #stamp を忠実移植。
// 判定境界(原典 rollFor): raw=2→大失敗 / raw=12 または total>=tn+5→大成功 / total>=tn→成功 / 他→失敗。
const TIERS = {
  crit: { label: "大成功", color: "#bd9448" }, // 燻金
  succ: { label: "成功",   color: "#ece2cb" }, // 骨
  fail: { label: "失敗",   color: "#9a5a44" }, // 褪せた乾血
  fumb: { label: "大失敗", color: "#a63d2e" }, // 乾血
};

export function JudgeStamp({ tier = "succ", label, animate = true, className, style }) {
  const t = TIERS[tier] || TIERS.succ;
  return (
    <span
      className={className}
      style={{
        display: "inline-block",
        font: '700 38px/1 "Shippori Mincho",serif',
        letterSpacing: ".2em",
        padding: "9px 24px",
        border: "3px solid " + t.color,
        color: t.color,
        borderRadius: 4,
        transform: "rotate(-5deg)",
        textShadow: "0 0 7px rgba(0,0,0,.4)",
        filter: "drop-shadow(0 0 1px rgba(0,0,0,.5))",
        animation: animate ? "stampIn .25s ease-out" : undefined,
        ...style,
      }}
      role="img"
      aria-label={"判定 " + (label || t.label)}
    >
      {label || t.label}
    </span>
  );
}

export default JudgeStamp;
