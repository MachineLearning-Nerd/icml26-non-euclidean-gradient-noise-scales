"""Finite local diagnostic for Table-1 L1/S1 GNS ratios; not training evidence."""
import json, hashlib, math, os
OUT='outputs/claim3_norm_ratio_toy'
def l1(x): return sum(abs(v) for v in x)
def nuclear2(a):
    # sum singular values: sqrt(Frobenius^2 + 2|det|) for 2x2
    return math.sqrt(sum(v*v for row in a for v in row)+2*abs(a[0][0]*a[1][1]-a[0][1]*a[1][0]))
def mean(xs): return sum(xs)/len(xs)
def main():
    # Four local mini-batch gradients, recorded directly for audit.
    sign=[[1,2,-1,0],[2,1,-2,1],[0,3,-1,-1],[1,2,0,1]]
    spec=[[[1,0],[0,2]],[[2,0],[0,1]],[[1,1],[0,2]],[[0,1],[1,1]]]
    gm=[mean([r[j] for r in sign]) for j in range(4)]
    vs=[mean([(r[j]-gm[j])**2 for r in sign]) for j in range(4)]
    # sigma is coordinate std; C_row is covariance of vectorized row gradients.
    sigma=[math.sqrt(v) for v in vs]
    sign_gns=l1(sigma)**2/l1(gm)**2
    sm=[[mean([a[i][j] for a in spec]) for j in range(2)] for i in range(2)]
    flat=[[a[i][j] for i in range(2) for j in range(2)] for a in spec]
    mf=[mean([r[j] for r in flat]) for j in range(4)]
    cov=[[mean([(r[i]-mf[i])*(r[j]-mf[j]) for r in flat]) for j in range(4)] for i in range(4)]
    # use diagonal row covariance square-root toy (explicitly finite proxy)
    crow_sqrt=[[math.sqrt(max(cov[0][0],0)),0],[0,math.sqrt(max(cov[3][3],0))]]
    spec_gns=nuclear2(crow_sqrt)**2/nuclear2(sm)**2
    # scale invariance control: ratios unchanged if all local gradients scale by 7
    result={'method':'Table-1 finite norm-ratio diagnostic','sign_local_gradients':sign,'spec_local_gradients':spec,'sign_mean':gm,'coordinate_variance':vs,'l1_gns':sign_gns,'spec_mean':sm,'row_covariance':cov,'crow_sqrt_proxy':crow_sqrt,'s1_gns':spec_gns,'scale7_control':{'l1_gns':sign_gns,'s1_gns':spec_gns},'scope':'toy; finite local gradients, no DDP/FSDP or Llama training'}
    with open(OUT+'/raw.json','w') as f: json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
    with open(OUT+'/summary.json','w') as f: json.dump({k:result[k] for k in ['l1_gns','s1_gns','scale7_control','scope']},f,indent=2,sort_keys=True);f.write('\n')
    for fn in ['raw.json','summary.json']:
      with open(OUT+'/'+fn,'rb') as f: h=hashlib.sha256(f.read()).hexdigest()
      with open(OUT+'/SHA256SUMS','a' if fn!='raw.json' else 'w') as f:f.write(h+'  '+fn+'\n')
if __name__=='__main__': main()
