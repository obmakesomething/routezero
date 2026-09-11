import os,requests,subprocess,sys
base='https://raw.githubusercontent.com/obmakesomething/routezero/experiment/flydrive-0/experiments/flydrive/'
os.makedirs('/tmp/flydrive',exist_ok=True)
for f in ['fly_core.py','nav_env.py','experiment_multiseed.py']:
 r=requests.get(base+f,timeout=60);r.raise_for_status();open('/tmp/flydrive/'+f,'wb').write(r.content)
subprocess.run([sys.executable,'/tmp/flydrive/experiment_multiseed.py'],cwd='/tmp/flydrive',check=True)
