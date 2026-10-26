import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { cardShadow, colors, easings, fonts, markerBackground, springs } from "./theme";

// The standard label: an off-white card with a mono meta line, a Satoshi title and an
// optional ✓ / ✕ badge. It springs in at `at`, breathes while idle and leaves at `exitAt`.

type CardProps = {
  meta: string;
  title: React.ReactNode;
  badge?: "yes" | "no";
  // Frames, relative to the enclosing Sequence.
  at?: number;
  exitAt?: number;
  top: number;
  left: number;
  rotate?: number;
  style?: React.CSSProperties;
};

const EXIT_FRAMES = 6;

export const Card: React.FC<CardProps> = ({ meta, title, badge, at = 0, exitAt, top, left, rotate = 0, style }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const enter = spring({ frame: frame - at, fps, config: springs.snappy });
  const exit =
    exitAt === undefined
      ? 0
      : interpolate(frame, [exitAt - EXIT_FRAMES, exitAt], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
          easing: easings.exit,
        });
  if (frame < at) {
    return null;
  }
  const drift = Math.sin(((frame - at) / fps) * 1.6) * 3;

  return (
    <div
      style={{
        position: "absolute",
        top,
        left,
        background: colors.card,
        color: colors.black,
        borderRadius: 26,
        padding: "28px 34px",
        boxShadow: cardShadow,
        opacity: enter * (1 - exit),
        translate: `0 ${(1 - enter) * 50 + drift - exit * 20}px`,
        scale: String(0.92 + enter * 0.08),
        rotate: `${rotate + (1 - enter) * -4}deg`,
        ...style,
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 22 }}>
        {badge ? (
          <div
            style={{
              flex: "none",
              width: 64,
              height: 64,
              borderRadius: "50%",
              display: "grid",
              placeItems: "center",
              background: badge === "yes" ? colors.sage : colors.earth,
              color: colors.white,
              fontFamily: fonts.display,
              fontWeight: 700,
              fontSize: 38,
            }}
          >
            {badge === "yes" ? "✓" : "✕"}
          </div>
        ) : null}
        <div>
          <div style={{ fontFamily: fonts.data, fontSize: 26, color: colors.earth }}>{meta}</div>
          <div
            style={{
              fontFamily: fonts.display,
              fontWeight: 700,
              textTransform: "uppercase",
              fontSize: 50,
              lineHeight: 1,
              marginTop: 10,
              whiteSpace: "nowrap",
            }}
          >
            {title}
          </div>
        </div>
      </div>
    </div>
  );
};

// A sage highlighter stroke painted left to right under a word, starting at `at`.
export const Marker: React.FC<{ at: number; children: React.ReactNode }> = ({ at, children }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const paint = spring({ frame: frame - at, fps, config: springs.smooth, durationInFrames: Math.round(0.35 * fps) });

  return (
    <span
      style={{
        backgroundImage: markerBackground(colors.sage),
        backgroundRepeat: "no-repeat",
        backgroundSize: `${paint * 100}% 100%`,
      }}
    >
      {children}
    </span>
  );
};
