import { evolvePath } from "@remotion/paths";
import { useId } from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { colors, easings } from "./theme";

// Hand-drawn brush lines over the frame, as if drawn on an iPad: white, roughened
// edges, soft shadow. Each path draws on in turn, starting at `at`.

type BrushStrokeProps = {
  // SVG path data in composition pixels, drawn in order.
  paths: string[];
  at?: number;
  // Frames to draw each path.
  drawFrames?: number;
  exitAt?: number;
  width?: number;
};

const EXIT_FRAMES = 6;

export const BrushStroke: React.FC<BrushStrokeProps> = ({ paths, at = 0, drawFrames = 12, exitAt, width = 16 }) => {
  const frame = useCurrentFrame();
  const filterId = `brush${useId().replace(/[^a-zA-Z0-9]/g, "")}`;
  const fade =
    exitAt === undefined
      ? 1
      : interpolate(frame, [exitAt - EXIT_FRAMES, exitAt], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ opacity: fade, filter: "drop-shadow(0 4px 10px rgba(10, 10, 10, 0.5))" }}>
      <svg width="100%" height="100%" viewBox="0 0 1080 1920" style={{ overflow: "visible" }}>
        <filter id={filterId}>
          <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves={2} seed={4} />
          <feDisplacementMap in="SourceGraphic" scale={9} />
        </filter>
        {paths.map((d, i) => {
          const start = at + i * drawFrames;
          const progress = interpolate(frame, [start, start + drawFrames], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: easings.enter,
          });
          return (
            <path
              key={d}
              d={d}
              fill="none"
              stroke={colors.white}
              strokeWidth={width}
              strokeLinecap="round"
              strokeLinejoin="round"
              filter={`url(#${filterId})`}
              {...evolvePath(progress, d)}
            />
          );
        })}
      </svg>
    </AbsoluteFill>
  );
};
