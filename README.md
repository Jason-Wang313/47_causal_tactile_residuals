# Calibrated Causal Tactile Residuals

Paper 47 for the robotics 60-paper batch.

Status: final_v3_full_scale.

Canonical PDF:

- `C:/Users/wangz/Downloads/47.pdf`
- Pages: 25
- Bytes: 395898
- SHA256: `0CC14476F0B7707BF023E56647368FC648791275818223E70F66BC38F1057BE5`

Final evidence:

- Full-scale compact rows: 352800.
- Represented trajectory evaluations: 53936064000.
- Represented frame-level residual decisions: 5177862144000.
- Calibrated causal tactile residual F1: 0.738.
- Calibrated causal tactile residual utility: 0.621.
- Raw residual energy F1: 0.597.
- Uncertainty gate F1: 0.550.
- Oracle source classifier F1: 0.949.

Important files:

- `paper/main.tex`: final manuscript source.
- `scripts/run_full_scale_tactile_suite.py`: deterministic full-scale experiment runner.
- `scripts/build_pdf.ps1`: canonical PDF builder and hash recorder.
- `docs/full_scale_execution_plan.md`: pre-edit plan and final outcome.
- `results/full_scale/`: generated condition rows, summaries, validation JSON, and LaTeX tables.
- `paper/figures/full_scale/`: generated PDF figures imported by the manuscript.

Rebuild commands:

- `python scripts/run_full_scale_tactile_suite.py`
- `powershell -ExecutionPolicy Bypass -File scripts/build_pdf.ps1`

The build script copies the generated PDF to `C:/Users/wangz/Downloads/47.pdf` and removes `paper/main.pdf`.
