import { useId } from "react";
import { Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { colors, easings, springs } from "./theme";

// An object cut out of the B-roll (scripts/object_cutout.swift) brought into the
// speaker's shot as a sticker: white outline, soft shadow, a springy pop at `at` from
// its base, leaving at `exitAt`.

type StickerProps = {
  // Transparent PNG inside the reel's public folder.
  src: string;
  // Frames, relative to the enclosing Sequence.
  at?: number;
  exitAt?: number;
  top: number;
  left: number;
  height: number;
  rotate?: number;
};

const OUTLINE = 9;
const EXIT_FRAMES = 6;

export const Sticker: React.FC<StickerProps> = ({ src, at = 0, exitAt, top, left, height, rotate = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const filterId = `sticker${useId().replace(/[^a-zA-Z0-9]/g, "")}`;
  if (frame < at) {
    return null;
  }
  const pop = spring({ frame: frame - at, fps, config: springs.hero });
  const exit =
    exitAt === undefined
      ? 0
      : interpolate(frame, [exitAt - EXIT_FRAMES, exitAt], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
          easing: easings.exit,
        });

  return (
    <>
      <svg width={0} height={0} style={{ position: "absolute" }}>
        <filter id={filterId}>
          <feMorphology in="SourceAlpha" operator="dilate" radius={OUTLINE} result="outline" />
          <feFlood floodColor={colors.white} />
          <feComposite in2="outline" operator="in" />
          <feMerge>
            <feMergeNode />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </svg>
      <Img
        src={staticFile(src)}
        style={{
          position: "absolute",
          top,
          left,
          height,
          rotate: `${rotate}deg`,
          scale: String(pop * (1 - exit * 0.2)),
          opacity: 1 - exit,
          transformOrigin: "50% 100%",
          filter: `url(#${filterId}) drop-shadow(0 18px 26px rgba(10, 10, 10, 0.35))`,
        }}
      />
    </>
  );
};
