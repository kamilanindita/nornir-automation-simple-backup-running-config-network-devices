from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import napalm_get
from datetime import datetime

def filename(hostname):
    now = datetime.now()
    date_time = now.strftime("%H:%M:%S_%m:%d:%Y")
    name='backup_'+hostname+'_'+ str(date_time) +'.txt'
    return name

nr = InitNornir(
        config_file="config.yaml", dry_run=True
)

results = nr.run(
        task=napalm_get, getters=['facts', 'config']
)

for host,  p in results.items():
	print(host +' --> '+ p.result['facts']['hostname'])
	print('Backup running configuration...')
	output = p.result['config']['running']
	SAVE_FILE = open(filename(p.result['facts']['hostname']), 'w')
	SAVE_FILE.write(output)
	SAVE_FILE.close()
	print('Successfully backed up the running config.')
