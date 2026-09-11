import os,time,requests,pandas as pd,numpy as np,resource
u='https://raw.githubusercontent.com/eonsystemspbc/fly-brain/main/data/2025_Connectivity_783.parquet';p='/tmp/full.parquet'
r=requests.get(u,timeout=180);r.raise_for_status();open(p,'wb').write(r.content)
d=pd.read_parquet(p,columns=['Presynaptic_Index','Postsynaptic_Index','Excitatory x Connectivity']);a=d.Presynaptic_Index.to_numpy(np.int32,copy=True);post=d.Postsynaptic_Index.to_numpy(np.int32,copy=True);w=d['Excitatory x Connectivity'].to_numpy(np.float32,copy=True);N=max(int(a.max()),int(post.max()))+1;E=len(w);del d
ptr=np.r_[0,np.cumsum(np.bincount(a,minlength=N),dtype=np.int64)];del a
sens=np.array([69093,97602,122795,124291,29281,100605,110469,51107,49584,129730,126873,28825,126600,126752,32863,108426,111357,14842,90589,92298,12494],np.int32)
rng=np.random.default_rng(7);v=np.full(N,-52.,np.float32);g=np.zeros(N,np.float32);sp=np.zeros(N,np.uint8);rf=np.full(N,22,np.int16);rs=np.full(N,22,np.int16);rs[sens]=0;buf=np.zeros((19,N),np.float32);bi=0;cnt=np.zeros(N,np.int32);events=0;t0=time.perf_counter()
for _ in range(1000):
 rec=np.zeros(N,np.float32)
 for i in np.flatnonzero(sp):
  s,e=ptr[i],ptr[i+1]
  if e>s:np.add.at(rec,post[s:e],w[s:e]);events+=int(e-s)
 rec*=.275;rf=np.where(sp,0,rf+1);gn=g*.98+buf[bi].copy()*(rf>=rs);buf[bi]=rec;bi=(bi+1)%19;fire=rng.random(len(sens))<.02;v[sens]+=.275*fire*250;v+=.005*(g-(v+52));ns=v>-45;v=np.where(ns,-52.,v);gn=np.where(ns,0.,gn);sp=ns.astype(np.uint8);cnt+=sp;g=gn
wall=time.perf_counter()-t0;graph_bytes=post.nbytes+w.nbytes+ptr.nbytes;state_bytes=v.nbytes+g.nbytes+sp.nbytes+rf.nbytes+rs.nbytes+buf.nbytes+cnt.nbytes
print('FULL',{'neurons':N,'edges':E,'wall_100ms_s':wall,'realtime_ratio':wall/.1,'total_spikes':int(cnt.sum()),'active_neurons':int((cnt>0).sum()),'syn_events':events,'synops_per_bio_s':events*10,'naive_edge_ops_100ms':E*1000,'edge_visit_reduction':(E*1000/max(1,events)),'graph_bytes_runtime':graph_bytes,'graph_bytes_compressed_est':E*6+(N+1)*4,'state_bytes':state_bytes,'peak_rss_kb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},flush=True)
