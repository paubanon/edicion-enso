import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { colors, easings, fonts, springs, textShadow } from "./theme";

// The loud tier of text: one concept, set big, usually placed behind the speaker
// through Footage's `behind` layers.

// display: Satoshi Bold uppercase, the title itself.
// contrast: Fira Sans Light Italic in sage, the word that turns the sentence.
// data: JetBrains Mono in sage, for anything measurable.
type LineStyle = "display" | "contrast" | "data";

export type TitleLine = {
  text: string;
  size: number;
  style?: LineStyle;
  // Overrides the style's colour, e.g. white for a contrast line over a bright wall.
  color?: string;
};

const LINE_STYLES: Record<LineStyle, React.CSSProperties> = {
  display: { fontFamily: fonts.display, fontWeight: 700, textTransform: "uppercase", letterSpacing: "-0.01em" },
  contrast: { fontFamily: fonts.text, fontWeight: 300, fontStyle: "italic", letterSpacing: "-0.02em" },
  data: { fontFamily: fonts.data, fontWeight: 400, letterSpacing: "-0.02em" },
};

type BigTitleProps = {
  lines: TitleLine[];
  // Length of the enclosing Sequence; the exit plays at its end.
  durationInFrames: number;
  top: number;
  // Seconds between consecutive words entering.
  stagger?: number;
};

const ENTER_SECONDS = 0.5;
const EXIT_SECONDS = 0.25;
const BREATH_SCALE = 0.008;

export const BigTitle: React.FC<BigTitleProps> = ({ lines, durationInFrames, top, stagger = 0.06 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const exitFrames = Math.round(EXIT_SECONDS * fps);
  const exit = interpolate(frame, [durationInFrames - exitFrames, durationInFrames], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: easings.exit,
  });
  const breath = 1 + Math.sin((frame / fps) * Math.PI * 0.8) * BREATH_SCALE;

  let wordIndex = 0;
  return (
    <AbsoluteFill style={{ top, alignItems: "center", scale: breath }}>
      {lines.map((line) => (
        <div
          key={line.text}
          style={{
            ...LINE_STYLES[line.style ?? "display"],
            fontSize: line.size,
            lineHeight: 0.95,
            color: line.color ?? ((line.style ?? "display") === "display" ? colors.white : colors.sage),
            textShadow,
            whiteSpace: "nowrap",
          }}
        >
          {line.text.split(" ").map((word) => {
            const enter = spring({
              frame: frame - Math.round(wordIndex++ * stagger * fps),
              fps,
              config: springs.snappy,
              durationInFrames: Math.round(ENTER_SECONDS * fps),
            });
            const shown = enter * (1 - exit);
            return (
              <span
                key={`${word}-${wordIndex}`}
                style={{
                  display: "inline-block",
                  marginInline: "0.12em",
                  opacity: shown,
                  translate: `0 ${(1 - enter) * 60 - exit * 30}px`,
                  filter: `blur(${(1 - shown) * 14}px)`,
                }}
              >
                {word}
              </span>
            );
          })}
        </div>
      ))}
    </AbsoluteFill>
  );
};
