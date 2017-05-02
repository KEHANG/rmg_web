import os

def getPPDAuthenticationInfo():

	try:
		host = os.environ['PPD_HOST']
		port = int(os.environ['PPD_PORT'])
		username = os.environ['PPD_USER']
		password = os.environ['PPD_PW']
	except KeyError:
		print('Predictor Performance Database Authentication Environment Variables Not Completely Set!')
		return 'None', 0, 'None', 'None'

	return host, port, username, password

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