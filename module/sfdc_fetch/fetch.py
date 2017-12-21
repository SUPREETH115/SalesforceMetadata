import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
import generate_package_xml
import subprocess
import file_processor
import json
from collections import OrderedDict


def fetch_():
	script_dir = os.path.dirname(os.path.abspath(__file__))
	package_xml_path=generate_package_xml.generate_package_xml__()
	subprocess.call(['java', '-jar', 'AntSF.jar','-f',os.path.join(script_dir,'../etc/ant_executor_config.json'),'-U','https://test.salesforce.com'])
	data = json.load(open(os.path.join(script_dir,'../etc/ant_executor_config.json')), object_pairs_hook=OrderedDict)
	sfdc_path=""
	git_path=""
	for task,login_detail in data.items():
		if (task == 'fetch'):
			for attribute in login_detail:
				sfdc_path=attribute['target']
	util_data = json.load(open(os.path.join(script_dir,'../etc/util_data.json')),object_pairs_hook=OrderedDict)
	git_path=util_data['git_path']
	file_processor.input_processor__(os.path.join(script_dir,'../etc/packagedata.json'),sfdc_path,git_path)
	os.remove("package.xml")



if __name__ == '__main__':
	fetch_()


