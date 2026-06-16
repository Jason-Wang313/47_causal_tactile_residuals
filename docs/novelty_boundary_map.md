# Novelty Boundary Map

| Nearby line | What it already covers | Why the final thesis is distinct |
|---|---|---|
| Slip detection / force control | Detects loss of grasp or contact change | Usually reactive thresholding, not adaptation-versus-recovery source selection |
| Contact state estimation | Infers contact state from tactile or force cues | Labels contact state, not residual source for controller response |
| Tactile world models | Predict future tactile states | Prediction is used, but residual interpretation is not usually the central interface |
| Anomaly detection / introspection | Flags unexpected robot behavior | Broad anomaly labels, not calibrated tactile contact-source diagnosis |
| Visuo-tactile control | Uses touch with vision for closed-loop manipulation | Fuses modalities, but tactile residuals are rarely framed as response-source selectors |

Final boundary:

The paper is about calibrated tactile residuals as a source-diagnostic interface. Its distinct claim is not that touch can detect contact, but that calibrated residual geometry and contact-graph inconsistency can choose between model adaptation and external-contact recovery.
