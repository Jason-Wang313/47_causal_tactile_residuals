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
- Final PDF SHA256: `CFDC5FA2E275C699628D2D1A6C3D460954CE6B09FFACBFC4C5D8D988A32DAB61`.
- Determinism: stable hash-based condition jitter, fixed factor maps, no global random state.
