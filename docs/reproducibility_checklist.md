# Reproducibility Checklist

- Full-scale generator: `scripts/run_full_scale_tactile_suite.py`.
- Build script: `scripts/build_pdf.ps1`.
- Canonical PDF path: `C:/Users/wangz/Downloads/47.pdf`.
- Local generated PDF policy: `paper/main.pdf` is removed after build.
- Compact rows: `results/full_scale/condition_metrics.csv`.
- Summaries: `results/full_scale/*_summary.csv`.
- Validation: `results/full_scale/experiment_validation.json`.
- Figures: `paper/figures/full_scale/*.pdf`.
- Tables: `results/full_scale/table_*.tex`.
- Final PDF SHA256: `0CC14476F0B7707BF023E56647368FC648791275818223E70F66BC38F1057BE5`.
- Determinism: stable hash-based condition jitter, fixed factor maps, no global random state.
- Visual QA: render pages 2, 5, 6, 7, 8, and 10 at 160 dpi and confirm VLA-style green citation boxes and red internal-reference boxes are thin, aligned, readable, and collision-free.
