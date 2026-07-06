import type { CSSProperties, ReactNode } from "react";

export type ChipVariant = "default" | "on" | "mate" | "tag";

export interface ChipProps {
  children?: ReactNode;
  /** default=状態(褪せ) / on=有効な才・業(金) / mate=連れ・縁者(緑) / tag=恒久タグ。 */
  variant?: ChipVariant;
  className?: string;
  style?: CSSProperties;
}

export function Chip(props: ChipProps): JSX.Element;
export default Chip;
