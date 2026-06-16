# Claims

Supported final claim:

- Tactile residuals can serve as controller-facing source evidence, not only alarm magnitudes.
- Under a contact-structured predictor, calibrated residual energy, residual shape, onset timing, spatial jump, persistence, and contact-graph inconsistency improve response selection between model adaptation and external-contact recovery.
- In the full-scale suite, calibrated causal tactile residuals reach 0.738 external-contact F1 and 0.621 utility across 352800 compact rows.
- The method improves over raw residual energy by 0.141 F1 and over uncertainty gating by 0.188 F1.
- The method reduces both harmful false recovery and missed external contact relative to the main alarm baselines.

Bounded claim:

- The result is a broad deterministic diagnostic benchmark, not hardware validation.
- The method assumes an active contact graph, phase label, and calibration metadata.
- Weak sensors, severe spatial blur, and weak positive events such as tool brush and micro-slip escape remain boundary cases.

Unsupported claim:

- The paper does not claim universal tactile causality, certified human-contact safety, or learned feature extraction robustness.
