// 状態・連れ・タグを示す小片。原典 .chip / .on / .mate / .tag を忠実移植。
const VARIANT = {
  default: { color: "var(--dim)", border: "var(--line)" },
  on: { color: "var(--gold)", border: "#5a4a2a" },      // 有効な才・業
  mate: { color: "#9db0a0", border: "#3a4a3e" },        // 連れ・縁者
  tag: { color: "#a89a80", border: "#463c2e" },         // 恒久タグ
};

export function Chip({ children, variant = "default", className, style }) {
  const v = VARIANT[variant] || VARIANT.default;
  return (
    <span
      className={className}
      style={{
        display: "inline-block",
        fontSize: 11,
        letterSpacing: ".08em",
        border: "1px solid " + v.border,
        color: v.color,
        padding: "0 7px",
        borderRadius: 2,
        lineHeight: 1.9,
        ...style,
      }}
    >
      {children}
    </span>
  );
}

export default Chip;
