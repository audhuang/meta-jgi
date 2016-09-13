from __future__ import print_function
from __future__ import division
import math
import random
import time
import sys
import argparse

import numpy as np 
import csv
import subprocess
import os
from os import listdir
from os.path import isfile, join 
from collections import Counter 
import cPickle as cp

def cut_length(seq_path, out, low, high): 
	cut = 0
	with open(seq_path, 'r') as f: 
		with open(out, 'w') as out:
			for line in f: 
				fa = line.split()
				if len(fa[1].strip()) >= low and len(fa[1].strip()) <= high: 
					out.write('>' + fa[0].strip() + '\n')
					out.write(fa[1].strip() + '\n')
				else: 
					cut += 1
	print('# cut sequences: ', cut)


def cluster(cdhit_path, fasta_path, thresh, c): 
	command = cdhit_path + 'cd-hit -i ' + fasta_path + '.faa -o ' + fasta_path + '_'+ \
	str(int(thresh * 100)) + ' -c ' + str(thresh) + ' -n ' + str(c)

	status = subprocess.call(command, shell=True)


def project_id_dic(project_path, pickle_path): 
	with open(project_path, 'rb') as inp: 
		reader = csv.reader(inp, delimiter = '\t')
		for row in reader: 
			print(row[7])


def main(): 
	seq_path = '../proteins_that_were_hit.sequences'
	fasta_cut_path = '../hits_50_1000.faa' 
	cdhit_path = '../tools/cdhit/'

	project_path = '../files/genome-projects.csv'
	pickle_path = './project_id_dic.pickle'

	# cut_length(seq_path, fasta_cut_path, 50, 1000)
	# cluster(cdhit_path, fasta_cut_path[:-4], 0.9, 5)



if __name__ == '__main__':
	main()