import os,time,requests,pandas as pd,numpy as np
URL='https://raw.githubusercontent.com/eonsystemspbc/fly-brain/main/data/2025_Connectivity_783.parquet'
SENSG=np.array([69093,97602,122795,124291,29281,100605,110469,51107,49584,129730,126873,28825,126600,126752,32863,108426,111357,14842,90589,92298,12494])
P9G=np.array([83620,119032])

def load(n=4000,seed=1):
 p='/tmp/flywire783.parquet'
 if not os.path.exists(p):
  r=requests.get(URL,timeout=180);r.raise_for_status();open(p,'wb').write(r.content)
 d=pd.read_parquet(p,columns=['Presynaptic_Index','Postsynaptic_Index','Excitatory x Connectivity'])
 a=d.Presynaptic_Index.to_numpy(np.int64);b=d.Postsynaptic_Index.to_numpy(np.int64);w0=d['Excitatory x Connectivity'].to_numpy(np.float32);N=max(a.max(),b.max())+1
 wd=np.bincount(a,weights=np.abs(w0),minlength=N)+np.bincount(b,weights=np.abs(w0),minlength=N);anc=np.r_[SENSG,P9G];m=np.isin(a,anc)|np.isin(b,anc);nei=np.unique(np.r_[a[m],b[m]]);cand=list(anc)+list(nei[np.argsort(wd[nei])[::-1]])+list(np.argsort(wd)[::-1]);sel=[];seen=set()
 for x in cand:
  x=int(x)
  if x not in seen:sel.append(x);seen.add(x)
  if len(sel)>=n:break
 sel=np.array(sel);loc=np.full(N,-1,np.int32);loc[sel]=np.arange(n);em=(loc[a]>=0)&(loc[b]>=0);pre=loc[a[em]];post=loc[b[em]];w=w0[em];o=np.argsort(pre,kind='stable');pre,post,w=pre[o],post[o],w[o];ptr=np.r_[0,np.cumsum(np.bincount(pre,minlength=n))].astype(np.int64)
 sens=loc[SENSG];sn=np.unique(np.r_[a[np.isin(a,SENSG)|np.isin(b,SENSG)],b[np.isin(a,SENSG)|np.isin(b,SENSG)]]);ban=set(SENSG.tolist()+sn.tolist());rc=[int(x) for x in sel[np.argsort(wd[sel])[::-1]] if int(x) not in ban];read=loc[np.array(rc[:min(512,len(rc))])]
 rng=np.random.default_rng(seed);variants={'real':(post.copy(),w.copy()),'weight_shuffle':(post.copy(),rng.permutation(w)),'topology_shuffle':(rng.permutation(post),w.copy()),'zero':(post.copy(),np.zeros_like(w))}
 return {'n':n,'edges':len(w),'ptr':ptr,'sens':sens,'read':read,'variants':variants,'graph_bytes':int(post.nbytes+w.nbytes+ptr.nbytes)}

class SNN:
 def __init__(self,G,name,seed=1):
  self.n=G['n'];self.ptr=G['ptr'];self.post,self.w=G['variants'][name];self.sens=G['sens'];self.read=G['read'];self.rng=np.random.default_rng(seed);self.reset()
 def reset(self):
  n=self.n;self.v=np.full(n,-52.,np.float32);self.g=np.zeros(n,np.float32);self.sp=np.zeros(n,np.uint8);self.rf=np.full(n,22,np.int16);self.rs=np.full(n,22,np.int16);self.rs[self.sens]=0;self.buf=np.zeros((19,n),np.float32);self.bi=0;self.events=0
 def window(self,rates,ms=20):
  cnt=np.zeros(len(self.read),np.int16);t0=time.perf_counter();steps=int(ms/.1)
  for _ in range(steps):
   rec=np.zeros(self.n,np.float32)
   for i in np.flatnonzero(self.sp):
    s,e=self.ptr[i],self.ptr[i+1]
    if e>s:np.add.at(rec,self.post[s:e],self.w[s:e]);self.events+=int(e-s)
   rec*=.275;self.rf=np.where(self.sp,0,self.rf+1);gn=self.g*.98+self.buf[self.bi].copy()*(self.rf>=self.rs);self.buf[self.bi]=rec;self.bi=(self.bi+1)%19
   fire=self.rng.random(len(self.sens))<rates*.0001;self.v[self.sens]+=.275*fire*250;self.v+=.005*(self.g-(self.v+52));ns=self.v>-45;self.v=np.where(ns,-52.,self.v);gn=np.where(ns,0.,gn);self.sp=ns.astype(np.uint8);cnt+=self.sp[self.read];self.g=gn
  feat=np.r_[cnt.astype(np.float32),self.v[self.read]+52.,self.g[self.read]].astype(np.float32)
  return feat,time.perf_counter()-t0
