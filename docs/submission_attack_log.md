# Submission Attack Log

## Attack 1: Raw residual thresholding may be enough.

Result: Partially rejected. Raw thresholding reaches 0.879 F1, while clean causal residuals reach 0.994 F1.

Decision impact: The clean mechanism is useful but not enough for a strong venue.

## Attack 2: Uncertainty gating may be enough under calibration shift.

Result: Sustained. At 0.7 shape-feature gain, causal residual F1 falls to 0.891 while the uncertainty gate remains at 0.918.

Decision impact: The paper must claim calibrated residual-shape diagnosis, not generic robustness.

## Attack 3: The result assumes labeled cause and contact graph structure.

Result: Sustained. The synthetic benchmark does not prove causal identification or feature extraction in hardware.

Decision impact: workshop-only.
