import type { CSSProperties } from "react";

export type SceneLocation =
  | "street" | "market" | "dock" | "alley"
  | "temple" | "guild" | "mine" | "field";

export type SceneSky = "morning" | "noon" | "night";

export type SceneFigure = "burly" | "robe" | "merchant" | "cloak" | "down";

export interface SceneProps {
  /** ロケーション。既定 "street"。未知の値は street にフォールバック。 */
  loc?: SceneLocation;
  /** 時刻＝空のグラデ。"night" のみ月が出る。既定 "noon"。 */
  sky?: SceneSky;
  /** 語り手の人影(任意)。"down" は倒れた人（右下）。省略で無し。 */
  figure?: SceneFigure;
  className?: string;
  style?: CSSProperties;
}

export function Scene(props: SceneProps): JSX.Element;
export const SCENE_LOCATIONS: SceneLocation[];
export const SCENE_FIGURES: SceneFigure[];
export default Scene;
