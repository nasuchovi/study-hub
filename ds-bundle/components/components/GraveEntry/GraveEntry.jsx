// 年代記の一行 — 過去帳に積まれる歴代の死。番号(no)＋一文。原典 .grave-entry を移植。
// 死因は <span style={{color:"var(--blood)"}}>、大往生・伝説は <span style={{color:"var(--gold)"}}>。
export function GraveEntry({ no, children, className, style }) {
  return (
    <div
      className={className}
      style={{
        background: "var(--paper)",
        border: "1px solid var(--line)",
        borderRadius: 2,
        padding: "11px 13px",
        fontSize: 13.5,
        lineHeight: 1.9,
        color: "var(--ink)",
        ...style,
      }}
    >
      {no != null && (
        <span style={{ color: "var(--dim)", fontSize: 11, letterSpacing: ".15em" }}>{no}</span>
      )}
      {no != null && <br />}
      {children}
    </div>
  );
}

export default GraveEntry;
