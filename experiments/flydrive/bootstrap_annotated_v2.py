import os,requests,subprocess,sys
rev='815dc43b0fc56d93f3f78883327b4cc6c50eee6e'
base=f'https://raw.githubusercontent.com/obmakesomething/routezero/{rev}/experiments/flydrive/'
os.makedirs('/tmp/flydrive_ann2',exist_ok=True)
for f in ['fly_core_annotated.py','nav_env.py','experiment_annotated.py']:
 r=requests.get(base+f,timeout=60);r.raise_for_status();open('/tmp/flydrive_ann2/'+f,'wb').write(r.content)
subprocess.run([sys.executable,'/tmp/flydrive_ann2/experiment_annotated.py'],cwd='/tmp/flydrive_ann2',check=True)
