# !/usr/bin/python
import os
import sys
sys.path.append('/Users/supreets/SalesforceMetadata/module')
import json
from collections import OrderedDict
from shutil import copy
import sfdc_parsing


data = json.load(open('/Users/supreets/SalesforceMetadata/module/sfdc_fetch/packagedata.json'), object_pairs_hook=OrderedDict)
parse_required_component_map=json.load(open('/Users/supreets/SalesforceMetadata/module/etc/ComponentRequiringParsing.json'), object_pairs_hook=OrderedDict)
parse_required_directory_map=json.load(open('/Users/supreets/SalesforceMetadata/module/etc/DirectoryRequiringParsing.json'), object_pairs_hook=OrderedDict)
folder_component_type_map = json.load(open('/Users/supreets/SalesforceMetadata/module/etc/FolderComponentMapping.json'), object_pairs_hook=OrderedDict)
extension_map= json.load(open('/Users/supreets/SalesforceMetadata/module/etc/ExtensionComponentMapping.json'), object_pairs_hook=OrderedDict)

sfdc_base="/Users/supreets/SalesforceMetadata/module/ant_output"
#git_base="/Users/supreets/python-test"
git_base="/Users/supreets/SalesforceMetadata/git_output"
component_type_map={}
parse_req_comp={}
parse_non_req_comp={}
type_=[]

for id,hash_ in data.items():
	for key,val in hash_.items():
		if (key == 'name'):
			value=val
		if (key == 'members'):
			for members in val:
				type_.append(members)
	for each_comp in type_:
		component_type_map[each_comp]=value
		type_=[]

for comp,type_ in component_type_map.items():
	if (type_=="CustomField"):
		component_type_map[comp.split('.')[0]]=type_
		del component_type_map[comp]

print component_type_map

for root, dirs, files in os.walk(sfdc_base, topdown=False):
	for name in files:
		file_path=os.path.join(root, name)
		directory=os.path.basename(root)
		print "Name:",file_path
		print "Directory",directory
		if ( not(directory in parse_required_directory_map.values()) or not(component_type_map[name.split('.')[0]] in parse_required_component_map.values())):
			dest_path=git_base+"/"+directory
			print "just copy "+file_path+" to "+dest_path
			if not os.path.exists(dest_path):
			 os.makedirs(dest_path)
			copy(file_path,dest_path)
		else:
			print "require parsing of", component_type_map[name.split('.')[0]]
			dest_file=git_base+"/"+directory+"/"+name
			if(os.path.exists(dest_file)):
				if(component_type_map[name.split('.')[0]] == "CustomField"):
					sfdc_parsing.CustomObjectParser_(file_path,dest_file)
			else:
				print "Parsing failed:File Not found",dest_file






        




