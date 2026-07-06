export interface CandleVignetteProps {
  /** 運命モード。灯りが赤へ転じ、揺れが速く不穏になる。既定 false。 */
  fate?: boolean;
  /** 古紙グレインを重ねるか。既定 true。 */
  grain?: boolean;
}

export function CandleVignette(props: CandleVignetteProps): JSX.Element;
export default CandleVignette;
