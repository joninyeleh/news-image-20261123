// News-image daily entry (Node 22, standard library only).
//
// The entry is the PNG beside this file (entry.png, 1024x1024, drawn by
// render.py). The program copies it unchanged to the grader's output
// directory, so the judge sees exactly those bytes. The copy is
// deterministic: two runs produce identical output bytes.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
// /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

const source = new URL('./entry.png', import.meta.url);
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

copyFileSync(source, join(outDir, 'entry.png'));
