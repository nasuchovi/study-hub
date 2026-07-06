// 本文パネル — 場所・語り手・出来事の本文。原典 #event-loc / #speaker-name / #event-text を移植。
// 古紙地に内影(inset shadow)で「くぼみに刻んだ」質感を出すのが要。
export function EventPanel({ loc, speaker, children, className, style }) {
  return (
    <div className={className} style={style}>
      {speaker && (
        <div style={{ fontSize: 12, color: "var(--dim)", letterSpacing: ".15em", padding: "1px 2px 0", minHeight: 20 }}>▸ {speaker}</div>
      )}
      {loc && (
        <div style={{ fontSize: 12, color: "var(--dim)", letterSpacing: ".2em", marginBottom: 4 }}>{loc}</div>
      )}
      <div
        style={{
          background: "var(--paper)",
          border: "1px solid var(--line)",
          borderRadius: 2,
          padding: "14px 15px",
          minHeight: 88,
          fontSize: 15,
          lineHeight: 1.85,
          color: "var(--ink)",
          boxShadow: "inset 0 0 0 1px rgba(0,0,0,.4), inset 0 1px 0 rgba(236,226,203,.03)",
        }}
      >
        {children}
      </div>
    </div>
  );
}

export default EventPanel;
