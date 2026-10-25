import { Composition } from "remotion";
import { PlayHQIntro } from "./PlayHQIntro";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="PlayHQIntro"
      component={PlayHQIntro}
      durationInFrames={150}
      fps={30}
      width={1080}
      height={1920}
      defaultProps={{
        title: "PLAYHQ",
        handle: "@playhqtv",
        tagline: "Die besten Gaming-Clips",
        accent: "#00f0ff",
        accent2: "#ff2bd6",
      }}
    />
  );
};
