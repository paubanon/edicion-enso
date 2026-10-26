import { colorCorrection, type ColorCorrectionParams } from "@remotion/effects/color-correction";
import { Video } from "@remotion/media";
import {
  AbsoluteFill,
  interpolate,
  Sequence,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { isWithin, type Edit, type Span } from "./edit";
import { springs } from "./theme";

export type Grade = ColorCorrectionParams;
export type PunchIn = Span & { zoom?: number };
// A fixed crop in place of the shot's alternating zoom, e.g. to keep a tripod or a light
// out of frame. It does not animate, so it reads as the shot's own framing.
export type Reframe = Span & { zoom: number; origin: string };
// Content shown between the footage and the cut-out person, so it reads as behind them.
export type BehindLayer = Span & { name: string; content: React.ReactNode };

const SHOT_ZOOMS = [1, 1.1];
const DEFAULT_PUNCH_ZOOM = 1.18;

type FramingProps = {
  edit: Edit;
  punchIns: PunchIn[];
  reframes: Reframe[];
  focus: string;
  // Frame at which the enclosing Sequence starts, so zooms follow the reel's clock.
  offset: number;
  children: React.ReactNode;
};

// Alternating zoom per shot hides jump cuts; punch-ins stress key lines.
const Framing: React.FC<FramingProps> = ({ edit, punchIns, reframes, focus, offset, children }) => {
  const frame = useCurrentFrame() + offset;
  const { fps } = useVideoConfig();

  const shotIndex = edit.shots.filter((shot) => shot.from <= frame).length - 1;
  const reframe = reframes.find((r) => isWithin(r, frame));
  const shotZoom = reframe?.zoom ?? SHOT_ZOOMS[shotIndex % SHOT_ZOOMS.length];
  const punch = punchIns.find((p) => isWithin(p, frame));
  const punchZoom = punch
    ? interpolate(
        spring({ frame: frame - punch.from, fps, config: springs.smooth }),
        [0, 1],
        [1, punch.zoom ?? DEFAULT_PUNCH_ZOOM],
      )
    : 1;

  return (
    <AbsoluteFill style={{ scale: shotZoom * punchZoom, transformOrigin: reframe?.origin ?? focus }}>
      {children}
    </AbsoluteFill>
  );
};

type FootageProps = {
  edit: Edit;
  grade?: Grade;
  punchIns?: PunchIn[];
  reframes?: Reframe[];
  behind?: BehindLayer[];
  // Zoom origin, ideally the speaker's face.
  focus?: string;
};

// The talking-head track: graded footage, then any "behind" layers, each covered by
// the person cut-out (public/cutout.webm from cutout.py) for exactly its span.
export const Footage: React.FC<FootageProps> = ({
  edit,
  grade = {},
  punchIns = [],
  reframes = [],
  behind = [],
  focus = "50% 35%",
}) => {
  const effects = [colorCorrection(grade)];
  const fill = { width: "100%", height: "100%" } as const;

  return (
    <AbsoluteFill>
      <Framing edit={edit} punchIns={punchIns} reframes={reframes} focus={focus} offset={0}>
        <Video name="Footage" src={staticFile("main_cut.mp4")} effects={effects} style={fill} />
      </Framing>

      {behind.map((layer) => (
        <Sequence key={layer.from} name={layer.name} from={layer.from} durationInFrames={layer.durationInFrames}>
          {layer.content}
          <Framing edit={edit} punchIns={punchIns} reframes={reframes} focus={focus} offset={layer.from}>
            <Video
              name="Person cut-out"
              src={staticFile("cutout.webm")}
              trimBefore={layer.from}
              muted
              effects={effects}
              style={fill}
            />
          </Framing>
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
