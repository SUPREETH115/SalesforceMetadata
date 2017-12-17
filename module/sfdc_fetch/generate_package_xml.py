import xml.etree.ElementTree as ET
import xml.dom.minidom
import json
from collections import OrderedDict

data = json.load(open('packagedata.json'), object_pairs_hook=OrderedDict)
root = ET.Element("Package",xmlns="http://soap.sforce.com/2006/04/metadata")
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
doc = ET.SubElement(root, "version").text="40.0"
xmlstr = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ",encoding='UTF-8',)
with open("package.xml", "w") as f:
    f.write(xmlstr)


