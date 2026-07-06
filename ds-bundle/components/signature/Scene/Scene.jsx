// 場面 — テキストの背後に置く小さな影絵。空(時刻)×ロケーション×人影で情景を作る。
// SKY / SCENES / FIGURES / 組み立ては原典 無法の国に生まれて_v0.8.html を忠実移植。
const SKY = {
  morning: ["#6b4a2f", "#2a1c12", false],
  noon: ["#7a6a4a", "#3a2f1f", false],
  night: ["#141821", "#05060a", true],
};

const SCENES = {
  street: '<path fill="var(--sil)" d="M0,70 40,70 40,50 55,38 70,50 70,72 110,72 110,44 130,32 150,44 150,74 200,74 200,56 214,46 228,56 228,76 480,76 480,130 0,130Z"/><rect x="86" y="58" width="7" height="9" fill="#c19a4b" opacity=".28"/><rect x="136" y="50" width="7" height="9" fill="#c19a4b" opacity=".2"/><path fill="var(--sil)" d="M300,76 310,40 316,40 326,76Z"/><rect x="309" y="34" width="8" height="8" fill="#c19a4b" opacity=".35"/>',
  market: '<path fill="var(--sil)" d="M0,80 480,80 480,130 0,130Z"/><path fill="var(--sil)" d="M30,80 30,52 100,52 100,80Z"/><path fill="#241a10" d="M24,52 106,52 98,38 32,38Z"/><path fill="var(--sil)" d="M150,80 150,56 230,56 230,80Z"/><path fill="#241a10" d="M144,56 236,56 228,42 152,42Z"/><path fill="var(--sil)" d="M290,80 290,50 380,50 380,80Z"/><path fill="#241a10" d="M284,50 386,50 378,34 292,34Z"/><rect x="52" y="62" width="10" height="10" fill="#c19a4b" opacity=".22"/><rect x="318" y="58" width="10" height="10" fill="#c19a4b" opacity=".22"/>',
  dock: '<rect y="84" width="480" height="46" fill="#0a0e10"/><path fill="#1c2426" d="M0,84 480,84 480,90 0,90Z" opacity=".6"/><path fill="var(--sil)" d="M0,84 0,60 90,60 90,84Z"/><rect x="120" y="66" width="22" height="18" fill="var(--sil)"/><rect x="146" y="72" width="16" height="12" fill="var(--sil)"/><path fill="var(--sil)" d="M220,84 220,30 226,30 226,60 300,72 300,78 226,66 226,84Z"/><path fill="var(--sil)" d="M360,96 470,96 460,84 370,84Z"/><path fill="var(--sil)" d="M410,84 410,58 414,58 414,84Z"/>',
  alley: '<path fill="var(--sil)" d="M0,0 150,0 150,26 120,40 120,130 0,130Z"/><path fill="var(--sil)" d="M480,0 330,0 330,30 360,44 360,130 480,130Z"/><path fill="#241a10" d="M120,40 360,44 360,52 120,48Z" opacity=".7"/><rect x="132" y="70" width="8" height="10" fill="#c19a4b" opacity=".18"/><path fill="var(--sil)" d="M120,130 120,96 200,104 200,130Z" opacity=".9"/>',
  temple: '<path fill="var(--sil)" d="M60,80 60,58 240,58 240,80Z"/><path fill="var(--sil)" d="M40,58 260,58 236,34 64,34Z"/><path fill="var(--sil)" d="M140,34 160,34 158,22 142,22Z"/><rect x="90" y="64" width="8" height="16" fill="#c19a4b" opacity=".22"/><path fill="var(--sil)" d="M330,80 330,48 338,40 346,48 346,80Z"/><path fill="var(--sil)" d="M0,80 480,80 480,130 0,130Z"/><path fill="var(--sil)" d="M390,80 390,60 460,60 460,80Z" opacity=".8"/>',
  guild: '<path fill="var(--sil)" d="M0,86 480,86 480,130 0,130Z"/><path fill="var(--sil)" d="M90,86 90,40 300,40 300,86Z"/><path fill="#241a10" d="M80,40 310,40 300,24 90,24Z"/><rect x="120" y="56" width="14" height="14" fill="#c19a4b" opacity=".3"/><rect x="250" y="56" width="14" height="14" fill="#c19a4b" opacity=".3"/><rect x="176" y="58" width="34" height="28" fill="#241a10"/><rect x="150" y="10" width="4" height="30" fill="var(--sil)"/><path fill="#3a3126" d="M154,12 200,16 200,28 154,24Z"/>',
  mine: '<path fill="var(--sil)" d="M0,130 0,74 90,44 200,84 320,38 480,86 480,130Z"/><path fill="#060403" d="M210,130 210,90 236,74 262,90 262,130Z"/><rect x="204" y="86" width="8" height="44" fill="var(--sil)"/><rect x="260" y="86" width="8" height="44" fill="var(--sil)"/><rect x="200" y="80" width="72" height="8" fill="var(--sil)"/><path fill="var(--sil)" d="M300,130 300,112 340,112 340,130Z" opacity=".8"/>',
  field: '<path fill="var(--sil)" d="M0,88 480,88 480,130 0,130Z"/><path fill="var(--sil)" d="M40,88 40,70 46,70 46,88Z M120,88 120,70 126,70 126,88Z M200,88 200,70 206,70 206,88Z"/><path fill="#241a10" d="M38,72 128,72 128,76 38,76Z M118,72 208,72 208,76 118,76Z" opacity=".8"/><path fill="var(--sil)" d="M300,88 C300,64 360,64 360,88Z"/><path fill="var(--sil)" d="M400,88 400,54 440,42 470,58 470,88Z"/>',
};

