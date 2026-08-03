import json
x=json.load(open('contract/live_claims.json'));assert x['orid']=='XMSaWRpEPS' and len(x['claims'])==5
