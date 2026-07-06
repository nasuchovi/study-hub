// 蝋燭の灯り — 全画面の微揺ビネット＋古紙グレイン。ゲームの環境光。
// position:relative の親(#app)直下に置く。運命モードは fate で赤変。
// 原典 無法の国に生まれて_v0.8.html #grain / #candle を忠実移植。
const GRAIN_BG =
  "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='2'/%3E%3C/filter%3E%3Crect width='140' height='140' filter='url(%23n)' opacity='0.9'/%3E%3C/svg%3E\")";

export function CandleVignette({ fate = false, grain = true }) {
  const candleBg = fate
    ? "radial-gradient(ellipse 90% 62% at 50% 30%, rgba(190,58,40,.13), rgba(8,0,0,.5) 90%)"
    : "radial-gradient(ellipse 90% 62% at 50% 28%, rgba(224,170,96,.09), rgba(0,0,0,.34) 90%)";
  return (
    <>
      {grain && (
        <div
          aria-hidden="true"
          style={{ position: "absolute", inset: 0, zIndex: 24, pointerEvents: "none", opacity: 0.05, backgroundImage: GRAIN_BG }}
        />
      )}
      <div
        aria-hidden="true"
        style={{
          position: "absolute",
          inset: 0,
          zIndex: 25,
          pointerEvents: "none",
          background: candleBg,
          animation: (fate ? "flicker 1.6s" : "flicker 4.2s") + " ease-in-out infinite",
        }}
      />
      <style>{"@keyframes flicker{0%,100%{opacity:1}47%{opacity:.86}52%{opacity:.95}70%{opacity:.88}}@media (prefers-reduced-motion: reduce){[style*='flicker']{animation:none!important}}"}</style>
    </>
  );
}

export default CandleVignette;
