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
import pandas as pd
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


def projectimg_dic(project_path, pickle_path): 
	project_img_dic = {}
	img_project_dic = {}

	with open(project_path, 'rb') as inp: 
		reader = csv.reader(inp, delimiter = ',')
		next(reader)
		for row in reader: 
			if row[15] != '': 
				links = row[15].split(' ')
				for link in links: 
					name = link.split(',')[1][1:-2]

					if row[7] not in project_img_dic: 
						project_img_dic[row[7]] = [str(name)] 
					else: 
						project_img_dic[row[7]].append(str(name))

					if name not in img_project_dic: 
						img_project_dic[name] = str(row[7])

	
	with open(r'project_img_dic.pickle', 'wb') as out: 
		cp.dump(project_img_dic, out)
	with open(r'img_project_dic.pickle', 'wb') as out: 
		cp.dump(img_project_dic, out)

	return project_img_dic, img_project_dic
	# df = pd.read_csv(project_path)
	# groups = list(df['IMG Portal'].groupby(df['Proposal']))
	# print(groups)
	# portal_ids = df['Portal ID'].apply(str)
		#15


def projecthit_dic(cluster_path): 
	project_hit_dic = {}

	with open(cluster_path, 'r') as f: 
		for line in f: 
			cluster = -1
			if line[0] == '>': 
				cluster = line.strip().split(' ')[-1]
				print(cluster)



def main(): 
	seq_path = '../proteins_that_were_hit.sequences'
	fasta_cut_path = '../hits_50_1000.faa' 
	cdhit_path = '../tools/cdhit/'

	project_path = '../files/genome-projects.csv'
	cluster_path = '../hits_50_1000_90.clstr'

	# cut_length(seq_path, fasta_cut_path, 50, 1000)
	# cluster(cdhit_path, fasta_cut_path[:-4], 0.9, 5)
	# project_img_dic, img_project_dic = projectimg_dic(project_path, pickle_path)
	projecthit_dic(cluster_path)



if __name__ == '__main__':
	main()