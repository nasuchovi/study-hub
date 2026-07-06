// 出目2の紋章 — 両方1の目を出した骰子二つ。ゲームのシグネチャ。
// 原典 無法の国に生まれて_v0.8.html #emblem の SVG をバイト単位で忠実移植。
export function Emblem({ width = 104, pipColor = "#1d150e", faceColor = "#ece2cb", className, style }) {
  return (
    <span
      className={className}
      style={{
        display: "inline-flex",
        justifyContent: "center",
        filter: "drop-shadow(0 3px 6px rgba(0,0,0,.55))",
        ...style,
      }}
    >
      <svg viewBox="0 0 120 62" width={width} xmlns="http://www.w3.org/2000/svg" role="img" aria-label="出目2の紋章">
        <g transform="rotate(-9 35 31)">
          <rect x="14" y="10" width="42" height="42" rx="7" fill={faceColor} />
          <circle cx="35" cy="31" r="4.6" fill={pipColor} />
        </g>
        <g transform="rotate(8 85 31)">
          <rect x="64" y="12" width="42" height="42" rx="7" fill={faceColor} />
          <circle cx="85" cy="33" r="4.6" fill={pipColor} />
        </g>
      </svg>
    </span>
  );
}

export default Emblem;
