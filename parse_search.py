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


def hmmsearch(search, hmm, fasta, out):
	command = search + 'hmmsearch --tblout ' + out + ' ' + hmm + ' ' + fasta
	status = subprocess.call(command, shell=True)

	if status == 1: 
		print('Error calling hmmsearch. ')
		sys.exit()


def parse(out): 
	results = []
	for qresult in SearchIO.parse(out, 'hmmer2-text'): 
		results.append(qresult.id)

	return results


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
	# input is name of fasta which corresponds to config

	hmm_path = './hmmlibrary.HMMs'
	hmmsearch_path = '../tools/hmmer-3.1b2/src/./'
	fasta_path = '../files/3300007621/3300007621.a.faa'
	searchout_path = '../results.tblout'
	config_path = '../files/3300007621/'

	# hmmbuild(hmmbuild_path, msa_path, buildout_path)
	hmmsearch(hmmsearch_path, hmm_path, fasta_path, searchout_path)

	# (clas, order) = parse_config(fasta_path)



if __name__ == '__main__':
	main()

