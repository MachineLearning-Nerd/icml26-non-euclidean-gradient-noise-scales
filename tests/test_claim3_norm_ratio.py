import json, subprocess
subprocess.run(['python3','src/claim3_norm_ratio_toy.py'],check=True)
d=json.load(open('outputs/claim3_norm_ratio_toy/raw.json'))
assert d['l1_gns']>0 and d['s1_gns']>0
assert d['l1_gns']==d['scale7_control']['l1_gns']
