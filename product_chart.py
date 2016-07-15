from __future__ import print_function
from __future__ import division
import math
import random
import time
import sys
import getpass
import argparse

import numpy as np 
import matplotlib.pyplot as plt
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



def analyze_projects(project_list): 
	'''
	Input: 
	  csv file of list of all projects
	Output:
	  produces pie chart of different types of metagenomic products 

	Comments: 

	'''
	df = pd.read_csv(project_list)
	saved_column = df['Product Name']
	count_dic = dict(Counter(list(saved_column)))
	print(count_dic)
	print(len(count_dic))
	
	projects = ['Other', 'Standard Draft', 'Minimal Draft', 'Annotated \nMetatranscriptome']
	count = [0, 0, 0, 0]
	for key in count_dic: 
		if 'Standard Draft' in key: 
			count[1] += count_dic[key]
		elif 'Minimal Draft' in key: 
			count[2] += count_dic[key]
		elif 'Annotated Metatranscriptome' in key: 
			count[3] += count_dic[key]
		else: 
			count[0] += int(count_dic[key])

	print(projects)
	print(count)

	plt.pie(
		count, 
		labels=projects, 
		autopct='%1.1f%%',
		)
	plt.axis('equal')
	plt.tight_layout()
	plt.show()



if __name__ == '__main__':
	project_list = '../files/genome-projects.csv'

	analyze_projects(project_list)
