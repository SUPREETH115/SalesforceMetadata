from lxml import etree
import xml.dom.minidom
from shutil import copy
import os
import json
import ntpath
from collections import OrderedDict

def remove_namespace(doc, namespace):
    """Remove namespace in the passed document in place."""
    ns = u'{%s}' % namespace
    nsl = len(ns)
    for elem in doc.getiterator():
        if elem.tag.startswith(ns):
            elem.tag = elem.tag[nsl:]

def getNameOfField(field):
	fullName = field.find("fullName")
	return fullName.text

def checkForExistingField(field,git_tree) :

	git_field_list=None
	git_last_field=None
	fieldname=getNameOfField(field)
	path="//fields[fullName='"+fieldname+"']"
	field_list =git_tree.xpath(path)
	if(field_list):
		field_list = field_list[0]
	if(len(field_list)!=0) :
			prevfield=field_list.getprevious()
			if(prevfield!=None) :
				field_list.getparent().remove(field_list)
				prevfield.addnext(field)
				print "PrevElement => ",prevfield.find('fullName').text
			else :
				parentfield=field_list.getparent()
				field_list.getparent().remove(field_list)
				parentfield.insert(0,field)	
	else :
		git_field_list=git_tree.findall("//fields")
		if(git_field_list):
			git_last_field = git_field_list[len(git_field_list)-1]
			print "PrevElement => ",git_last_field.find('fullName').text
			git_last_field.addnext(field)
		else :
			git_parent_field=git_tree.getroot()
			print "ParentElement => ",git_parent_field.tag
			git_parent_field.insert(0,field)

def CustomObjectParser_(sfdc_path,git_path):
	script_dir = os.path.dirname(os.path.abspath(__file__))
	util_data = json.load(open(os.path.join(script_dir,'../etc/util_data.json')),object_pairs_hook=OrderedDict)
	sfdc_tree = etree.parse(sfdc_path)
	print git_path
	print ntpath.basename(git_path)
	git_tree = etree.parse(git_path)
	#sfdc_tree = etree.parse('/Users/supreets/SalesforceMetadata/module/data/sfdc/objects/PageLayoutChangeRequest__c.object')
	#git_tree = etree.parse('/Users/supreets/SalesforceMetadata/module/data/git/objects/PageLayoutChangeRequest__c.object')
	remove_namespace(sfdc_tree,util_data['name_space'])
	remove_namespace(git_tree,util_data['name_space'])

	sfdc_field_list = sfdc_tree.findall("//fields")
	for field in sfdc_field_list :
		print "Field => ",field.find('fullName').text
		checkForExistingField(field,git_tree)
	sh=git_tree.getroot()
	#sh.set('xmlns','http://soap.sforce.com/2006/04/metadata')
	xmlstr = etree.tostring(git_tree, pretty_print=True,encoding='UTF-8',xml_declaration=True,)
	with open(os.path.join(script_dir,'../'+ntpath.basename(git_path)), "w") as f:
		f.write(xmlstr)
	copy(os.path.join(script_dir,'../'+ntpath.basename(git_path)),git_path)
	os.remove(os.path.join(script_dir,'../'+ntpath.basename(git_path)))
	    #cprint etree.tostring(git_tree, pretty_print=True)
	    #xmlstr = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ",encoding='UTF-8',)

