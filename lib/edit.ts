import type { Caption } from "@remotion/captions";

// Shape of <reel>/src/edit.json, written by the reel-editor skill's cut.py.
// Every frame value is on the output timeline.
export type Span = { from: number; durationInFrames: number };

export type Shot = { from: number; take: string };

export type Edit = {
  fps: number;
  width: number;
  height: number;
  durationInFrames: number;
  shots: Shot[];
  captions: Caption[];
};

export const isWithin = (span: Span, frame: number) =>
  frame >= span.from && frame < span.from + span.durationInFrames;
