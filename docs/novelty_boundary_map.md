# Novelty Boundary Map

| Nearby line | What it already covers | Why it is not yet the thesis |
|---|---|---|
| Slip detection / force control | Detects loss of grasp or contact change | Usually reactive thresholding, not causal separation of model misspecification vs external contact |
| Contact state estimation | Infers contact state from tactile/force cues | Often assumes a stable process model and labels contact state, not source of residual |
| Tactile world models | Predict future tactile states | Predictive, but typically do not interpret residuals as a causal diagnostic channel |
| Anomaly detection / introspection | Flags unexpected robot behavior | Usually broad anomalies; not grounded in tactile contact physics |
| Visuo-tactile control | Uses touch with vision for closed-loop manipulation | Fuses modalities, but tactile is not centered as a residual explanation variable |
