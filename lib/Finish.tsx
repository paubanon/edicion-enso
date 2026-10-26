import { AbsoluteFill, useCurrentFrame } from "remotion";

// Top of the layer stack: film grain and a vignette tie footage and graphics into
// one image. The grain seed follows the frame, so renders are deterministic.

type FinishProps = {
  grain?: number;
  vignette?: number;
};

export const Finish: React.FC<FinishProps> = ({ grain = 0.07, vignette = 0.35 }) => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <AbsoluteFill
        style={{ background: `radial-gradient(ellipse at 50% 42%, transparent 55%, rgba(0,0,0,${vignette}) 100%)` }}
      />
      <svg width="100%" height="100%" style={{ position: "absolute", opacity: grain, mixBlendMode: "overlay" }}>
        <filter id="grain">
          <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves={2} seed={frame % 1000} stitchTiles="stitch" />
          <feColorMatrix type="saturate" values="0" />
        </filter>
        <rect width="100%" height="100%" filter="url(#grain)" />
      </svg>
    </AbsoluteFill>
  );
};
