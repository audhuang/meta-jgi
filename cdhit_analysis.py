from __future__ import print_function
from __future__ import division
import math
import random
import time
import sys

import numpy as np 
import pandas as pd
import csv

import subprocess
import os


def convert_to_fasta(inp): 
	with open(inp + '.sequences', 'r') as f: 
		with open(inp + '.faa', 'w') as out:
			for line in f: 
				fa = line.split()
				out.write('>' + fa[0] + '\n')
				out.write(fa[1] + '\n')



def cluster(path, thresh, inp): 
	if thresh >= 0.6: 
		command = path + 'cd-hit -i ' + inp + '.sequences -o ' + inp + str(60) + '.sequences -c ' + \
		str(thresh) + ' -n 4 -M 16000 -d 0 -T 8'

		status = subprocess.call(command, shell=True)

	elif thresh >= 0.8: 
		command = path + 'cd-hit -i ' + inp + '.sequences -o ' + inp + str(thresh * 100) + '.sequences -c ' + \
		str(thresh * 100) + ' -n 5 -M 16000 -d 0 -T 8'

		print(command)
		# status = subprocess.call(command, shell=True)


def main(): 
	cdhit = '../tools/cdhit/'
	thresh = 0.9
	inp = '../proteins_that_were_hit'
	# cluster(cdhit, thresh, inp)
	convert_to_fasta(inp)


if __name__ == '__main__':
	main()