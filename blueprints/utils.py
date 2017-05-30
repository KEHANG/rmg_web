import os
import ConfigParser

from rmgpy.molecule import Molecule

def read_config(cfg_path='default'):
	'''This function reads a configuration file and returns an equivalent dictionary'''

	config_parser = ConfigParser.SafeConfigParser()
	config_parser.optionxform = str

	if cfg_path == 'default':
		cfg_path = os.path.join(os.path.dirname(__file__), 'config.cfg')
	with open(cfg_path, 'r') as fid:
		config_parser.readfp(fid)
	return config_parser._sections

def getTCDAuthenticationInfo():
	
	try:
		config = read_config()

		host = config['ThermoCentralDatabase']['TCD_HOST']
		port = int(config['ThermoCentralDatabase']['TCD_PORT'])
		username = config['ThermoCentralDatabase']['TCD_USER']
		password = config['ThermoCentralDatabase']['TCD_PW']

		return host, port, username, password
	except KeyError:
		print('Thermo Central Database Configuration File  Not Completely Set!')
 
	return 'None', 0, 'None', 'None'

def getPPDAuthenticationInfo():

	try:
		config = read_config()

		host = config['PredictorPerformanceDatabase']['PPD_HOST']
		port = int(config['PredictorPerformanceDatabase']['PPD_PORT'])
		username = config['PredictorPerformanceDatabase']['PPD_USER']
		password = config['PredictorPerformanceDatabase']['PPD_PW']

		return host, port, username, password
	except KeyError:
		print('Predictor Performance Database Authentication Environment Variables Not Completely Set!')
	
	return 'None', 0, 'None', 'None'

def connect_to_PPD():

	import pymongo

	host, port, username, password = getPPDAuthenticationInfo()
	remote_address = 'mongodb://{0}:{1}@{2}/admin'.format(username, 
														password,
														host)
	client = pymongo.MongoClient(remote_address, 
								port, 
								serverSelectionTimeoutMS=2000)
	try:
		client.server_info()
		print("\nConnection success to Predictor Performance Database!\n")
		return client
	
	except (pymongo.errors.ServerSelectionTimeoutError,
			pymongo.errors.OperationFailure):
		print("\nConnection failure to Predictor Performance Database...")
		print("Predictor Performance Page may fail.\n")
		return None

def draw_molecule_from_aug_inchi(aug_inchi, path):
    molecule = Molecule().fromAugmentedInChI(aug_inchi)
    path = os.path.join(path, '{0}.svg'.format(aug_inchi.replace('/', '_slash_')))
    if not os.path.exists(path):
        molecule.draw(path)