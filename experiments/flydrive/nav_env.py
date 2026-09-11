import numpy as np
class Nav:
 def __init__(self,seed=0,max_steps=100):self.rng=np.random.default_rng(seed);self.max_steps=max_steps
 def reset(self):
  r=self.rng;self.p=r.uniform(-.8,.8,2);self.goal=r.uniform(-.8,.8,2);self.h=r.uniform(-np.pi,np.pi);self.av=0.;self.t=0;self.obs=[]
  for _ in range(3):
   for _ in range(100):
    c=r.uniform(-.7,.7,2);rad=r.uniform(.10,.18)
    if np.linalg.norm(c-self.p)>rad+.3 and np.linalg.norm(c-self.goal)>rad+.25:self.obs.append((c,rad));break
  return self.observe()
 def ray(self,off):
  ang=self.h+off;best=0.
  for c,rad in self.obs:
   v=c-self.p;dist=np.linalg.norm(v)-rad;ad=np.arctan2(np.sin(np.arctan2(v[1],v[0])-ang),np.cos(np.arctan2(v[1],v[0])-ang))
   if abs(ad)<.65:best=max(best,max(0.,1-dist/.75)*(1-abs(ad)/.65))
  return min(1.,best)
 def observe(self):
  v=self.goal-self.p;dist=np.linalg.norm(v);bearing=np.arctan2(np.sin(np.arctan2(v[1],v[0])-self.h),np.cos(np.arctan2(v[1],v[0])-self.h))/np.pi
  return np.array([bearing,min(1.,dist/2.3),self.ray(.7),self.ray(0),self.ray(-.7),np.clip(self.av/.28,-1,1),1.],np.float32)
 def expert(self,o):
  b,_,l,f,r,_,_=o;s=b+1.4*(l-r)
  if f>.45:s=(-.8 if l<r else .8)
  return 0 if s<-.14 else (2 if s>.14 else 1)
 def step(self,a):
  self.av=(-.28,0,.28)[a];self.h+=self.av;spd=.045 if self.ray(0)<.65 else .06;self.p+=spd*np.array([np.cos(self.h),np.sin(self.h)]);self.t+=1
  hit=any(np.linalg.norm(self.p-c)<rad+.035 for c,rad in self.obs);goal=np.linalg.norm(self.p-self.goal)<.11;done=hit or goal or self.t>=self.max_steps;rew=(2. if goal else (-1. if hit else -.005));return self.observe(),rew,done,{'success':goal,'collision':hit}

def rates(o):
 x=o.copy();x[0]=(x[0]+1)/2;x[5]=(x[5]+1)/2;x=np.clip(x,0,1);return np.repeat(10+190*x,3).astype(np.float32)
def expert_episodes(seed,n):
 out=[]
 for k in range(n):
  e=Nav(seed*1000+k);o=e.reset();O=[];A=[]
  while True:
   a=e.expert(o);O.append(o);A.append(a);o,_,d,_=e.step(a)
   if d:break
  out.append((np.array(O),np.array(A)))
 return out
