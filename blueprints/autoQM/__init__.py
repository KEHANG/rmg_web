import time
import datetime
from flask import Blueprint, render_template

from rmgpy.data.thermoTest import getTCDAuthenticationInfo
from rmgpy.data.thermo import ThermoCentralDatabaseInterface
from blueprints.utils import draw_molecule_from_aug_inchi

autoQM = Blueprint('autoQM', __name__,
					template_folder='templates',
					static_folder='./static',
					static_url_path='/blueprints/autoQM/static')

# connect to related tables
host, port, username, password = getTCDAuthenticationInfo()
application = 'rmg_web'
tcdi = ThermoCentralDatabaseInterface(host, port, username, password, application)

thermoCentralDB =  getattr(tcdi.client, 'thermoCentralDB')
saturated_ringcore_table = getattr(thermoCentralDB, 'saturated_ringcore_table')
saturated_ringcore_status_table = getattr(thermoCentralDB, 'saturated_ringcore_status_table')

@autoQM.route('/')
def dashboard():
	current_time = time.time()
	query = {"timestamp":
					{
					"$gte": current_time - 3600*24*7, # one week back
					"$lt": current_time
					}
			}
	status_res = list(saturated_ringcore_status_table.find(query))

	# analysis for the latest status
	pending = status_res[-1]['pending']
	success = status_res[-1]['job_success']
	failed_convergence = status_res[-1]['job_failed_convergence']
	failed_isomorphism = status_res[-1]['job_failed_isomorphism']
	created = status_res[-1]['job_created']
	launched = status_res[-1]['job_launched']
	running = status_res[-1]['job_running']
	aborted = status_res[-1]['job_aborted']
	off_queue = success + failed_convergence + failed_isomorphism + aborted
	on_queue = created + launched + running

	timestamp = status_res[-1]['timestamp']
	time_date = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%d/%m/%Y: %H:%M:%S')

	molecule_samples = get_molecule_samples(status='pending')

	return render_template('autoQM.html', 
							off_queue=off_queue,
							on_queue=on_queue,
							pending=pending,
							launched=launched,
							running=running,
							created=created,
							success=success,
							failed_isomorphism=failed_isomorphism,
							failed_convergence=failed_convergence,
							time=time_date,
							molecule_samples=molecule_samples)

def get_molecule_samples(status, limit=3):

	query = {"status":status}
	sort_key = [('count', -1)]
	top_ringcore_counts = list(saturated_ringcore_table.find(query).sort(sort_key).limit(limit))
	ringcore_count_list = []
	for ringcore_count in top_ringcore_counts:
		ringcore = str(ringcore_count['aug_inchi'])
		draw_molecule_from_aug_inchi(ringcore, autoQM.static_folder + '/img')
		count = ringcore_count['count']
		ringcore_count_list.append((ringcore, count))

	return ringcore_count_list

