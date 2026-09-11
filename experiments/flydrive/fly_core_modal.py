import os,time,requests,pandas as pd,numpy as np
CONN='https://raw.githubusercontent.com/eonsystemspbc/fly-brain/main/data/2025_Connectivity_783.parquet'
ANN='https://raw.githubusercontent.com/flyconnectome/flywire_annotations/main/supplemental_files/Supplemental_file1_neuron_annotations.tsv'

def _take(frame,cls,side,k,used,score_col='out_score'):
 q=frame[(frame.cell_class==cls)&(frame.side==side)&(~frame.root_id.isin(used))].sort_values(score_col,ascending=False).head(k)
 ids=[int(x) for x in q.root_id];used.update(ids);return ids

def load(n=4000,seed=1):
 p='/tmp/flywire783.parquet'
 if not os.path.exists(p):
  r=requests.get(CONN,timeout=180);r.raise_for_status();open(p,'wb').write(r.content)
 cols=['Presynaptic_ID','Postsynaptic_ID','Presynaptic_Index','Postsynaptic_Index','Excitatory x Connectivity']
 d=pd.read_parquet(p,columns=cols);a=d.Presynaptic_Index.to_numpy(np.int64);b=d.Postsynaptic_Index.to_numpy(np.int64);w0=d['Excitatory x Connectivity'].to_numpy(np.float32);N=max(a.max(),b.max())+1
 ann=pd.read_csv(ANN,sep='\t',low_memory=False);target=set(int(x) for x in ann.root_id.values)
 ids={}
 for rid,idx in zip(d.Presynaptic_ID.values,a):
  ri=int(rid)
  if ri in target:ids[ri]=int(idx)
 for rid,idx in zip(d.Postsynaptic_ID.values,b):
  ri=int(rid)
  if ri in target:ids.setdefault(ri,int(idx))
 absw=np.abs(w0);outw=np.bincount(a,weights=absw,minlength=N);inw=np.bincount(b,weights=absw,minlength=N);wd=outw+inw
 s=ann[(ann.flow=='afferent')&(ann.super_class=='sensory')].copy();s=s[s.root_id.map(lambda x:int(x) in ids)];s['out_score']=s.root_id.map(lambda x:outw[ids[int(x)]])
 used=set();groups=[]
 # observation: bearing, distance, left obstacle, front obstacle, right obstacle, angular velocity, speed
 groups.append(_take(s,'visual','left',8,used)+_take(s,'visual','right',8,used))
 groups.append(_take(s,'visual','left',8,used)+_take(s,'visual','right',8,used))
 groups.append(_take(s,'visual','left',16,used))
 groups.append(_take(s,'visual','left',8,used)+_take(s,'visual','right',8,used))
 groups.append(_take(s,'visual','right',16,used))
 groups.append(_take(s,'mechanosensory','left',8,used)+_take(s,'mechanosensory','right',8,used))
 groups.append(_take(s,'mechanosensory','left',8,used)+_take(s,'mechanosensory','right',8,used))
 if any(len(g)!=16 for g in groups):raise RuntimeError('could not select 16 neurons per modality group')
 sens_ids=[x for g in groups for x in g];sens_idx=np.array([ids[x] for x in sens_ids],np.int64)
 dn=ann[ann.super_class=='descending'].copy();dn=dn[dn.root_id.map(lambda x:int(x) in ids)];dn['in_score']=dn.root_id.map(lambda x:inw[ids[int(x)]])
 out_ids=[]
 for side in ['left','right']:out_ids += [int(x) for x in dn[dn.side==side].sort_values('in_score',ascending=False).head(128).root_id]
 desc_idx=np.array([ids[x] for x in out_ids],np.int64)
 anchors=np.r_[sens_idx,desc_idx];m=np.isin(a,anchors)|np.isin(b,anchors);nei=np.unique(np.r_[a[m],b[m]]);cand=list(anchors)+list(nei[np.argsort(wd[nei])[::-1]])+list(np.argsort(wd)[::-1]);sel=[];seen=set()
 for x in cand:
  x=int(x)
  if x not in seen:sel.append(x);seen.add(x)
  if len(sel)>=n:break
 sel=np.array(sel);loc=np.full(N,-1,np.int32);loc[sel]=np.arange(n);em=(loc[a]>=0)&(loc[b]>=0);pre=loc[a[em]];post=loc[b[em]];w=w0[em];o=np.argsort(pre,kind='stable');pre,post,w=pre[o],post[o],w[o];ptr=np.r_[0,np.cumsum(np.bincount(pre,minlength=n))].astype(np.int64);sens=loc[sens_idx];read=loc[desc_idx]
 rng=np.random.default_rng(seed);variants={'real':(post.copy(),w.copy()),'weight_shuffle':(post.copy(),rng.permutation(w)),'topology_shuffle':(rng.permutation(post),w.copy()),'zero':(post.copy(),np.zeros_like(w))}
 return {'n':n,'edges':len(w),'ptr':ptr,'sens':sens,'read':read,'variants':variants,'graph_bytes':int(post.nbytes+w.nbytes+ptr.nbytes),'input_n':len(sens),'output_n':len(read),'groups':groups}
class SNN:
 def __init__(self,G,name,seed=1):self.n=G['n'];self.ptr=G['ptr'];self.post,self.w=G['variants'][name];self.sens=G['sens'];self.read=G['read'];self.rng=np.random.default_rng(seed);self.reset()
 def reset(self):
  n=self.n;self.v=np.full(n,-52.,np.float32);self.g=np.zeros(n,np.float32);self.sp=np.zeros(n,np.uint8);self.rf=np.full(n,22,np.int16);self.rs=np.full(n,22,np.int16);self.rs[self.sens]=0;self.buf=np.zeros((19,n),np.float32);self.bi=0;self.events=0
 def window(self,rates,ms=20):
  cnt=np.zeros(len(self.read),np.int16);t0=time.perf_counter()
  for _ in range(int(ms/.1)):
   rec=np.zeros(self.n,np.float32)
   for i in np.flatnonzero(self.sp):
    s,e=self.ptr[i],self.ptr[i+1]
    if e>s:np.add.at(rec,self.post[s:e],self.w[s:e]);self.events+=int(e-s)
   rec*=.275;self.rf=np.where(self.sp,0,self.rf+1);gn=self.g*.98+self.buf[self.bi].copy()*(self.rf>=self.rs);self.buf[self.bi]=rec;self.bi=(self.bi+1)%19;fire=self.rng.random(len(self.sens))<rates*.0001;self.v[self.sens]+=.275*fire*250;self.v+=.005*(self.g-(self.v+52));ns=self.v>-45;self.v=np.where(ns,-52.,self.v);gn=np.where(ns,0.,gn);self.sp=ns.astype(np.uint8);cnt+=self.sp[self.read];self.g=gn
  return np.r_[cnt.astype(np.float32),self.v[self.read]+52.,self.g[self.read]].astype(np.float32),time.perf_counter()-t0
def encode(o):
 x=o.copy();x[0]=(x[0]+1)/2;x[5]=(x[5]+1)/2;x=np.clip(x,0,1);return np.repeat((10+190*x).astype(np.float32),16)
