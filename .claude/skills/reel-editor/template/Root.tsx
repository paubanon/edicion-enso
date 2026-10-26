import { Composition } from "remotion";
import { edit } from "./edit";
import { Reel } from "./Reel";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="Reel"
      component={Reel}
      durationInFrames={edit.durationInFrames}
      fps={edit.fps}
      width={edit.width}
      height={edit.height}
    />
  );
};
