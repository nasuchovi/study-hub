import type { CSSProperties, ReactNode } from "react";

export interface StatusBarProps {
  /** 年齢表示（例 "二十九歳"）。骨色で最も目立つ。 */
  age?: ReactNode;
  /** 所持金（例 "38G"）。金色。 */
  money?: ReactNode;
  /** 負傷の数（点灯する乾血の点の数）。既定 0。 */
  injury?: number;
  /** 負傷の上限（点の総数）。既定 4。 */
  injuryMax?: number;
  /** 業の値。 */
  karma?: ReactNode;
  className?: string;
  style?: CSSProperties;
}

export function StatusBar(props: StatusBarProps): JSX.Element;
export default StatusBar;
