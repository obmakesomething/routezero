import requests,pandas as pd,numpy as np,time
u='https://raw.githubusercontent.com/eonsystemspbc/fly-brain/main/data/2025_Connectivity_783.parquet';p='/tmp/c.parquet'
r=requests.get(u,timeout=180);r.raise_for_status();open(p,'wb').write(r.content)
d=pd.read_parquet(p,columns=['Presynaptic_Index','Postsynaptic_Index','Excitatory x Connectivity'])
a=d.Presynaptic_Index.to_numpy(np.int64);b=d.Postsynaptic_Index.to_numpy(np.int64);ww=d['Excitatory x Connectivity'].to_numpy(np.float32);N=max(a.max(),b.max())+1
sensg=np.array([69093,97602,122795,124291,29281,100605,110469,51107,49584,129730,126873,28825,126600,126752,32863,108426,111357,14842,90589,92298,12494]);p9g=np.array([83620,119032]);anc=np.r_[sensg,p9g]
wd=np.bincount(a,weights=np.abs(ww),minlength=N)+np.bincount(b,weights=np.abs(ww),minlength=N);m=np.isin(a,anc)|np.isin(b,anc);nei=np.unique(np.r_[a[m],b[m]]);cand=list(anc)+list(nei[np.argsort(wd[nei])[::-1]])+list(np.argsort(wd)[::-1]);sel=[];seen=set()
for x in cand:
 x=int(x)
 if x not in seen:sel.append(x);seen.add(x)
 if len(sel)==4000:break
sel=np.array(sel);loc=np.full(N,-1,np.int32);loc[sel]=np.arange(4000);em=(loc[a]>=0)&(loc[b]>=0);pre=loc[a[em]];post=loc[b[em]];w=ww[em];o=np.argsort(pre,kind='stable');pre,post,w=pre[o],post[o],w[o];ptr=np.r_[0,np.cumsum(np.bincount(pre,minlength=4000))];sens=loc[sensg];p9=loc[p9g]
pm=np.isin(a,p9g)|np.isin(b,p9g);pn=np.unique(np.r_[a[pm],b[pm]]);pn=pn[loc[pn]>=0];read=np.unique(np.r_[p9,loc[pn[np.argsort(wd[pn])[::-1]]]])[:128]
DT=.1;rb=22;rng=np.random.default_rng(7);v=np.full(4000,-52.,np.float32);g=np.zeros(4000,np.float32);sp=np.zeros(4000,np.uint8);rf=np.full(4000,rb,np.int16);rs=np.full(4000,rb,np.int16);rs[sens]=0;buf=np.zeros((19,4000),np.float32);bi=0;cnt=np.zeros(4000,np.int32);events=0;rates=np.zeros(4000,np.float32);rates[sens]=200.;t0=time.perf_counter()
for _ in range(1000):
 rec=np.zeros(4000,np.float32)
 for i in np.flatnonzero(sp):
  s,e=ptr[i],ptr[i+1];np.add.at(rec,post[s:e],w[s:e]);events+=e-s
 rec*=.275;rf=np.where(sp,0,rf+1);gn=g*.98+buf[bi].copy()*(rf>=rs);buf[bi]=rec;bi=(bi+1)%19;v+=.275*(rng.random(4000)<rates*.0001)*250;v+=.005*(g-(v+52));ns=v>-45;v=np.where(ns,-52.,v);gn=np.where(ns,0.,gn);sp=ns.astype(np.uint8);cnt+=sp;g=gn
print('edges',len(w),'read_n',len(read),'elapsed_100ms',time.perf_counter()-t0,'spikes',int(cnt.sum()),'active',int((cnt>0).sum()),'events',int(events),'p9',cnt[p9].tolist(),'read_sum',int(cnt[read].sum()),'read_nonzero',int((cnt[read]>0).sum()),flush=True)
