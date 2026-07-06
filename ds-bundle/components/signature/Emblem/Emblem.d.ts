import type { CSSProperties } from "react";

export interface EmblemProps {
  /** 表示幅(px)。既定 104。タイトルは104前後、アプリアイコンは512。 */
  width?: number;
  /** 目(ピップ)の色。既定 #1d150e。 */
  pipColor?: string;
  /** 骰子面の色。既定 #ece2cb（骨）。 */
  faceColor?: string;
  className?: string;
  style?: CSSProperties;
}

export function Emblem(props: EmblemProps): JSX.Element;
export default Emblem;
