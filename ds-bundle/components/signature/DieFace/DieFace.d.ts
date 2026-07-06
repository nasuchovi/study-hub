import type { CSSProperties } from "react";

export interface DieFaceProps {
  /** 出目 1〜6。既定 1。 */
  n?: 1 | 2 | 3 | 4 | 5 | 6;
  /** 一辺(px)。既定 62。目の大きさは自動追従。 */
  size?: number;
  /** 質感。"bone"=骨彫り(既定) / "obsidian"=黒曜。 */
  variant?: "bone" | "obsidian";
  /** 振動アニメーション。prefers-reduced-motion では自動で止める配慮を忘れずに。 */
  rolling?: boolean;
  className?: string;
  style?: CSSProperties;
}

export function DieFace(props: DieFaceProps): JSX.Element;
export default DieFace;
