// World News One Image — 21 November 2026.
// Entry point: runs the poster drawing program and writes /output/entry.png.
// The drawing program is deterministic: same input, same bytes, every run.
import { spawnSync } from "node:child_process";
import { mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const script = join(here, "draw_poster.py");
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";

mkdirSync(outDir, { recursive: true });

const run = spawnSync("python3", [script, outDir], { stdio: "inherit" });
if (run.error) {
  console.error("poster draw failed:", run.error.message);
  process.exit(1);
}
if (run.status !== 0) {
  console.error(`poster draw exited with status ${run.status}`);
  process.exit(run.status ?? 1);
}
console.log(`entry.png written to ${join(outDir, "entry.png")}`);
