from __future__ import print_function
from __future__ import division
import math
import random
import time
import sys
import getpass
import argparse

import numpy as np 
import cPickle as cp
# import matplotlib.pyplot as plt
import pandas as pd
import csv

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

def parse_config(inp): 
	'''
	Input: 
	  name of config file, including .config extension 
	  
	Output:
	  class of environment 
	  order of environment

	Comments: 
	  check if files present
	  
	'''
	classification = [''] * 6
	with open('../config/' + inp) as f: 
		for line in f: 
			linelist = line.split(' ')
			if 'domain' in linelist[0]: 
				classification[0] = linelist[1].strip().lower() 
			elif 'family' in linelist[0]: 
				classification[4] = linelist[1].strip().lower()
			elif 'genus' in linelist[0]: 
				classification[5] = linelist[1].strip().lower()
			elif 'ir_class' in linelist[0]: 
				classification[2] = linelist[1].strip().lower() 
			elif 'ir_order' in linelist[0]: 
				classification[3] = linelist[1].strip().lower()
			elif 'phylum' in linelist[0]: 
				classification[1] = linelist[1].strip().lower()
	return classification


def test(): 
	'''
	  test parsing on a single config file 
	'''
	inp = 'Colrivmeta1547A3_FD.config'
	classification = parse_config(inp)
	print(classification)


#===============================================================================
# Get Config Info
#===============================================================================

def main(): 
	'''
	Comments: 
	  creates dictionary of IMG identifier : (class, order)

	  consider adding other features from the config file? 
	  
	'''
	# img_metadata_dic = {}
	with open('../config_krona.txt', 'wb') as f: 
		write = csv.writer(f, delimiter='\t')
		for dirname, dirnames, filenames in os.walk('../config'): 
			for filename in filenames: 
				if filename.endswith('.config'): 
					# img_metadata_dic[filename.split('.')[0]] = parse_config(filename)
					write.writerow(parse_config(filename))

	# with open('../code/img_metadata_dic.p', 'wb') as f: 
	# 	cp.dump(img_metadata_dic, f)
	# print(img_metadata_dic)


if __name__ == '__main__':
	main()