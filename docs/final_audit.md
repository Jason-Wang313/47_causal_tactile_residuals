# Final Audit

Paper: 47_causal_tactile_residuals

Decision: workshop-only

Submission-hardening version: v2

## Original evidence

- Raw threshold: accuracy 0.877, precision 0.863, recall 0.896, F1 0.879.
- Uncertainty gate: accuracy 0.917, precision 0.903, recall 0.933, F1 0.918.
- Causal tactile residual: accuracy 0.994, precision 0.996, recall 0.992, F1 0.994.

## V2 shape-calibration stress

- Shape gain 0.8: causal F1 0.957, still above uncertainty gate F1 0.918.
- Shape gain 0.7: causal F1 0.891, below uncertainty gate F1 0.918.
- Shape gain 0.6: causal F1 0.812.
- Shape gain 0.5: causal F1 0.667.

## Main blocker

The paper remains synthetic and assumes calibrated tactile feature extraction. The v2 stress shows the clean causal rule can lose to a simpler uncertainty gate when asymmetry, onset-lag, and spatial-jump features are under-reported.

## Submission decision

Workshop-only. The paper is coherent as a mechanism and diagnostic benchmark, but it is not ready for a main robotics conference without real tactile traces, hardware validation, and robustness to sensor/feature calibration shifts.

## Artifact audit

- Canonical PDF: `C:/Users/wangz/Downloads/47.pdf`
- Local generated PDF: removed after build
- Desktop copy: absent
- Build script: `scripts/build_pdf.ps1`
- V2 stress script: `scripts/v2_shape_calibration_stress.py`
