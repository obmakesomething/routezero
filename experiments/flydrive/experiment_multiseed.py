import json,time,numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from fly_core import load,SNN
from nav_env import Nav,rates,expert_episodes
WIN=20;ALL=[]
def feats(G,name,eps,seed):
 X=[];Y=[];wall=0.;events=0
 for j,(oo,aa) in enumerate(eps):
  s=SNN(G,name,seed+j);ev=s.events
  for o,a in zip(oo,aa):f,t=s.window(rates(o),WIN);X.append(f);Y.append(a);wall+=t
  events+=s.events-ev
 return np.array(X),np.array(Y),wall,events
def closed(G,m,name,seeds):
 suc=col=steps=0;rew=wall=events=0.
 for sd in seeds:
  e=Nav(sd);o=e.reset();s=SNN(G,name,sd);ev=s.events
  while 1:
   f,t=s.window(rates(o),WIN);wall+=t;a=int(m.predict(f[None])[0]);o,r,d,z=e.step(a);rew+=r;steps+=1
   if d:suc+=z['success'];col+=z['collision'];break
  events+=s.events-ev
 n=len(seeds);return dict(success=suc/n,collision=col/n,reward=rew/n,steps=steps/n,wall_ms_action=1000*wall/steps,synops_action=events/steps)
for SEED in [7,17,27]:
 G=load(4000,SEED);tr=expert_episodes(SEED,80);va=expert_episodes(SEED+100,25);XO=np.concatenate([x for x,_ in tr]);yo=np.concatenate([y for _,y in tr]);XOV=np.concatenate([x for x,_ in va]);yov=np.concatenate([y for _,y in va])
 for name in ['real','weight_shuffle','topology_shuffle','zero']:
  X,y,wall,events=feats(G,name,tr,SEED);XV,yv,_,_=feats(G,name,va,SEED+500);m=make_pipeline(StandardScaler(),LogisticRegression(max_iter=400,class_weight='balanced'));t=time.perf_counter();m.fit(X,y);fit=time.perf_counter()-t
  row={'seed':SEED,'model':name,'val_acc':accuracy_score(yv,m.predict(XV)),'train_n':len(y),'train_wall':wall,'fit_wall':fit,'synops_train_sample':events/len(y),'graph_bytes':G['graph_bytes'],'decoder_params':X.shape[1]*3+3,**closed(G,m,name,range(10000+SEED*10,10030+SEED*10))};ALL.append(row);print('ROW',json.dumps(row),flush=True)
 for name,m in [('linear',make_pipeline(StandardScaler(),LogisticRegression(max_iter=400,class_weight='balanced'))),('mlp',make_pipeline(StandardScaler(),MLPClassifier(hidden_layer_sizes=(32,32),max_iter=500,random_state=SEED)))]:
  t=time.perf_counter();m.fit(XO,yo);fit=time.perf_counter()-t;suc=col=steps=0;rew=0.
  for sd in range(10000+SEED*10,10030+SEED*10):
   e=Nav(sd);o=e.reset()
   while 1:
    a=int(m.predict(o[None])[0]);o,r,d,z=e.step(a);rew+=r;steps+=1
    if d:suc+=z['success'];col+=z['collision'];break
  p=24 if name=='linear' else 1411;row={'seed':SEED,'model':name,'val_acc':accuracy_score(yov,m.predict(XOV)),'train_n':len(yo),'fit_wall':fit,'decoder_params':p,'success':suc/30,'collision':col/30,'reward':rew/30,'steps':steps/30};ALL.append(row);print('ROW',json.dumps(row),flush=True)
print('META',json.dumps({'nodes':4000,'edges':G['edges'],'readout':len(G['read']),'window_ms':WIN,'naive_edge_ops_action':G['edges']*200,'compressed_graph_est_bytes':G['edges']*6+(G['n']+1)*4}),flush=True)
for model in ['real','weight_shuffle','topology_shuffle','zero','linear','mlp']:
 q=[x for x in ALL if x['model']==model];print('AGG',json.dumps({'model':model,**{k:float(np.mean([x[k] for x in q])) for k in ['val_acc','success','collision','reward','steps']}}),flush=True)
print('RESULTS_JSON',json.dumps(ALL),flush=True)
