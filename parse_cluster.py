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
from collections import Counter


def num_redundancies(inp): 
	counts = []
	totals = []
	with open(inp, 'r') as f: 
		for line in f: 
			if line[0] == '>': 
				counts.append(0)
				totals.append(0)

			else: 
				perc = (line.split(' ')[-1].strip()[:-1])
				if perc != '' and float(perc) >= 99.: 
					counts[-1] += 1
			totals[-1] += 1

	perc = []
	for i in range(len(counts)): 
		perc.append(counts[i] / totals[i])

	# unique = list(Counter(counts).items())
	unique = list(Counter(perc).items())

	with open(r'cluster_redun.pickle', 'wb') as out: 
		cp.dump(counts, out)
	with open(r'cluster_redun_counts.pickle', 'wb') as out: 
		cp.dump(unique, out)


def num_superfamily(inp): 
	counts = []
	with open(inp, 'r') as f: 
		for line in f: 
			if line[0] == '>': 
				counts.append(0)

			else: 
				pre = line.split(' ')[1][:3].strip()
				if pre == '>GI': 
					counts[-1] += 1

	with open(r'cluster_super.pickle', 'wb') as out: 
		cp.dump(counts, out)


def num_overlap(table_path): 
	with open(r'subgroups.pickle', 'rb') as inp: 
		subgroups = cp.load(inp)

	pfam = []
	counts = [0 for x in subgroups]
	linecount = 0

	with open(table_path, 'r') as f: 
		for line in f: 
			if line[0] != '#': 
				col = line.split()
				subgroup = col[2]
				name = col[0]

				if subgroup == 'Nitroreductase': 
					pfam.append(name)

	with open(table_path, 'r') as f: 
		for line in f: 
			if line[0] != '#': 
				col = line.split()
				subgroup = col[2]
				name = col[0]

				if subgroup != 'Nitroreductase': 
					if name in pfam: 
						ind = subgroups.index(subgroup)
						counts[ind] += 1
			linecount += 1
			if linecount % 10000 == 0: 
				print('linecount: ', linecount)
				print('projects: ', subgroups)
				print('counts: ', counts)
	
	print('final projects: ', subgroups)
	print('final counts: ', counts)


	with open(r'results_overlap.pickle', 'wb') as out: 
		cp.dump(counts, out)


def overlap(table_path): 


	pfam = []
	counts = 0
	linecount = 0

	with open(table_path, 'r') as f: 
		for line in f: 
			if line[0] != '#': 
				col = line.split()
				subgroup = col[2]
				name = col[0]

				if subgroup == 'Nitroreductase': 
					pfam.append(name)

	with open(table_path, 'r') as f: 
		for line in f: 
			if line[0] != '#': 
				col = line.split()
				subgroup = col[2]
				name = col[0]

				if subgroup != 'Nitroreductase': 
					if name in pfam: 
						count += 1
			linecount += 1
			if linecount % 10000 == 0: 
				print('linecount: ', linecount)
				print('counts: ', counts)
	
	print('final counts: ', counts)



def num_total(table_path): 
	with open(r'subgroups.pickle', 'rb') as inp: 
		subgroups = cp.load(inp)

	counts = [0 for x in subgroups]
	print('subgroups: ', subgroups)
	print('counts: ', counts)

	linecount = 0

	with open(table_path, 'r') as f: 
		for line in f: 
			if line[0] != '#': 
				col = line.split()
				subgroup = col[2]
				name = col[0]

				ind = subgroups.index(subgroup)
				counts[ind] += 1

	print('final projects: ', subgroups)
	print('final counts: ', counts)


	with open(r'subgroup_counts.pickle', 'wb') as out: 
		cp.dump(counts, out)


def main(): 

	inp = '../hits_and_superfamily80.clstr'
	table_path = '../results.table'
	# num_superfamily(inp)
	# num_redundancies(inp)
	# num_overlap(table_path)
	# num_total(table_path)
	overlap(table_path)

if __name__ == '__main__':
	main()