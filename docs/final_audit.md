# Final Audit

Paper: 47_causal_tactile_residuals

Final title: Calibrated Causal Tactile Residuals for Contact-Source Diagnosis

Status: final_v3_full_scale

## Evidence

- Compact condition rows: 352800.
- Represented trajectory evaluations: 53936064000.
- Represented frame-level residual decisions: 5177862144000.
- Raw residual energy: F1 0.597, utility 0.491.
- Uncertainty gate: F1 0.550, utility 0.451.
- Uncalibrated causal residual: F1 0.633, utility 0.524.
- Calibrated causal tactile residual: F1 0.738, utility 0.621.
- Oracle source classifier: F1 0.949, utility 0.858.

## Main Finding

Calibrated causal tactile residuals are the strongest non-oracle policy and improve both harmful false recovery and missed external contact relative to alarm baselines.

## Boundaries

- The evidence is deterministic and synthetic.
- Hardware traces, human-subject safety, and learned tactile feature extraction are future validation layers.
- The method needs contact-graph context and calibration metadata.

## Artifact Audit

- Canonical PDF: `C:/Users/wangz/Downloads/47.pdf`
- Pages: 25
- Bytes: 395898
- SHA256: `0CC14476F0B7707BF023E56647368FC648791275818223E70F66BC38F1057BE5`
- Local generated PDF: removed after build
- Build script: `scripts/build_pdf.ps1`
- Full-scale runner: `scripts/run_full_scale_tactile_suite.py`
- Visual QA: rendered affected highlight pages 2, 5, 6, 7, 8, and 10 at 160 dpi from the canonical Downloads PDF; verified 15 green citation boxes, 10 red internal-reference boxes, and 25 visible `(0, 0, 1)` borders with no layout collisions.
