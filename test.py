from __future__ import print_function
from __future__ import division

import math
import random
import time

import numpy as np 
import matplotlib.pyplot as plt
import csv 

import xml.etree.ElementTree as ET 
import pandas as pd
import urllib2
import os
from os import listdir
from os.path import isfile, join 
import zipfile
import tarfile
import requests

if __name__ == '__main__':
	# r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
	project_list = '../files/genome-projects.csv'

	df = pd.read_csv(project_list)
	portal_ids = df['Portal ID'].apply(str)

	i = 0
	for portal in df['Product Name']: 
		if 'Draft' in portal: 
			temp = portal_ids[i].split(',')[1][1:-2]
			if ',' or '"' in temp: 
				print(temp)

		i += 1