const FIGURES = {
  burly: '<path fill="var(--sil)" d="M0,0 C-9,0 -13,7 -13,14 L-13,20 C-20,23 -24,32 -24,44 L-24,86 -14,86 -13,52 -10,52 -10,86 10,86 10,52 13,52 14,86 24,86 24,44 C24,32 20,23 13,20 L13,14 C13,7 9,0 0,0Z"/>',
  robe: '<path fill="var(--sil)" d="M0,0 C-7,0 -10,6 -10,12 L-10,17 C-18,22 -21,34 -22,48 L-24,86 24,86 22,48 C21,34 18,22 10,17 L10,12 C10,6 7,0 0,0Z"/>',
  merchant: '<path fill="var(--sil)" d="M-16,6 16,6 12,0 -12,0Z M0,7 C-6,7 -9,12 -9,17 L-9,21 C-16,25 -19,34 -19,46 L-19,86 -8,86 -8,54 8,54 8,86 19,86 19,46 C19,34 16,25 9,21 L9,17 C9,12 6,7 0,7Z"/>',
  cloak: '<path fill="var(--sil)" d="M0,2 C-8,2 -12,9 -12,15 L-12,18 C-19,24 -22,36 -22,52 L-22,86 22,86 22,52 C22,36 19,24 12,18 L12,15 C12,9 8,2 0,2Z M-12,15 C-14,8 -8,-2 0,-2 8,-2 14,8 12,15 8,10 -8,10 -12,15Z"/>',
  down: '<path fill="var(--sil)" d="M-40,16 C-40,10 -34,8 -28,9 L20,14 C30,15 38,18 38,24 L38,26 -40,26Z M-46,10 a7,7 0 1,1 0,14 a7,7 0 1,1 0,-14Z"/>',
};

function skyDefs(t) {
  const [c1, c2, moon] = SKY[t] || SKY.noon;
  return (
    '<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="' +
    c1 + '"/><stop offset="1" stop-color="' + c2 + '"/></linearGradient></defs>' +
    '<rect width="480" height="130" fill="url(#sky)"/>' +
    (moon
      ? '<circle cx="392" cy="30" r="13" fill="#cfc7ae" opacity=".85"/><circle cx="386" cy="26" r="11" fill="' + c1 + '" opacity=".55"/>'
      : "")
  );
}

export function Scene({ loc = "street", sky = "noon", figure, className, style }) {
  const fig = figure && FIGURES[figure]
    ? '<g transform="translate(400,' + (figure === "down" ? 96 : 40) + ')">' + FIGURES[figure] + "</g>"
    : "";
  const inner = skyDefs(sky) + (SCENES[loc] || SCENES.street) + fig;
  return (
    <div
      className={className}
      style={{ width: "100%", border: "1px solid var(--line)", borderRadius: 2, overflow: "hidden", background: "#000", ...style }}
    >
      <svg viewBox="0 0 480 130" xmlns="http://www.w3.org/2000/svg" style={{ display: "block", width: "100%", height: "auto" }} dangerouslySetInnerHTML={{ __html: inner }} />
    </div>
  );
}

export const SCENE_LOCATIONS = Object.keys(SCENES);
export const SCENE_FIGURES = Object.keys(FIGURES);
export default Scene;
