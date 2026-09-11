import json,time,numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from fly_core import load,SNN
from nav_env import Nav,rates,expert_episodes
SEED=7;WIN=20
G=load(4000,SEED);train=expert_episodes(SEED,18);val=expert_episodes(SEED+1,6)

def features(name,eps,seed):
 X=[];Y=[];wall=0.;events=0
 for j,(oo,aa) in enumerate(eps):
  s=SNN(G,name,seed+j);before=s.events
  for o,a in zip(oo,aa):
   f,t=s.window(rates(o),WIN);X.append(f);Y.append(a);wall+=t
  events+=s.events-before
 return np.array(X),np.array(Y),wall,events

def eval_closed(model,name,seeds):
 suc=col=steps=0;rew=wall=events=0.;n=0
 for sd in seeds:
  e=Nav(sd);o=e.reset();s=SNN(G,name,sd);ev0=s.events
  while True:
   f,t=s.window(rates(o),WIN);wall+=t;a=int(model.predict(f[None])[0]);o,r,d,info=e.step(a);rew+=r;steps+=1
   if d:suc+=int(info['success']);col+=int(info['collision']);break
  events+=s.events-ev0;n+=1
 return {'success':suc/n,'collision':col/n,'reward':rew/n,'steps':steps/n,'eval_wall_s':wall,'eval_syn_events':int(events),'synops_action':events/max(1,steps),'wall_ms_action':1000*wall/max(1,steps)}
res=[]
for name in ['real','weight_shuffle','topology_shuffle','zero']:
 X,y,wall,events=features(name,train,SEED);XV,yv,vwall,ve=features(name,val,SEED+99)
 m=make_pipeline(StandardScaler(),LogisticRegression(max_iter=300,class_weight='balanced'));t=time.perf_counter();m.fit(X,y);fit=time.perf_counter()-t;acc=accuracy_score(yv,m.predict(XV));cl=eval_closed(m,name,range(900,910));row={'model':name,'val_acc':acc,'train_samples':len(y),'feature_dim':X.shape[1],'train_sim_wall_s':wall,'fit_wall_s':fit,'train_syn_events':int(events),'synops_train_sample':events/len(y),'sim_realtime_ratio':wall/(len(y)*WIN/1000),'graph_bytes':G['graph_bytes'],'decoder_params':X.shape[1]*3+3,**cl};res.append(row);print('ROW',json.dumps(row),flush=True)
XO=np.concatenate([x for x,_ in train]);yo=np.concatenate([y for _,y in train]);XOV=np.concatenate([x for x,_ in val]);yov=np.concatenate([y for _,y in val])
for name,m in [('linear',make_pipeline(StandardScaler(),LogisticRegression(max_iter=300,class_weight='balanced'))),('mlp',make_pipeline(StandardScaler(),MLPClassifier(hidden_layer_sizes=(32,32),max_iter=300,random_state=SEED)))]:
 t=time.perf_counter();m.fit(XO,yo);fit=time.perf_counter()-t;acc=accuracy_score(yov,m.predict(XOV));suc=col=steps=0;rew=0.
 for sd in range(900,910):
  e=Nav(sd);o=e.reset()
  while True:
   a=int(m.predict(o[None])[0]);o,r,d,info=e.step(a);rew+=r;steps+=1
   if d:suc+=int(info['success']);col+=int(info['collision']);break
 params=(7*3+3 if name=='linear' else 7*32+32+32*32+32+32*3+3);row={'model':name,'val_acc':acc,'train_samples':len(yo),'feature_dim':7,'fit_wall_s':fit,'decoder_params':params,'success':suc/10,'collision':col/10,'reward':rew/10,'steps':steps/10};res.append(row);print('ROW',json.dumps(row),flush=True)
print('META',json.dumps({'nodes':G['n'],'edges':G['edges'],'readout':len(G['read']),'window_ms':WIN,'naive_edge_ops_action':G['edges']*int(WIN/.1),'compressed_graph_est_bytes':G['edges']*6+(G['n']+1)*4}),flush=True)
print('RESULTS_JSON',json.dumps(res),flush=True)
