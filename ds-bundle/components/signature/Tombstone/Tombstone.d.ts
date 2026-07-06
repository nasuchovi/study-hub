import type { CSSProperties, ReactNode } from "react";

export interface TombstoneProps {
  /** 碑文本文。死因は <Cause>、稀な伝説は <Rare> で包んで色分けする。 */
  children?: ReactNode;
  /** 最大高。既定 "min(420px,62vh)"。 */
  maxHeight?: string | number;
  className?: string;
  style?: CSSProperties;
}

export function Tombstone(props: TombstoneProps): JSX.Element;
/** 死因(乾血)の色付き断片。 */
export function Cause(props: { children?: ReactNode }): JSX.Element;
/** 伝説(燻金)の色付き断片。 */
export function Rare(props: { children?: ReactNode }): JSX.Element;
export default Tombstone;
