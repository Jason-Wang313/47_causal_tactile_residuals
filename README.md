# Causal Tactile Residuals

Paper 47 for the robotics 60-paper batch.

Decision: workshop-only.

The v2 shape-calibration stress narrows the claim. The clean causal tactile residual rule reaches 0.994 external-contact F1 on the synthetic diagnostic. When residual-shape features are attenuated to 0.8 gain, causal F1 remains 0.957. At 0.7 gain, causal F1 drops to 0.891, below the uncertainty gate at 0.918. The paper is therefore a mechanism note about calibrated residual-shape features, not a hardware-robust tactile diagnosis result.

Canonical PDF:

- `C:/Users/wangz/Downloads/47.pdf`

Important files:

- `paper/main.tex`: manuscript source.
- `docs/causal_tactile_residual_cases.csv`: original synthetic cases.
- `docs/v2_shape_calibration_stress.json`: v2 calibration stress summary.
- `docs/v2_shape_calibration_stress.csv`: v2 stress table data.
- `paper/v2_shape_calibration_table.tex`: manuscript table generated from v2 stress.
- `docs/final_audit.md`: final hardening audit.

Rebuild commands:

- `python scripts/v2_shape_calibration_stress.py`
- `powershell -ExecutionPolicy Bypass -File scripts/build_pdf.ps1`

The build script copies the generated PDF to `C:/Users/wangz/Downloads/47.pdf` and removes `paper/main.pdf`.
