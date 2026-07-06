import type { ButtonHTMLAttributes, CSSProperties, ReactNode } from "react";

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  /** ボタン主文。 */
  children?: ReactNode;
  /** 副文（判定条件・注記など）。小さく褪せた色で下段に出る。 */
  meta?: ReactNode;
  disabled?: boolean;
  className?: string;
  style?: CSSProperties;
}

export function Button(props: ButtonProps): JSX.Element;
export default Button;
