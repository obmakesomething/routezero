import sys,json,time,numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from fly_core_modal import load,SNN,encode
from nav_env import Nav,expert_episodes
SEED=int(sys.argv[1]);WIN=20;G=load(4000,SEED);tr=expert_episodes(SEED,60);va=expert_episodes(SEED+100,20);XO=np.concatenate([x for x,_ in tr]);yo=np.concatenate([y for _,y in tr]);XOV=np.concatenate([x for x,_ in va]);yov=np.concatenate([y for _,y in va]);ALL=[]
def feats(name,eps,seed):
 X=[];Y=[];wall=0.;events=0
 for j,(oo,aa) in enumerate(eps):
  s=SNN(G,name,seed+j);ev=s.events
  for o,a in zip(oo,aa):f,t=s.window(encode(o),WIN);X.append(f);Y.append(a);wall+=t
  events+=s.events-ev
 return np.array(X),np.array(Y),wall,events
def closed(m,name):
 suc=col=steps=0;rew=wall=events=0.
 for sd in range(30000+SEED*10,30030+SEED*10):
  e=Nav(sd);o=e.reset();s=SNN(G,name,sd);ev=s.events
  while 1:
   f,t=s.window(encode(o),WIN);wall+=t;a=int(m.predict(f[None])[0]);o,r,d,z=e.step(a);rew+=r;steps+=1
   if d:suc+=int(z['success']);col+=int(z['collision']);break
  events+=s.events-ev
 return dict(success=suc/30,collision=col/30,reward=rew/30,steps=steps/30,wall_ms_action=1000*wall/steps,synops_action=events/steps)
for name in ['real','weight_shuffle','topology_shuffle','zero']:
 X,y,wall,events=feats(name,tr,SEED);XV,yv,_,_=feats(name,va,SEED+500);m=make_pipeline(StandardScaler(),LogisticRegression(max_iter=250,class_weight='balanced'));t=time.perf_counter();m.fit(X,y);fit=time.perf_counter()-t;row={'seed':SEED,'model':name,'val_acc':accuracy_score(yv,m.predict(XV)),'train_n':len(y),'input_n':G['input_n'],'output_n':G['output_n'],'edges':G['edges'],'graph_bytes':G['graph_bytes'],'decoder_params':X.shape[1]*3+3,'train_wall':wall,'fit_wall':fit,'synops_train_sample':events/len(y),**closed(m,name)};ALL.append(row);print('ROW',json.dumps(row),flush=True)
for name,m in [('linear',make_pipeline(StandardScaler(),LogisticRegression(max_iter=250,class_weight='balanced'))),('mlp',make_pipeline(StandardScaler(),MLPClassifier(hidden_layer_sizes=(32,32),max_iter=400,random_state=SEED)))]:
 t=time.perf_counter();m.fit(XO,yo);fit=time.perf_counter()-t;suc=col=steps=0;rew=0.
 for sd in range(30000+SEED*10,30030+SEED*10):
  e=Nav(sd);o=e.reset()
  while 1:
   a=int(m.predict(o[None])[0]);o,r,d,z=e.step(a);rew+=r;steps+=1
   if d:suc+=int(z['success']);col+=int(z['collision']);break
 row={'seed':SEED,'model':name,'val_acc':accuracy_score(yov,m.predict(XOV)),'train_n':len(yo),'decoder_params':24 if name=='linear' else 1411,'fit_wall':fit,'success':suc/30,'collision':col/30,'reward':rew/30,'steps':steps/30};ALL.append(row);print('ROW',json.dumps(row),flush=True)
print('META',json.dumps({'nodes':G['n'],'edges':G['edges'],'sensory_inputs':G['input_n'],'descending_outputs':G['output_n'],'window_ms':WIN}),flush=True);print('RESULTS_JSON',json.dumps(ALL),flush=True)
