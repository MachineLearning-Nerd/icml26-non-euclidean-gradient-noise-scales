import json
json.dump({'verdict':'inconclusive','reason':'literal 160M/3.2B-token benchmark is CPU-infeasible under local-only policy'},open('outputs/claim1_source_audit/summary.json','w'),indent=2)
