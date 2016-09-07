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
				if len(fa[1].strip()) >= 50: 
					out.write('>' + fa[0].strip() + '\n')
					out.write(fa[1].strip() + '\n')



def cluster(path, thresh, inp): 

	command = path + 'cd-hit -i ' + inp + '.faa -o ' + inp + str(int(thresh * 100)) + ' -c ' + \
	str(thresh) + ' -n 5'

	print(command)
	status = subprocess.call(command, shell=True)


def main(): 
	cdhit = '../tools/cdhit/'
	thresh = 0.8
	inp = '../proteins_that_were_hit'

	convert_to_fasta(inp)
	cluster(cdhit, thresh, inp)
	


if __name__ == '__main__':
	main()