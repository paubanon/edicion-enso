import { loadFont } from "@remotion/fonts";
import { Easing, staticFile } from "remotion";

// One source of truth for the look: no inline colours, fonts or easings elsewhere.
// Brand rules live in .claude/skills/reel-editor/marca/MARCA.md; the font files are
// served from each reel's public/marca link to that folder.

const brandFont = (family: string, file: string, weight: string, style = "normal") =>
  loadFont({ family, url: staticFile(`marca/fuentes/${file}`), weight, style });

brandFont("Satoshi", "Satoshi-Variable.ttf", "300 900");
brandFont("Satoshi", "Satoshi-VariableItalic.ttf", "300 900", "italic");
brandFont("Fira Sans", "FiraSans-Light.ttf", "300");
brandFont("Fira Sans", "FiraSans-LightItalic.ttf", "300", "italic");
brandFont("Fira Sans", "FiraSans-Bold.ttf", "700");
brandFont("JetBrains Mono", "JetBrainsMono-Variable.ttf", "100 800");

export const fonts = {
  // Titles (Bold 700, uppercase), labels and spoken captions.
  display: "Satoshi",
  // Reading text; Light Italic is the contrast word inside a title.
  text: "Fira Sans",
  // Anything measurable: angles, reps, times.
  data: "JetBrains Mono",
};

// Luminous Enso Pure.
export const colors = {
  black: "#0A0A0A",
  white: "#FFFFFF",
  mist: "#E5E8E4",
  sage: "#A2B598",
  sageLight: "#D4DECE",
  earth: "#8C7565",
  // Cards: brighter than mist, which reads grey against very bright footage.
  card: "#F8F9F7",
};

// Text over footage is white with a wide shadow, sage for the key word, even on light
// walls: the user found black text unattractive. Text on cards is black, key word on a
// sage marker.
export const textShadow = "0 3px 10px rgba(10, 10, 10, 0.45), 0 10px 60px rgba(10, 10, 10, 0.4)";
export const cardShadow = "0 24px 60px rgba(10, 10, 10, 0.28), 0 4px 12px rgba(10, 10, 10, 0.12)";

// Highlighter stroke behind the lower part of a word.
export const markerBackground = (color: string) => `linear-gradient(transparent 58%, ${color} 58%, ${color} 92%, transparent 92%)`;

// Composition-space margins Instagram's UI leaves clear (1080x1920).
export const safeZone = { top: 220, bottom: 420, left: 60, right: 140 };

export const springs = {
  // UI-like pop for words and cards; no visible bounce.
  snappy: { damping: 200, stiffness: 300, mass: 0.6 },
  // Larger elements and camera moves.
  smooth: { damping: 200, stiffness: 120, mass: 1 },
  // A small, intentional overshoot for the one hero moment per beat.
  hero: { damping: 14, stiffness: 160, mass: 0.8 },
} as const;

export const easings = {
  enter: Easing.bezier(0.16, 1, 0.3, 1),
  exit: Easing.bezier(0.7, 0, 0.84, 0),
  camera: Easing.bezier(0.65, 0, 0.35, 1),
} as const;
