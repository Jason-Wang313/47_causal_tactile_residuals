# Novelty Boundary Map

| Nearby line | What it already covers | Why it is not yet the thesis |
|---|---|---|
| Slip detection / force control | Detects loss of grasp or contact change | Usually reactive thresholding, not separation of model misspecification from external contact |
| Contact state estimation | Infers contact state from tactile or force cues | Labels contact state, not source of residual |
| Tactile world models | Predict future tactile states | Predictive, but residual interpretation is not the central interface |
| Anomaly detection / introspection | Flags unexpected robot behavior | Broad anomaly labels, not tactile contact-source diagnosis |
| Visuo-tactile control | Uses touch with vision for closed-loop manipulation | Fuses modalities, but tactile residuals are not framed as causal response selectors |

## V2 boundary

Causal residuals are useful only when residual-shape and timing features remain calibrated. At 0.7 shape-feature gain, the uncertainty gate becomes stronger than the causal rule in this synthetic diagnostic.
