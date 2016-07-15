from __future__ import print_function
from __future__ import division
import math
import random
import time
import sys
import getpass
import argparse

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


#===============================================================================
# Helper Functions
#===============================================================================

def get_ext(filename): 

	split_list = filename.split('.')
	name = '.'.join(split_list[:-2])
	ext = '.'.join(split_list[-2:])

	return name, ext


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
	+ str(filename) + '" -b cookies > ' + '../files/' + str(filename) + '.xml'

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
	try: 
		tar = tarfile.open('../files/' + id_name + '.tar.gz', 'r:gz')
		tar.extractall(path = '../files')
		tar.close()

	except tarfile.ReadError: 
		with open("../files/notargz_files.txt", "a") as myfile:
			myfile.write(id_name + '\n')
		tar = tarfile.open('../files/' + id_name + '.tar.gz', 'r')
		tar.extractall(path = '../files')
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

	url = []
	filename = []

	try: 
		tree = ET.parse('../files/' + xml_file + '.xml')
		root = tree.getroot()
	except ET.ParseError: 
		print('No permission for xml file: ', xml_file)
		with open("../files/nopermiss_files.txt", "a") as myfile:
			myfile.write(xml_file + '\n')
		return filename

	for i in root: 
		for j in i: 
			if 'filename' in j.attrib: 
				name, ext = get_ext(j.attrib['filename'])
				if ext == 'tar.gz': 
					url.append(j.attrib['url'].replace('&amp;', '&'))
					filename.append(name)

	if url == [] or filename == []: 
		print('Error finding file to download in xml file: ', xml_file)
		with open("../files/unfound_files.txt", "a") as myfile:
			myfile.write(xml_file + '\n')
		return filename
		# sys.exit() 
	else: 
		for i in range(len(filename)): 
			print("Downloading file: ", filename[i])
			command = 'curl "http://genome.jgi.doe.gov' + str(url[i]) + \
			'" -b cookies > ' + '../files/' + str(filename[i]) + '.tar.gz'
			flag = subprocess.call(command, shell=True)
			
			if flag == 0: 
				print("Extracting file: ", filename[i])
				extract_file(filename[i])
				command = 'rm -rf ../files/' + filename[i] + '.tar.gz'
				flag = subprocess.call(command, shell=True)
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
	print('Finding config files. ')
	config = []
	
	for dirname, dirnames, filenames in os.walk('../files/' + str(folder)): 
		for filename in filenames: 
			name = str(os.path.join(dirname, filename))

			if name.endswith('.config'): 
				config.append((name, filename))

	if config == []: 
		print('Error finding config file. ')
		with open("../files/noconfig_files.txt", "a") as myfile:
			myfile.write(folder + '\n')
		# sys.exit()


	if config != []: 
		for con in config: 
			command = 'cp ' + con[0] + ' ../config/' + folder + '.config'
			flag = subprocess.call(command, shell=True)
			if flag == 1: 
				print("Error copying config file: ", config)
				sys.exit()

	# delete folder  
	command = 'rm -rf ../files/' + str(folder)
	flag = subprocess.call(command, shell=True)


	return config

#===============================================================================
# Main Loop
#===============================================================================

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Set a start point. ')
	parser.add_argument('--start', nargs='?', type=str, default='PueRicMetagenome_FD')
	args = parser.parse_args()

	project_list = '../files/genome-projects.csv'
	portal_list = get_projects(project_list)
	start = portal_list.index(args.start)
	print('START: ', start)

	if start == 0: 
		open('../files/unfound_files.txt', 'w').close()
		open('../files/nopermiss_files.txt', 'w').close()
		open('../files/nofasta_files.txt', 'w').close()
		open('../files/noconfig_files.txt', 'w').close()
		open('../files/notargz_files.txt', 'w').close()


	sign_in()
	for i in range(start, len(portal_list)): 
		print('\nINDEX: ', i)
		portal_name = portal_list[i]
		get_xml(portal_name)
		filename = download_file(portal_name)
		if filename != []: 
			for fil in filename: 
				config = get_fasta_config(fil)
		time.sleep(30)

		if i == 100: 
			time.sleep(100)




		
	



