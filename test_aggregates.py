import csv
from pathlib import Path
p = Path(__file__).parent / 'data'
def read(name):
    with (p/name).open() as f:
        return list(csv.DictReader(f))
r=read('longitudinal_summary.csv')
assert len(r)==7 and len({x['model'] for x in r})==7
assert all(0<=float(x[k])<=1 for x in r for k in ('auc','brier'))
s=read('scenarios.csv')
assert len(s)==6
for period,total in [('2026 Oct-Dec',26812802),('2027 Jun-Aug',33502404)]:
    rows=sorted((x for x in s if x['period']==period),key=lambda x:float(x['assumed_absolute_rate_change']))
    assert len(rows)==3 and int(rows[1]['conditional_people'])==total
    assert int(rows[0]['conditional_people'])<total<int(rows[2]['conditional_people'])
b=read('bootstrap.csv')
assert all(float(b[0][k])<0<float(b[1][k]) for k in ('auc_delta','brier_delta'))
print('Published summary consistency checks passed')
