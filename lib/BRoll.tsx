import { colorCorrection } from "@remotion/effects/color-correction";
import { Video } from "@remotion/media";
import { AbsoluteFill, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import type { Grade } from "./Footage";

// A full-frame cutaway over the voice: muted, graded like the footage, with a slow push-in
// so a held shot never sits frozen.

type BRollProps = {
  // Path inside the reel's public folder.
  src: string;
  // Seconds into the clip to start from.
  startAt?: number;
  grade?: Grade;
  style?: React.CSSProperties;
};

const PUSH_PER_SECOND = 0.02;

export const BRoll: React.FC<BRollProps> = ({ src, startAt = 0, grade = {}, style }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const push = 1 + interpolate(frame / fps, [0, 10], [0, PUSH_PER_SECOND * 10]);

  return (
    <AbsoluteFill style={{ overflow: "hidden", ...style }}>
      <Video
        src={staticFile(src)}
        trimBefore={Math.round(startAt * fps)}
        muted
        effects={[colorCorrection(grade)]}
        style={{ width: "100%", height: "100%", objectFit: "cover", scale: String(push) }}
      />
    </AbsoluteFill>
  );
};
