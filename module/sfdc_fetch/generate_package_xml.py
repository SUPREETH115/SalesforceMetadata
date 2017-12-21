import os
import xml.etree.ElementTree as ET
import xml.dom.minidom
import json
from collections import OrderedDict

def generate_package_xml__():
	script_dir = os.path.dirname(os.path.abspath(__file__))
	data = json.load(open(os.path.join(script_dir,'../etc/packagedata.json')), object_pairs_hook=OrderedDict)
	util_data = json.load(open(os.path.join(script_dir,'../etc/util_data.json')), object_pairs_hook=OrderedDict)
	root = ET.Element("Package",xmlns=util_data['name_space'])
	for id,hash_ in data.items():
		doc = ET.SubElement(root, "types")
		for key,val in hash_.items():
		 print key
		 if (key == 'name'):
		 	print(key,":",val)
		 	ET.SubElement(doc, "name").text=val
		 else:
		 	for member in val:
		 		print(key,":",member)
		 		ET.SubElement(doc, "members").text=member
	doc = ET.SubElement(root, "version").text=xmlns=util_data['version']
	xmlstr = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ",encoding='UTF-8',)
	with open("package.xml", "w") as f:
		f.write(xmlstr)
	return os.path.abspath('package.xml')


