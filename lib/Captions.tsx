import type { Caption } from "@remotion/captions";
import { useMemo } from "react";
import { AbsoluteFill, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { isWithin, type Span } from "./edit";
import { colors, fonts, springs, textShadow } from "./theme";

// The quiet tier of text: it follows the voice so the reel reads muted, and steps
// aside (hiddenDuring) whenever a big title or card carries the moment.

const MAX_WORDS = 3;
const MAX_CHARS = 18;
const MAX_GAP_MS = 300;
// A page stays up until the next one, unless the speaker pauses longer than this.
const MAX_LINGER_MS = 400;
const SENTENCE_BREAK = /[.,?!…]$/;

type Page = { startMs: number; endMs: number; tokens: Caption[] };

const paginate = (captions: Caption[]): Page[] => {
  const pages: Page[] = [];
  let current: Caption[] = [];
  const flush = () => {
    if (current.length > 0) {
      pages.push({ startMs: current[0].startMs, endMs: current[current.length - 1].endMs, tokens: current });
    }
    current = [];
  };

  for (const caption of captions) {
    const previous = current[current.length - 1];
    const chars = current.map((c) => c.text).join("").length + caption.text.length;
    if (
      previous &&
      (current.length >= MAX_WORDS ||
        chars > MAX_CHARS ||
        caption.startMs - previous.endMs > MAX_GAP_MS ||
        SENTENCE_BREAK.test(previous.text))
    ) {
      flush();
    }
    current.push(caption);
  }
  flush();

  return pages.map((page, i) => {
    const next = pages[i + 1];
    const lingerEnd = page.endMs + MAX_LINGER_MS;
    return { ...page, endMs: next ? Math.min(next.startMs, lingerEnd) : lingerEnd };
  });
};

type PageProps = { page: Page; timeMs: number; fontSize: number };

const CaptionPage: React.FC<PageProps> = ({ page, timeMs, fontSize }) => {
  const { fps } = useVideoConfig();
  const activeIndex = page.tokens.filter((t) => t.startMs <= timeMs).length - 1;

  return (
    <div
      style={{
        maxWidth: 900,
        textAlign: "center",
        fontFamily: fonts.text,
        fontWeight: 700,
        fontSize,
        lineHeight: 1.15,
        color: colors.white,
        textShadow,
      }}
    >
      {page.tokens.map((token, i) => {
        const appear = spring({ frame: ((timeMs - token.startMs) / 1000) * fps, fps, config: springs.snappy });
        const isActive = i === activeIndex;
        return (
          <span
            key={token.startMs}
            style={{
              display: "inline-block",
              whiteSpace: "pre",
              color: isActive ? colors.sage : colors.white,
              opacity: i <= activeIndex ? 1 : 0.35,
              translate: `0 ${(1 - appear) * 12}px`,
            }}
          >
            {token.text}
          </span>
        );
      })}
    </div>
  );
};

type CaptionsProps = {
  captions: Caption[];
  hiddenDuring?: Span[];
  // Vertical position of the line, in composition pixels.
  top?: number;
  // Spans with their own position, e.g. above the head in a close-up whose chest is busy.
  topDuring?: (Span & { top: number })[];
  fontSize?: number;
};

export const Captions: React.FC<CaptionsProps> = ({
  captions,
  hiddenDuring = [],
  top = 1260,
  topDuring = [],
  fontSize = 60,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const timeMs = (frame / fps) * 1000;

  const pages = useMemo(() => paginate(captions), [captions]);
  const page = pages.find((p) => p.startMs <= timeMs && timeMs < p.endMs);
  if (!page || hiddenDuring.some((span) => isWithin(span, frame))) {
    return null;
  }

  return (
    <AbsoluteFill style={{ alignItems: "center", top: topDuring.find((span) => isWithin(span, frame))?.top ?? top }}>
      <CaptionPage page={page} timeMs={timeMs} fontSize={fontSize} />
    </AbsoluteFill>
  );
};
