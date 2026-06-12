import csv, re, os, json
from collections import Counter,defaultdict
path='docs/related_work_matrix.csv'
rows=list(csv.DictReader(open(path,encoding='utf-8')))
keywords=['contact','tactile','haptic','slip','world model','prediction','residual','force','torque','manipulation','anomaly','state estimation','control','sim-to-real','vision-based tactile']
clusters=defaultdict(list)
for r in rows:
    t=r['title'].lower()
    for k in keywords:
        if k in t:
            clusters[k].append(r)
for k in keywords:
    print('\n##',k,len(clusters[k]))
    for r in clusters[k][:8]:
        print(r['year'],r['title'])
