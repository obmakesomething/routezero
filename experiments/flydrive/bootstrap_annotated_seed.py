import os,requests,subprocess,sys
seed=sys.argv[1];rev='77761121def6057e04ee08a3f0e4dfe8708030a5';base=f'https://raw.githubusercontent.com/obmakesomething/routezero/{rev}/experiments/flydrive/';os.makedirs('/tmp/fdas',exist_ok=True)
for f in ['fly_core_annotated.py','nav_env.py','experiment_annotated_seed.py']:
 r=requests.get(base+f,timeout=60);r.raise_for_status();open('/tmp/fdas/'+f,'wb').write(r.content)
subprocess.run([sys.executable,'/tmp/fdas/experiment_annotated_seed.py',seed],cwd='/tmp/fdas',check=True)
