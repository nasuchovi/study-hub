// 骰子（1つの面）— 2D6判定の主役。骨彫り(bone)と黒曜(obsidian)の2質感。
// 目の配置・寸法は原典 無法の国に生まれて_v0.8.html の PIP_POS / .die / .pip を忠実移植。
const PIP_POS = {
  1: [[50, 50]],
  2: [[28, 28], [72, 72]],
  3: [[25, 25], [50, 50], [75, 75]],
  4: [[28, 28], [72, 28], [28, 72], [72, 72]],
  5: [[26, 26], [74, 26], [50, 50], [26, 74], [74, 74]],
  6: [[28, 24], [72, 24], [28, 50], [72, 50], [28, 76], [72, 76]],
};

export function DieFace({ n = 1, size = 62, variant = "bone", rolling = false, className, style }) {
  const face =
    variant === "obsidian"
      ? "radial-gradient(circle at 32% 26%,#3a3630,#1c1814 70%,#0c0a08)"
      : "radial-gradient(circle at 32% 26%,#f6eeda,#e0d4b6 68%,#c9ba98)";
  const pipColor = variant === "obsidian" ? "#d9cfba" : "#231c14";
  const pip = Math.round(size * 0.177);
  return (
    <div
      className={className}
      style={{
        width: size,
        height: size,
        background: face,
        borderRadius: 8,
        position: "relative",
        boxShadow: "0 4px 14px rgba(0,0,0,.6)",
        animation: rolling ? "tumble .12s infinite" : undefined,
        ...style,
      }}
      role="img"
      aria-label={"骰子 " + n}
    >
      {(PIP_POS[n] || PIP_POS[1]).map(([x, y], i) => (
        <span
          key={i}
          style={{
            position: "absolute",
            width: pip,
            height: pip,
            borderRadius: "50%",
            background: pipColor,
            left: "calc(" + x + "% - " + pip / 2 + "px)",
            top: "calc(" + y + "% - " + pip / 2 + "px)",
          }}
        />
      ))}
    </div>
  );
}

export default DieFace;
