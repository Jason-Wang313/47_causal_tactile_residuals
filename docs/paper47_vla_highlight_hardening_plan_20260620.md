# Paper 47 VLA Highlight Hardening Plan

Date: 2026-06-20

## Objective

Harden Paper 47's visible PDF link-box styling so it matches the VLA-v4 role-model PDF's professional red and green boxed callouts while preserving the final 25-page calibrated causal tactile residual manuscript, its full-scale benchmark, and all scientific claims.

## Current Evidence

- Canonical PDF: `C:/Users/wangz/Downloads/47.pdf`.
- Current page count: 25.
- Current affected link pages: 2, 5, 6, 7, 8, and 10.
- Current link annotations: 15 green citation/link boxes and 10 red internal-reference boxes.
- Current border state: all 25 link annotations use border `(0, 0, 0)`, so the boxes are invisible.
- Current LaTeX source uses `\usepackage[hidelinks]{hyperref}` in `paper/main.tex`.
- Current full-scale benchmark remains 352,800 compact condition rows, 53,936,064,000 represented trajectory evaluations, and 5,177,862,144,000 frame-level residual decisions.

## Role-Model Style Target

Match the VLA-v4 role model's link annotation style:

```tex
\usepackage{hyperref}
\hypersetup{
  colorlinks=false,
  pdfborder={0 0 1},
  citebordercolor={0 1 0},
  linkbordercolor={1 0 0},
  urlbordercolor={0 1 0}
}
```

Expected Paper 47 result after rebuild:

- Page count remains 25.
- All 15 citation/link annotations remain green.
- All 10 internal-reference link annotations remain red.
- All 25 link annotations use visible border `(0, 0, 1)`.
- No benchmark data, tables, figures, claims, or manuscript body text changes.

## Execution Plan

1. Render the affected pre-change pages to `C:/Users/wangz/highlight_box_hardening/tmp/pdfs/paper47_before` for baseline visual comparison.
2. Replace `\usepackage[hidelinks]{hyperref}` in `paper/main.tex` with plain `\usepackage{hyperref}` plus the VLA-v4 `\hypersetup` block above.
3. Rebuild using `scripts/build_pdf.ps1`, which exports only `C:/Users/wangz/Downloads/47.pdf`, records build metadata, and removes local `paper/main.pdf`.
4. Verify with `pypdf` that the rebuilt PDF has 25 pages, 15 green link annotations, 10 red link annotations, and 25 `(0, 0, 1)` borders.
5. Render affected post-change pages 2, 5, 6, 7, 8, and 10 and visually inspect the boxes for role-model-like color, line weight, alignment, spacing, and legibility.
6. Update README, child status, and tracked audit/readiness metadata with the final hash, size, and visual hardening evidence.
7. Remove Paper 47 temporary render folders after QA while preserving the shared `role_model` render.
8. Commit and push the clean repo before moving to the next paper.

## Non-Goals

- Do not rerun the benchmark.
- Do not pad content or alter the 25-page manuscript.
- Do not revise claims, tables, captions, figures, or body text unless visual QA exposes a layout defect that requires a tiny local fix.

## Final QA Result

- Rebuilt canonical PDF: `C:/Users/wangz/Downloads/47.pdf`.
- Final page count: 25.
- Final size: 395898 bytes.
- Final SHA256: `0CC14476F0B7707BF023E56647368FC648791275818223E70F66BC38F1057BE5`.
- Verified annotations: 15 green citation boxes, 10 red internal-reference boxes, and 25 visible `(0, 0, 1)` borders.
- Rendered pages 2, 5, 6, 7, 8, and 10 at 160 dpi; the boxes match the VLA-v4 role model's thin, professional style and do not create layout collisions.
