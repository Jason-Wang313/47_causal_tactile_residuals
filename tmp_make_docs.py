import csv, os, re, textwrap, json
from collections import defaultdict
base='docs'
rows=list(csv.DictReader(open(os.path.join(base,'related_work_matrix.csv'),encoding='utf-8')))
for r in rows:
    r['score_f']=float(r['score']) if r['score'] else 0.0
# select tactile/contact-centric papers
keys=['tactile','contact','haptic','slip','force','torque','world model','prediction','residual','anomaly','state estimation','control','sim-to-real']
selected=[]
seen=set()
for r in sorted(rows, key=lambda x:(-x['score_f'], x['year'], x['title'])):
    t=r['title'].lower()
    if any(k in t for k in keys):
        norm=re.sub(r'\s+',' ',t)
        if norm in seen: continue
        seen.add(norm)
        selected.append(r)
    if len(selected)>=120:
        break
# write hostile set
with open(os.path.join(base,'hostile_prior_work.md'),'w',encoding='utf-8') as f:
    f.write('# Hostile Prior Work\n\n')
    f.write('This set is intentionally pessimistic: each paper is treated as if it could already absorb part of the proposed mechanism unless its assumptions clearly differ.\n\n')
    for i,r in enumerate(selected[:100],1):
        f.write(f"{i}. **{r['title']}** ({r['year']}, {r['venue']}) - {r['url']}\n")
# literature map
clusters=defaultdict(list)
for r in rows:
    t=r['title'].lower()
    for k in ['tactile','contact','slip','world model','prediction','residual','anomaly','state estimation','control','sim-to-real']:
        if k in t:
            clusters[k].append(r)
with open(os.path.join(base,'literature_map.md'),'w',encoding='utf-8') as f:
    f.write('# Literature Map\n\n')
    f.write('## Core thesis space\n\n')
    f.write('- Tactile sensing has been used for contact detection, slip detection, state estimation, force control, and visuo-tactile manipulation.\n')
    f.write('- Recent work moves toward tactile/world models and contact-rich policies, but mostly treats tactile as an observation stream rather than a causal diagnostic signal.\n')
    f.write('- The likely wedge is separating internal model error from exogenous contact disturbances through tactile residuals.\n\n')
    for k in ['tactile','contact','slip','world model','prediction','residual','anomaly','state estimation','control','sim-to-real']:
        f.write(f'## {k.title()} ({len(clusters[k])})\n\n')
        for r in clusters[k][:10]:
            f.write(f"- {r['year']} {r['title']}\n")
        f.write('\n')
# novelty boundary map
with open(os.path.join(base,'novelty_boundary_map.md'),'w',encoding='utf-8') as f:
    f.write('# Novelty Boundary Map\n\n')
    f.write('| Nearby line | What it already covers | Why it is not yet the thesis |\n|---|---|---|\n')
    rows_map=[
        ('Slip detection / force control','Detects loss of grasp or contact change','Usually reactive thresholding, not causal separation of model misspecification vs external contact'),
        ('Contact state estimation','Infers contact state from tactile/force cues','Often assumes a stable process model and labels contact state, not source of residual'),
        ('Tactile world models','Predict future tactile states','Predictive, but typically do not interpret residuals as a causal diagnostic channel'),
        ('Anomaly detection / introspection','Flags unexpected robot behavior','Usually broad anomalies; not grounded in tactile contact physics'),
        ('Visuo-tactile control','Uses touch with vision for closed-loop manipulation','Fuses modalities, but tactile is not centered as a residual explanation variable'),
    ]
    for a,b,c in rows_map:
        f.write(f'| {a} | {b} | {c} |\n')
# claims
with open(os.path.join(base,'claims.md'),'w',encoding='utf-8') as f:
    f.write('# Claims\n\n')
    f.write('1. Tactile residuals can be used as a causal diagnostic channel, not just a reactive alarm.\n')
    f.write('2. Under a contact-structured predictor, residual shape and timing can separate expected model error from unexpected external contact better than raw thresholding.\n')
    f.write('3. This distinction matters because the two cases call for different robot responses: model adaptation vs interruption / recovery.\n')
    f.write('4. Existing tactile/contact papers mostly estimate state, detect slip, or improve control; they do not center the residual as an explanatory variable with a causal role.\n')
    f.write('5. The paper is strongest if it demonstrates the failure of a pure prediction-error baseline under exogenous contact and shows an operational separation signal.\n')
# reviewer attacks
with open(os.path.join(base,'reviewer_attacks.md'),'w',encoding='utf-8') as f:
    f.write('# Reviewer Attacks\n\n')
    attacks=[
        'Your residual is just a rebranding of contact anomaly detection.',
        'The model may only work because the tactile sensor is highly structured or the task set is narrow.',
        'The separation between model error and external contact may collapse under calibration drift or surface compliance changes.',
        'You do not prove causality; you only show correlation between residual patterns and contact events.',
        'A threshold on force magnitude could achieve the same behavior without the proposed mechanism.',
        'The approach may fail when contact is expected but not modeled, especially under novel objects.',
    ]
    for a in attacks:
        f.write(f'- {a}\n')
# novelty decision and final audit placeholders
with open(os.path.join(base,'novelty_decision.md'),'w',encoding='utf-8') as f:
    f.write('# Novelty Decision\n\n')
    f.write('Chosen direction: causal tactile residuals for disambiguating internal dynamics error from unexpected external contact.\n\n')
    f.write('Why this is the strongest candidate: it changes the role of touch from sensing state to explaining error source, which is a different central mechanism.\n\n')
    f.write('Rejected weaker directions: larger model, more data, generic uncertainty, generic active learning, or a generic tactile policy stack.\n')
