// 墓碑 — 死のたびに生成される縦書きの記録。年代記＝プレイヤーの神話の一葉。
// 版面は原典 無法の国に生まれて_v0.8.html .tomb を忠実移植。
// 本文中で死因は className="cause"(乾血)、稀な伝説は className="rare"(金) で色分けする。
export function Tombstone({ children, maxHeight = "min(420px,62vh)", className, style }) {
  return (
    <div
      className={className}
      style={{
        writingMode: "vertical-rl",
        background: "var(--paper)",
        border: "1px solid var(--line)",
        padding: "24px 20px",
        minHeight: 290,
        maxHeight,
        maxWidth: "100%",
        overflow: "auto",
        font: '15.5px/2.3 "Shippori Mincho","Hiragino Mincho ProN","Yu Mincho","Noto Serif JP",serif',
        letterSpacing: ".12em",
        color: "var(--bone)",
        ...style,
      }}
    >
      {children}
    </div>
  );
}

// 本文断片ヘルパー: <Cause>…</Cause> / <Rare>…</Rare>
export const Cause = ({ children }) => <span style={{ color: "var(--blood)" }}>{children}</span>;
export const Rare = ({ children }) => <span style={{ color: "var(--gold)" }}>{children}</span>;

export default Tombstone;
