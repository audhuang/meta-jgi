from __future__ import print_function
from __future__ import division
import math
import random
import time
import sys
import getpass

import numpy as np 
# import matplotlib.pyplot as plt
import pandas as pd

import xml.etree.ElementTree as ET 
import subprocess
import os
from os import listdir
from os.path import isfile, join 
import tarfile
import requests
from collections import Counter 
import pprint

 
# start_time = time.time()
# elapsed_time = time.time() - start_time

#===============================================================================
# Analyze Files
#===============================================================================

def analyze_projects(project_list): 
	'''
	Input: 
	  csv file of list of all projects
	Output:
	  prints number of each type of product
	  (examples include standard draft, minimal draft, metatranscriptome)

	Comments: 

	'''
	df = pd.read_csv(project_list)
	saved_column = df['Product Name']
	project_count_dic = dict(Counter(list(saved_column)))
	
	pp = pprint.PrettyPrinter(indent=4)
	pp.pprint(project_count_dic)
	pp.pprint(project_count_dic.items())


#===============================================================================
# Automatically Download Projects
#===============================================================================

def sign_in(): 
	'''
	Input: 
	  
	Output:
	  
	Comments: 
	  takes user input of JGI login information and logs in to JGI

	'''
	print('Signing in. ')
	user = raw_input('Enter user: ')
	password = getpass.getpass()

	command = 'curl "https://signon.jgi.doe.gov/signon/create" --data-urlencode \
	 "login=' + user + '" --data-urlencode "password=' + password + \
	 '" -c \cookies > /dev/null'

	flag = subprocess.call(command, shell=True)
	if flag == 1: 
		print('Error logging in. ')
		sys.exit()

def get_projects(project_list): 
	'''
	Input: 
	  a csv file of projects downloaded from the JGI database 
	Output:
	  a list of portal ID strings 

	Comments: 
	  right now only annotated or minimal drafts
	  check that file exists? 

	'''
	projects = []
	
	df = pd.read_csv(project_list)
	portal_ids = df['Portal ID'].apply(str)

	i = 0
	for portal in df['Product Name']: 
		if 'Draft' in portal: 
			projects.append(portal_ids[i].split(',')[1][1:-2])
		i += 1
	
	return projects

def get_xml(filename): 
	'''
	Input: 
	  a portal ID string 
	Output:
	  flag - corresponding to whether the xml of the portal has been downloaded

	Comments: 
	  portal format? 
	  delete xml file? 

	'''
	print("Downloading xml: ", filename)

	command = 'curl "http://genome.jgi.doe.gov/ext-api/downloads/get-directory?organism=' \
	+ str(filename) + '" -b cookies > ' + plato + '/files/' + str(filename) + '.xml'

	flag = subprocess.call(command, shell=True)


def extract_file(id_name): 
	'''
	Input: 
	  numerical id of the downloaded project 
	Output:
	  

	Comments: 
	  extracts folder from single downloaded tar file
	  other file formats?

	'''
	tar = tarfile.open(plato + '/files/' + id_name + '.tar.gz', 'r:gz')
	tar.extractall(path = (plato + '/files'))
	tar.close()


def download_file(xml_file): 
	'''
	Input: 
	  xml file 
	Output:
	  flag - corresponding to whether the xml of the portal has been downloaded
	  filename - the name of the downloaded file folder

	Comments: 
	  portal format? 
	  delete xml file? 
	  handle flag?

	'''

	tree = ET.parse(plato + '/files/' + xml_file + '.xml')
	root = tree.getroot()

	url = ''
	filename = ''
	for i in root[1]: 
		if i.attrib['filename'].endswith('.tar.gz'): 
			url = i.attrib['url']
			url.replace('&amp;', '&')
			filename = i.attrib['filename'].split('.')[0]

	if url == '' or filename == '': 
		print('Error finding file to download in xml file: ', xml_file)
		sys.exit() 
	else: 
		print("Downloading file: ", filename)
		command = 'curl "http://genome.jgi.doe.gov' + str(url) + \
		'" -b cookies > ' + plato + '/files/' + str(filename) + '.tar.gz'
		flag = subprocess.call(command, shell=True)
		
		if flag == 0: 
			print("Extracting file: ", filename)
			extract_file(filename)
		elif flag == 1: 
			print("Error downloading file. ")
			sys.exit()
		
	return filename


def get_fasta_config(folder): 
	'''
	Input: 
	  folder name of downloaded project files
	  
	Output:
	  name of fasta file 
	  name of config file (environment information)

	Comments: 
	  check if files present
	  
	'''
	print('Finding fasta and config files. ')
	fasta = []
	config = ''
	
	for dirname, dirnames, filenames in os.walk(plato + '/files/' + str(folder)): 
		for filename in filenames: 
			name = str(os.path.join(dirname, filename))

			if name.endswith('.faa'): 
				fasta.append(name)
				command = 'cp ' + name + ' ' + plato + '/fasta/' + filename
				flag = subprocess.call(command, shell=True)
				if flag == 1: 
					print("Error copying fasta file: ", name)
					sys.exit()
			
			elif name.endswith('.config'): 
				config = name
				command = 'cp ' + name + ' ' + plato + '/config/' + filename
				flag = subprocess.call(command, shell=True)
				if flag == 1: 
					print("Error copying config file: ", name)
					sys.exit()

	if fasta == []: 
		print('Error finding fasta file. ')
		sys.exit() 
	if config == '': 
		print('Error finding config file. ')
		sys.exit()

	return fasta, config



if __name__ == '__main__':
	global plato
	plato = 'ahuang@crick.cgl.ucsf.edu:/nobackup/babbittlab/audrey'
	sign_in()

	project_list = '../files/genome-projects.csv'
	name = 'Colrivmeta1547A3_FD'
	get_xml(name)
	filename = download_file(name)
	fasta, config = get_fasta_config(filename)
	print(name, filename)
	print(fasta, config)
	
	# portal_list = get_projects(project_list)
	# for portal_name in portal_list: 
	# 	flag = get_xml(portal_name)
	#	filename, flag = download_file(portal_name)
	#	fasta, config = get_fasta_config(filename)

		
	



