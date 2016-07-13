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

from Bio import SeqIO
import subprocess
import os
from os import listdir
from os.path import isfile, join 
import tarfile
import requests
from collections import Counter 
import pprint
from itertools import groupby, imap

#===============================================================================
# Helper Functions
#===============================================================================

def test_mean(inp_file): 
	tot = 0
	num = 0
	with open('../fasta/' + inp_file) as handle:
		for header, group in groupby(handle, lambda x:x.startswith('>')):
			if not header:
				num += 1
				tot += sum(imap(lambda x: len(x.strip()), group))
	result = float(tot)/num
	print(result)


#===============================================================================
# Analyze Files
#===============================================================================

def mean_length(inp_file): 
	'''
	Input: 
	  fasta file name
	  
	Output:
	  mean of fasta sequence lengths
	  var of fasta sequence lengths
	 
	Comments: 

	  
	'''
	num = 0
	tot = 0 
	sq = 0
	handle = open('../fasta/' + inp_file, 'rU')

	for fa in SeqIO.parse(handle, 'fasta'): 
		num += 1
		tot += len(str(fa.seq))
		sq += len(str(f.seq)) ** 2
	handle.close()
	
	mean = tot / num
	var = (sq - (tot ** 2) / num) / num
	return mean, var


#===============================================================================
# Main Loop
#===============================================================================

if __name__ == '__main__':
	inp = '3300003150.a.faa'

	mean, var = mean_length(inp)
	print('mean: ', mean)
	print('var: ', var)

	
