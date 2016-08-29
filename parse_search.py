from __future__ import print_function
from __future__ import division
import math
import random
import time
import sys
import getpass
import argparse

import numpy as np 
# import matplotlib.pyplot as plt
import pandas as pd
import csv

import subprocess
import os
from os import listdir
from os.path import isfile, join 
import tarfile
import requests
from collections import Counter 
import pprint
from Bio import SearchIO


def hmmbuild(build, msa, out): 
	command = build + 'hmmbuild ' + out + msa
	status = subprocess.call(command, shell=True)
	
	if status == 1: 
		print('Error calling hmmbuild. ')
		sys.exit()


def hmmsearch(search, hmm, fa, fasta_path, out):
	command = search + 'hmmsearch --tblout ' + out + fa + '_results.tblout' + ' ' + hmm + ' ' + fasta_path
	print('command: ', command)
	status = subprocess.call(command, shell=True)

	if status == 1: 
		print('Error calling hmmsearch. ')
		sys.exit()


def parse(fa, out): 
	results = {}
	# for qresult in SearchIO.parse(out, 'hmmer3-text'): 
	with open(out + fa + '_results.tblout') as f: 
		for line in f: 
			if line[0] != '#': 
				subgroup = line.split()[2]
				if subgroup != 'Nitroreductase': 
					if subgroup not in results: 
						results[subgroup] = 1
					else: 
						results[subgroup] += 1

	return results 


def write_results(fa, out, results, header):
	with open(out, 'a') as f:
		write = csv.writer(f, delimiter=',')
		if header == False: 
			subgroups = list(results.keys())
			write.writerow([''] + subgroups)

		val = list(results.values())
		total = sum(val)
		val[:] = [x / total for x in val]

		write.writerow([fa] + val)


def parse_config(inp): 
	'''
	Input: 
	  name of config file, including .config extension 
	  
	Output:
	  class of environment 
	  order of environment

	Comments: 
	  check if files present
	  
	'''
	clas = ''
	order = ''
	with open('../config/' + inp + '.config') as f: 
		for line in f: 
			linelist = line.split(' ')
			if 'ir_class' in linelist[0]: 
				clas = linelist[1].strip().lower() 
			elif 'ir_order' in linelist[0]: 
				order = linelist[1].strip().lower()
	return (clas, order)


def parse_phylo(inp): 
	with open('../phylo/' + inp + '.phylo') as f: 
		for line in f: 
			linelist = line.split(' ')
			if linelist[0] == inp: 
				phylodic[linelist[0]] = linelist[1] 

	return phylodic



def main(): 
	parser = argparse.ArgumentParser(description='add test file?')
	# parser.add_argument('--start', nargs='?', type=str, default='PueRicMetagenome_FD')
	parser.add_argument('--add', nargs='?', type=str, default=None)
	args = parser.parse_args()


	hmm_path = './hmmlibrary.HMMs'
	hmmsearch_path = '../tools/hmmer-3.1b2/src/./'
	fasta_path = '../files/'
	searchout_path = '../'
	config_path = '../files/'
	results_path = './data'

	header = False
	if add != None: 
		fasta = [str(args.add)]
		header = True
	else: 
		fasta = ['3300007621', '3300006190', '3300006034']
		open(results_path, 'w').close()
	
	print(fasta)

	# hmmbuild(hmmbuild_path, msa_path, buildout_path)
	

	for fa in fasta: 
		hmmsearch(hmmsearch_path, hmm_path, fa, (fasta_path + fa + '/' + fa + '.a.faa'), searchout_path)
		results = parse(fa, searchout_path)
		write_results(fa, results_path, results, header)
		header = True

	# (clas, order) = parse_config(fasta_path)



if __name__ == '__main__':
	main()

