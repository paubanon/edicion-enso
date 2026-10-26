import { AbsoluteFill } from "remotion";
import { BigTitle } from "../../../lib/BigTitle";
import { Captions } from "../../../lib/Captions";
import type { Span } from "../../../lib/edit";
import { Finish } from "../../../lib/Finish";
import { Footage, type Grade } from "../../../lib/Footage";
import { colors } from "../../../lib/theme";
import { edit } from "./edit";

// Layer stack, bottom to top: graded footage -> titles behind the person -> person
// cut-out -> cards and graphics -> captions -> grain and vignette.
// Cue frames come from edit/cut_transcript.md.

const GRADE: Grade = { contrast: 1.08, saturation: 1.05, vibrance: 0.1 };

const HOOK: Span = { from: 0, durationInFrames: 60 };

export const Reel: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: colors.black }}>
      <Footage
        edit={edit}
        grade={GRADE}
        behind={[
          {
            name: "Hook title",
            ...HOOK,
            content: (
              <BigTitle
                durationInFrames={HOOK.durationInFrames}
                top={260}
                lines={[
                  { text: "Título", size: 210 },
                  { text: "con contraste", size: 140, style: "contrast" },
                ]}
              />
            ),
          },
        ]}
      />
      <Captions captions={edit.captions} hiddenDuring={[HOOK]} />
      <Finish />
    </AbsoluteFill>
  );
};
