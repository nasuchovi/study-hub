// 選択肢・行動ボタン。古紙地・角丸2px・左揃え・任意の副文(meta)。
// 原典 無法の国に生まれて_v0.8.html の button / .meta を忠実移植。
export function Button({ children, meta, disabled, onClick, className, style, ...rest }) {
  return (
    <button
      type="button"
      disabled={disabled}
      onClick={onClick}
      className={className}
      style={{
        fontFamily: "inherit",
        color: "var(--ink)",
        background: "var(--paper)",
        border: "1px solid var(--line)",
        borderRadius: 2,
        padding: "12px 14px",
        fontSize: 15,
        lineHeight: 1.6,
        textAlign: "left",
        width: "100%",
        cursor: disabled ? "default" : "pointer",
        boxShadow: "inset 0 0 0 1px rgba(0,0,0,.38)",
        opacity: disabled ? 0.35 : 1,
        ...style,
      }}
      {...rest}
    >
      {children}
      {meta ? (
        <span style={{ display: "block", fontSize: 11.5, color: "var(--dim)", marginTop: 2, letterSpacing: ".03em" }}>{meta}</span>
      ) : null}
    </button>
  );
}

export default Button;
