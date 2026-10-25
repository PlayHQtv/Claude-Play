import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

export type PlayHQIntroProps = {
  title: string;
  handle: string;
  tagline: string;
  accent: string;
  accent2: string;
};


const GRID_HEIGHT = 800;
const GRID_COLUMNS = 16;
const GRID_ROWS = 12;

const Background: React.FC<{ accent: string; accent2: string }> = ({
  accent,
  accent2,
}) => {
  const frame = useCurrentFrame();
  const angle = frame * 1.2;
  const gridOffset = (frame / 15) % 1;

  return (
    <AbsoluteFill style={{ backgroundColor: "#07070d" }}>
      <AbsoluteFill
        style={{
          background: `conic-gradient(from ${angle}deg at 50% 45%, ${accent}33, transparent 25%, ${accent2}33, transparent 60%, ${accent}33)`,
          filter: "blur(80px)",
        }}
      />
      {/* Retro perspective grid scrolling towards the viewer */}
      <svg
        width={1080}
        height={GRID_HEIGHT}
        style={{ position: "absolute", bottom: 0, left: 0 }}
      >
        <defs>
          <linearGradient id="fade" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="white" stopOpacity={0} />
            <stop offset="0.5" stopColor="white" stopOpacity={1} />
          </linearGradient>
          <mask id="gridMask">
            <rect width={1080} height={GRID_HEIGHT} fill="url(#fade)" />
          </mask>
        </defs>
        <g mask="url(#gridMask)" stroke={accent} strokeWidth={3} opacity={0.7}>
          {new Array(GRID_COLUMNS + 1).fill(0).map((_, i) => {
            const x = -1080 + (i / GRID_COLUMNS) * 3240;
            return <line key={`v${i}`} x1={540} y1={0} x2={x} y2={GRID_HEIGHT} />;
          })}
          {new Array(GRID_ROWS).fill(0).map((_, i) => {
            // Rows move towards the viewer; squaring the position fakes perspective
            const t = (i + gridOffset) / GRID_ROWS;
            const y = t * t * GRID_HEIGHT;
            return <line key={`h${i}`} x1={0} y1={y} x2={1080} y2={y} />;
          })}
        </g>
      </svg>
    </AbsoluteFill>
  );
};

const Letter: React.FC<{
  char: string;
  index: number;
  accent: string;
  accent2: string;
}> = ({ char, index, accent, accent2 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const progress = spring({
    frame: frame - 8 - index * 4,
    fps,
    config: { damping: 11, stiffness: 160 },
  });
  const y = interpolate(progress, [0, 1], [-400, 0]);
  const rotate = interpolate(progress, [0, 1], [index % 2 ? 40 : -40, 0]);

  // Short RGB-split glitch around frame 55 and 100
  const glitch =
    (frame > 52 && frame < 58) || (frame > 98 && frame < 102)
      ? (index % 2 ? 1 : -1) * 14
      : 0;

  return (
    <span
      style={{
        display: "inline-block",
        transform: `translateY(${y}px) rotate(${rotate}deg) translateX(${glitch}px)`,
        opacity: progress,
        textShadow: `${-6 - glitch}px 0 ${accent2}, ${6 + glitch}px 0 ${accent}, 0 0 40px ${accent}`,
      }}
    >
      {char}
    </span>
  );
};

export const PlayHQIntro: React.FC<PlayHQIntroProps> = ({
  title,
  handle,
  tagline,
  accent,
  accent2,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const taglineIn = spring({ frame: frame - 45, fps, config: { damping: 200 } });
  const handleIn = spring({ frame: frame - 65, fps, config: { damping: 14 } });
  const ctaIn = spring({ frame: frame - 90, fps, config: { damping: 12 } });
  const pulse = 1 + Math.sin(frame / 4) * 0.04 * ctaIn;
  const flash = interpolate(frame, [8, 12, 20], [0, 0.6, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const fadeOut = interpolate(
    frame,
    [durationInFrames - 12, durationInFrames],
    [1, 0],
    { extrapolateLeft: "clamp" },
  );

  return (
    <AbsoluteFill style={{ fontFamily: "Impact, 'Arial Black', sans-serif" }}>
      <Background accent={accent} accent2={accent2} />
      <AbsoluteFill
        style={{
          justifyContent: "center",
          alignItems: "center",
          flexDirection: "column",
          opacity: fadeOut,
          paddingBottom: 300,
        }}
      >
        <div
          style={{
            fontSize: 230,
            color: "white",
            letterSpacing: 8,
            fontStyle: "italic",
          }}
        >
          {title.split("").map((c, i) => (
            <Letter key={i} char={c} index={i} accent={accent} accent2={accent2} />
          ))}
        </div>
        <div
          style={{
            marginTop: 20,
            height: 10,
            width: 700 * taglineIn,
            background: `linear-gradient(90deg, ${accent}, ${accent2})`,
            borderRadius: 5,
            boxShadow: `0 0 30px ${accent}`,
          }}
        />
        <div
          style={{
            marginTop: 40,
            fontSize: 70,
            color: "white",
            fontFamily: "Arial, sans-serif",
            fontWeight: 800,
            opacity: taglineIn,
            transform: `translateY(${(1 - taglineIn) * 40}px)`,
          }}
        >
          {tagline}
        </div>
        <div
          style={{
            marginTop: 30,
            fontSize: 80,
            color: accent,
            fontFamily: "Arial, sans-serif",
            fontWeight: 900,
            transform: `scale(${handleIn})`,
            textShadow: `0 0 30px ${accent}`,
          }}
        >
          {handle}
        </div>
      </AbsoluteFill>
      <AbsoluteFill
        style={{
          justifyContent: "flex-end",
          alignItems: "center",
          paddingBottom: 260,
          opacity: fadeOut,
        }}
      >
        <div
          style={{
            fontFamily: "Arial, sans-serif",
            fontWeight: 900,
            fontSize: 64,
            color: "#07070d",
            background: `linear-gradient(90deg, ${accent}, ${accent2})`,
            padding: "28px 70px",
            borderRadius: 999,
            transform: `scale(${ctaIn * pulse})`,
            boxShadow: `0 0 50px ${accent2}aa`,
          }}
        >
          ▶ FOLGEN FÜR MEHR
        </div>
      </AbsoluteFill>
      <AbsoluteFill style={{ backgroundColor: "white", opacity: flash }} />
    </AbsoluteFill>
  );
};
