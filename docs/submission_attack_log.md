# Submission Attack Log

## Attack 1: Raw residual thresholding may be enough.

Result: Rejected in the full-scale suite. Raw energy reaches 0.597 F1 and 0.491 utility; calibrated causal tactile residuals reach 0.738 F1 and 0.621 utility.

## Attack 2: Uncertainty gating may be enough.

Result: Rejected in the full-scale suite. The uncertainty gate reaches 0.550 F1 and 0.451 utility.

## Attack 3: Shape-only diagnosis may be enough.

Result: Rejected. Residual-shape-only diagnosis reaches 0.576 F1 and misses too many external contacts.

## Attack 4: Calibration is the real dependency.

Result: Sustained as a boundary. The final paper treats calibration metadata as part of the residual interface and reports performance under seven calibration regimes.

## Attack 5: The result assumes contact graph structure.

Result: Sustained as scope. The method targets contact-structured controllers or learned systems that expose an active contact hypothesis.
