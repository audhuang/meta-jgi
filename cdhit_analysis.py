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
import cPickle as cp


def convert_to_fasta(inp): 
	with open(inp + '.sequences', 'r') as f: 
		with open(inp + '.faa', 'w') as out:
			for line in f: 
				fa = line.split()
				if len(fa[1].strip()) >= 50: 
					out.write('>' + fa[0].strip() + '\n')
					out.write(fa[1].strip() + '\n')


def concat_fasta(out, file1, file2): 
	with open(out + '.faa', 'w') as out: 
		with open(file1, 'r') as f1: 
			for line in f1: 
				out.write(line) 
		with open(file2, 'r') as f2: 
			for line in f2: 
				out.write(line)


def cluster(path, thresh, inp): 

	command = path + 'cd-hit -i ' + inp + '.faa -o ' + inp + str(int(thresh * 100)) + ' -c ' + \
	str(thresh) + ' -n 5'

	print(command)
	status = subprocess.call(command, shell=True)


# def parse_clstr(inp): 
# 	with open(inp, 'r') as f: 
# 		for line in f: 
# 			if line[0] == '>': 
# 				cluster = line[8:]
# 			else: 


def get_lengths(inp): 
	lengths = []
	with open(inp, 'r') as f: 
		for line in f: 
			if line[0] != '>': 
				lengths.append(len(line))

	with open(r'lengths.pickle', 'wb') as out: 
		cp.dump(lengths, out)




def main(): 
	cdhit = '../tools/cdhit/'
	thresh = 0.8
	inp = '../proteins_that_were_hit'
	out = '../hits_and_superfamily'

	# convert_to_fasta(inp)
	# concat_fasta(out, inp + '.faa', '../sfld_superfamily_122.fasta')
	# cluster(cdhit, thresh, out)
	get_lengths(inp + '.faa')
	


if __name__ == '__main__':
	main()