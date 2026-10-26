import { Audio } from "@remotion/media";
import { Sequence, staticFile, useVideoConfig } from "remotion";

// Sound effects from marca/sfx (see its LEEME.md). Each entry knows its attack, so a
// sound placed `at` a frame lands its hit on that frame rather than after it.

const SFX = {
  pop: { file: "dragon-studio-pop-402324 (1).mp3", attack: 0.19, volume: 0.3 },
  whoosh: { file: "dragon-studio-simple-whoosh-382724.mp3", attack: 0.07, volume: 0.25 },
  riser: { file: "dragon-studio-riser-swoosh-transition-390289.mp3", attack: 0.17, volume: 0.3 },
  page: { file: "dragon-studio-flipping-book-page-499646.mp3", attack: 0.02, volume: 0.4 },
  typing: { file: "dragon-studio-typing-with-keyboard-435489.mp3", attack: 0.04, volume: 0.5 },
  shutter: { file: "freesound_community-camera-shutter-6305.mp3", attack: 0.04, volume: 0.35 },
  writing: { file: "freesound_community-writingpensignaturepaper-102967.mp3", attack: 0.38, volume: 1 },
  underline: { file: "nikin-scratch-sound-effect-for-video-title-underline-317747.mp3", attack: 0.05, volume: 0.25 },
} as const;

export type SfxName = keyof typeof SFX;

type SfxProps = {
  name: SfxName;
  at: number;
  // Cut the sound after this many frames past its hit (long typing or writing loops).
  holdFrames?: number;
  volume?: number;
};

export const Sfx: React.FC<SfxProps> = ({ name, at, holdFrames, volume }) => {
  const { fps } = useVideoConfig();
  const sfx = SFX[name];
  const lead = Math.round(sfx.attack * fps);
  const start = at - lead;

  return (
    <Sequence
      name={`SFX ${name}`}
      from={Math.max(0, start)}
      durationInFrames={holdFrames === undefined ? undefined : lead + holdFrames}
      layout="none"
    >
      <Audio
        src={staticFile(`marca/sfx/${sfx.file}`)}
        trimBefore={start < 0 ? -start : undefined}
        volume={volume ?? sfx.volume}
      />
    </Sequence>
  );
};
