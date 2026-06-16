# Experiment Rigor Checklist

- Full-scale deterministic suite: yes.
- Compact condition rows: 352800.
- Represented trajectory-level evaluations: 53936064000.
- Represented frame-level residual decisions: 5177862144000.
- Contact-source families: 16.
- Sensor models: 6.
- Calibration regimes: 7.
- Manipulation phases: 5.
- Material regimes: 5.
- Policies: 7.
- Noise regimes: 3.
- Baselines: raw energy, uncertainty gate, temporal persistence, residual-shape only, uncalibrated causal residual, oracle source classifier.
- Negative controls: internal-cause harmful recovery summaries.
- Calibration stress: ideal, mild attenuation, severe attenuation, asymmetry bias, onset latency skew, spatial blur, cross-axis coupling.
- Validation metadata: `results/full_scale/experiment_validation.json`.
- Hardware validation: future work.

Decision: final v3 full-scale artifact is submission-ready within the scoped benchmark.
