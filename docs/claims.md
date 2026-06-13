# Claims

Supported claim:

- Tactile residuals can serve as a diagnostic channel, not just a reactive alarm.
- Under a contact-structured predictor, calibrated residual shape and timing can separate internal model mismatch from unexpected external contact better than raw thresholding.
- In the clean synthetic diagnostic, the causal residual rule reaches 0.994 external-contact F1, compared with 0.918 for the uncertainty gate and 0.879 for raw thresholding.

V2 narrowed claim:

The causal rule depends on calibrated residual-shape features. With asymmetry, onset-lag, and spatial-jump features attenuated to 0.7 gain, causal F1 falls to 0.891, below the uncertainty gate at 0.918. With 0.6 gain, causal F1 falls to 0.812.

Unsupported claim:

The paper does not demonstrate real tactile-skin robustness, learned feature extraction, human-contact safety, or broad causal identification.
