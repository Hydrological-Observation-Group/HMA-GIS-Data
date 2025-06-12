#!/usr/bin/python3
# -*- coding: utf-8 -*-
''' Version: 2.0 '''
''' Author: Christian Schwatke <christian.schwatke@tum.de>'''
''' Last change: 2024-01-10 '''

import os
import sys
import json
import pprint
import requests
import datetime

''' Download path were all water level time series will be stored '''
download_path = 'downloads/'
if not os.path.isdir(download_path):
	os.mkdir(download_path)

API_KEY = '###API_KEY###'
OUTPUT_FORMAT = 'ascii'
#~ OUTPUT_FORMAT = 'json'
#~ OUTPUT_FORMAT = 'netcdf'
#~ OUTPUT_FORMAT = 'csv'

url = 'https://dahiti.dgfi.tum.de/api/v2/list-targets/'
args = {}
''' User configuration '''
args['api_key'] = API_KEY
''' Search options '''
args['basin'] = 'Amazon'
#args['continent'] = 'Asia'
#args['country'] = 'de'
#args['min_lon'] = 0
#args['max_lon'] = 10
#args['min_lat'] = 0
#args['max_lat'] = 10


''' send request as method POST '''
response = requests.post(url, data=args)
if response.status_code == 200:
	''' convert json string in python list '''
	targets = json.loads(response.text)['data']
	print ('Dataset(s) found:',len(targets))		

	for target in targets:
		print (target)		

		''' download water level time series '''
		url = 'https://dahiti.dgfi.tum.de/api/v2/download-water-level/'
		args = {}
		args['api_key'] = API_KEY
		args['dahiti_id'] = target['dahiti_id']
		args['format'] = OUTPUT_FORMAT
		
		if args['format'] == "ascii":
			path_output = os.path.abspath(download_path+'/'+str(target['dahiti_id'])+'.txt')
		elif args['format'] == "json":
			path_output = os.path.abspath(download_path+'/'+str(target['dahiti_id'])+'.json')
		elif args['format'] == "netcdf":
			path_output = os.path.abspath(download_path+'/'+str(target['dahiti_id'])+'.nc')
		elif args['format'] == "csv":
			path_output = os.path.abspath(download_path+'/'+str(target['dahiti_id'])+'.csv')
		else:
			print ('Invalid format `'+format+'`')
			sys.exit(0)

		print ('Downloading ... ',target['dahiti_id'],'->',target['target_name'].encode("utf8"),'('+path_output+')')
		
		response_download = requests.post(url, json=args)
		if response_download.status_code == 200:
			if args['format'] == "ascii":
				data_ascii = response_download.text
				output = open(path_output,'w')
				output.write(data_ascii)
				output.close()
			if args['format'] == "json":
				data_json = response_download.text
				output = open(path_output,'w')
				output.write(data_json)
				output.close()
			if args['format'] == "netcdf":				
				with open(path_output, 'wb') as f:
					for chunk in response_download.iter_content(chunk_size=1024): 
						if chunk:
							f.write(chunk)
			if args['format'] == "csv":
				data_csv = response_download.text
				output = open(path_output,'w')
				output.write(data_csv)
				output.close()						
		else:
			print ('Error: `download-water-level` request failed!')
			data = json.loads(response_download.text)
			pprint.pprint(data)
			sys.exit(0)
else:
	print ('Error: `list-targets` request failed!')
	data = json.loads(response.text)
	pprint.pprint(data)