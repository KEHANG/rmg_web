import datetime
from bson.son import SON
from flask import Blueprint, render_template

from rmgpy.data.thermoTest import getTCDAuthenticationInfo
from rmgpy.data.thermo import ThermoCentralDatabaseInterface

from blueprints.utils import draw_molecule_from_aug_inchi

thermo_central_db = Blueprint('thermo_central_db', __name__,
                        	template_folder='templates',
                        	static_folder='./static',
                            static_url_path='/blueprints/thermo_central_db/static')

# thermo central database setup
host, port, username, password = getTCDAuthenticationInfo()
application = 'rmg_web'
tcdi = ThermoCentralDatabaseInterface(host, port, username, password, application)

# get total registered molecule count
thermoCentralDB =  getattr(tcdi.client, 'thermoCentralDB')
registration_table = getattr(thermoCentralDB, 'registration_table')
saturated_ringcore_table = getattr(thermoCentralDB, 'saturated_ringcore_table')

@thermo_central_db.route('/')
def dashboard():
    
    total_mol_count = registration_table.count()

    # get a dict of molecules with count
    aggreg_pipeline=[{"$group": {"_id": "$radical_number", "count": {"$sum": 1}}},
                    {"$sort": SON([("count", -1)])}]
    radical_count_list = []
    for record in registration_table.aggregate(aggreg_pipeline):
        radical = record['_id']
        count = record['count']
        radical_count_list.append((radical, count))

    # get a dict of users with count
    aggreg_pipeline=[{"$group": {"_id": "$user", "count": {"$sum": 1}}},
                    {"$sort": SON([("count", -1)])}]
    user_count_list = []
    for record in registration_table.aggregate(aggreg_pipeline):
        user = record['_id']
        count = record['count']
        user_count_list.append((user, count))

    # get a dict of applications with count
    aggreg_pipeline=[{"$group": {"_id": "$application", "count": {"$sum": 1}}},
                    {"$sort": SON([("count", -1)])}]
    application_count_list = []
    for record in registration_table.aggregate(aggreg_pipeline):
        application = record['_id']
        count = record['count']
        application_count_list.append((application, count))

    # get analysis result
    total_ringcore_count = saturated_ringcore_table.count()
    top_ringcore_counts = list(saturated_ringcore_table.find().sort([('count', -1)]).limit(4))
    ringcore_count_list = []
    for ringcore_count in top_ringcore_counts:
        ringcore = str(ringcore_count['aug_inchi'])
        draw_molecule_from_aug_inchi(ringcore, thermo_central_db.static_folder + '/img')
        count = ringcore_count['count']
        timestamp = ringcore_count['timestamp']
        ringcore_count_list.append((ringcore, count, timestamp))

    # user-application stats
    aggreg_pipeline=[{"$group": 
                   {"_id": 
                        {"application":"$application",
                        "user":"$user"}, 
                    "count": 
                        {"$sum": 1}
                   }
              },
             {"$sort": SON([("count", -1)])}]
    user_application_count_list = []
    for record in registration_table.aggregate(aggreg_pipeline):
        application = record['_id']['application']
        user = record['_id']['user']
        count = record['count']
        user_application_count_list.append((user, application, count))

    return render_template('thermo_central_db.html', 
                            total_mol_count=total_mol_count, 
                            total_ringcore_count=total_ringcore_count,
                            radical_count_list=radical_count_list,
                            user_count_list=user_count_list,
                            application_count_list=application_count_list,
                            ringcore_count_list=ringcore_count_list,
                            user_application_count_list=user_application_count_list,
                            time=datetime.datetime.fromtimestamp(int(timestamp)).strftime('%d/%m/%Y: %H:%M:%S'))