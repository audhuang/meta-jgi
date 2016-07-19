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
	clas = ''
	order = ''
	with open('../config/' + inp) as f: 
		for line in f: 
			linelist = line.split(' ')
			if 'ir_class' in linelist[0]: 
				clas = linelist[1].strip().lower() 
			elif 'ir_order' in linelist[0]: 
				order = linelist[1].strip().lower()
	return (clas, order)


def test(): 
	inp = 'Colrivmeta1547A3_FD.config'
	(clas, order) = parse_config(inp)
	print(clas, order)


#===============================================================================
# Get Config Info
#===============================================================================

def main(): 
	img_metadata_dic = {}

	for dirname, dirnames, filenames in os.walk('../config'): 
		for filename in filenames: 
			if filename.endswith('.config'): 
				img_metadata_dic[filename.split('.')[0]] = parse_config(filename)

	with open('../code/img_metadata_dic.p', 'wb') as f: 
		cp.dump(img_metadata_dic, f)
	print(img_metadata_dic)


if __name__ == '__main__':
	main()