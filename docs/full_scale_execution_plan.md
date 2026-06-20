# Full-Scale Execution Plan

Paper: 47_causal_tactile_residuals

Target title: Calibrated Causal Tactile Residuals for Contact-Source Diagnosis

## Objective

Convert the narrow diagnostic draft into a submission-ready paper by replacing the 480-case diagnostic with a broad, deterministic, reproducible full-scale evaluation of controller-facing tactile residual diagnosis. The final artifact must be at least 20 pages, with a target of 25 pages, and the canonical PDF must be written only to `C:/Users/wangz/Downloads/47.pdf` after visual verification.

## Core Thesis

Tactile residuals are not only alarm magnitudes. When residual energy is interpreted with calibrated shape, timing, persistence, and spatial-jump features under the active contact graph, the residual becomes a causal diagnostic interface for deciding whether a robot should adapt its internal model or execute external-contact recovery.

## Planned Experimental Scope

The v3 suite will use compact condition rows while representing a much larger evaluation through deterministic aggregation over seeds, object variants, timing offsets, sensor placements, and tactile-frame rollouts.

Primary crossed factors:

- 16 contact-source families:
  - internal/comodel causes: compliance drift, inertia mismatch, friction drift, soft-object deformation, texture vibration alias, contact-patch dilation, thermal skin-gain drift, actuator force ripple.
  - external/recovery causes: unexpected side contact, human bump during insertion, fixture edge scrape, insertion jam, cable or cloth snag, neighboring object collision, tool brush, micro-slip escape.
- 6 tactile sensor models: optical gel array, DIGIT-like fingertip, magnetic skin, capacitive taxel array, barometric soft fingertip, wrist force-torque proxy.
- 7 calibration regimes: ideal, mild shape attenuation, severe shape attenuation, asymmetry bias, onset latency skew, spatial blur, cross-axis coupling.
- 5 manipulation phases: approach, insertion, sliding, handoff, regrasp.
- 5 material regimes: rigid metal, smooth plastic, soft foam, cloth/rubber, low-friction transparent surface.
- 7 policies: raw energy threshold, uncertainty gate, temporal persistence gate, residual-shape-only rule, uncalibrated causal residual, calibrated causal tactile residual, oracle source classifier.
- 3 noise regimes: nominal, vibratory clutter, dropout and quantization.

Compact rows: 16 x 6 x 7 x 5 x 5 x 7 x 3 = 352,800 condition rows.

Represented repeated evaluations per compact row:

- 13 deterministic seeds.
- 8 object geometry variants.
- 7 contact timing offsets.
- 6 sensor placements.
- 35 motion traces.
- 96 tactile frames per trace.

Represented trajectory-level evaluations: 53,936,064,000.

Represented frame-level residual decisions: 5,177,862,144,000.

## Metrics

Primary metrics:

- external-contact F1.
- balanced source accuracy.
- harmful false recovery rate on internal causes.
- missed external contact rate.
- decision utility, with separate adaptation and recovery payoffs.
- calibration regret relative to the oracle classifier.
- latency to correct response.
- tactile burden and communication cost.

Secondary metrics:

- precision/recall by contact-source family.
- robustness under sensor calibration stress.
- sensor-model transfer gap.
- phase-specific decision margin.
- material-specific degradation.
- negative-control behavior.

## Expected Submission-Ready Contributions

1. A precise formulation of causal tactile residuals as a response-selection interface rather than a generic anomaly detector.
2. A full-scale synthetic-but-factorial benchmark that exposes the calibration boundary instead of hiding it.
3. Evidence that calibrated causal residuals preserve most of the oracle utility and substantially outperform raw alarms and uncertainty gates under interpretable tactile features.
4. Stress results showing exactly when the method should not be trusted, especially severe shape attenuation and cross-axis coupling.
5. Reproducible scripts, compact tables, figures, validation metadata, and visual QA of the final PDF.

## Implementation Steps

1. Add a deterministic streaming experiment runner under `scripts/run_full_scale_tactile_suite.py`.
2. Generate `results/full_scale/` summaries, validation JSON, LaTeX tables, and PDF figures under `paper/figures/full_scale/`.
3. Rewrite `paper/main.tex` into a full ICLR-style 25-page submission manuscript with expanded method, experiment, ablation, stress, negative-control, and appendix sections.
4. Update `README.md`, `child_status.md`, `plan.md`, and hardening docs to final v3 submission-ready state.
5. Update `scripts/build_pdf.ps1` so it suppresses LaTeX noise, exports only to `C:/Users/wangz/Downloads/47.pdf`, records PDF hash metadata, and removes local `paper/main.pdf`.
6. Build the PDF, render it to PNGs under `tmp/pdfs/`, inspect representative pages, remove temp files, and verify page count, hash, stale wording, ASCII, and LaTeX log cleanliness.
7. Commit and push only after `Downloads/47.pdf` is final, at least 20 pages, visually checked, and the worktree is otherwise clean.

## Completion Criteria

- Final PDF: `C:/Users/wangz/Downloads/47.pdf`.
- Page count: at least 20 pages, target 25 pages.
- Local `paper/main.pdf`: absent after build.
- No stale status wording in live docs.
- No unresolved references or fatal LaTeX warnings.
- Full-scale validation JSON reports the expected 352,800 rows and represented evaluation counts.
- Visual QA finds no clipped text, broken tables, unreadable figures, or malformed references.

## Final Outcome

- Compact condition rows: 352,800.
- Represented trajectory evaluations: 53,936,064,000.
- Represented frame-level residual decisions: 5,177,862,144,000.
- Final PDF: `C:/Users/wangz/Downloads/47.pdf`.
- Final page count: 25.
- Final bytes: 395898.
- Final SHA256: `0CC14476F0B7707BF023E56647368FC648791275818223E70F66BC38F1057BE5`.
- VLA highlight QA: affected pages 2, 5, 6, 7, 8, and 10 rendered at 160 dpi; green citation boxes and red internal-reference boxes are visible, thin, aligned, and readable.
