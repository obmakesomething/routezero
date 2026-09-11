import os,requests,subprocess,sys
base='https://raw.githubusercontent.com/obmakesomething/routezero/experiment/flydrive-0/experiments/flydrive/'
os.makedirs('/tmp/flydrive_ann',exist_ok=True)
for f in ['fly_core_annotated.py','nav_env.py','experiment_annotated.py']:
 r=requests.get(base+f,timeout=60);r.raise_for_status();open('/tmp/flydrive_ann/'+f,'wb').write(r.content)
subprocess.run([sys.executable,'/tmp/flydrive_ann/experiment_annotated.py'],cwd='/tmp/flydrive_ann',check=True)
