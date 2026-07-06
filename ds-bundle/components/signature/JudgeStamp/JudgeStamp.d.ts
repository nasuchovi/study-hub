import type { CSSProperties } from "react";

export type JudgeTier = "crit" | "succ" | "fail" | "fumb";

export interface JudgeStampProps {
  /** 判定段階。crit=大成功(金) / succ=成功(骨) / fail=失敗(褪色) / fumb=大失敗(乾血)。既定 succ。 */
  tier?: JudgeTier;
  /** 表示文字の上書き。既定は tier に対応する語（大成功/成功/失敗/大失敗）。 */
  label?: string;
  /** 捺される登場アニメ。prefers-reduced-motion では false に。既定 true。 */
  animate?: boolean;
  className?: string;
  style?: CSSProperties;
}

export function JudgeStamp(props: JudgeStampProps): JSX.Element;
export default JudgeStamp;
