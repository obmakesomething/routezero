import requests,os,sys,numpy as np
base='https://raw.githubusercontent.com/obmakesomething/routezero/experiment/flydrive-0/experiments/flydrive/'
os.makedirs('/tmp/fda',exist_ok=True)
for f in ['fly_core_annotated.py']:
 r=requests.get(base+f,timeout=60);r.raise_for_status();open('/tmp/fda/'+f,'wb').write(r.content)
sys.path.insert(0,'/tmp/fda');from fly_core_annotated import load,SNN
G=load(4000,7,112,256);print('GRAPH',{'nodes':G['n'],'edges':G['edges'],'sensory_inputs':G['input_n'],'descending_outputs':G['output_n'],'graph_bytes':G['graph_bytes']},flush=True)
for name in ['real','weight_shuffle','topology_shuffle','zero']:
 s=SNN(G,name,7);r=np.full(G['input_n'],200.,np.float32);f,t=s.window(r,100);print('CAL',name,{'wall100ms':t,'events':s.events,'feature_nonzero':int((f!=0).sum()),'feature_dim':len(f),'read_spike_sum':int(f[:G['output_n']].sum()),'read_spike_nonzero':int((f[:G['output_n']]>0).sum()),'v_nonzero':int((np.abs(f[G['output_n']:2*G['output_n']])>1e-6).sum()),'g_nonzero':int((np.abs(f[2*G['output_n']:])>1e-6).sum())},flush=True)
