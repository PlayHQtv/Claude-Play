import { Config } from "@remotion/cli/config";

// Cloud container: use the preinstalled Chromium instead of downloading one.
// Set REMOTION_BROWSER locally to override, or leave unset to let Remotion download.
const browser =
  process.env.REMOTION_BROWSER ??
  (require("fs").existsSync("/opt/pw-browsers/chromium")
    ? "/opt/pw-browsers/chromium"
    : null);
if (browser) {
  Config.setBrowserExecutable(browser);
}
Config.setVideoImageFormat("jpeg");
Config.setCodec("h264");
