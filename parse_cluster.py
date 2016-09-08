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

def num_redundancies(inp): 
	counts = []
	with open(inp, 'r') as f: 
		for line in f: 
			if line[0] == '>': 
				counts.append(0)

			else: 
				perc = (line.split(' ')[-1].strip()[:-1])
				if perc != '' and float(perc) >= 99.: 
					counts[-1] += 1

	with open(r'cluster_redun.pickle', 'wb') as out: 
		cp.dump(counts, out)


def num_superfamily(inp): 
	counts = []
	with open(inp, 'r') as f: 
		for line in f: 
			if line[0] == '>': 
				counts.append(0)

			else: 
				perc = line.split(' ')
				print(perc)

	with open(r'cluster_redun.pickle', 'wb') as out: 
		cp.dump(counts, out)



def main(): 
	# inp = '../proteins_that_were_hit90.clstr'
	# num_redundancies(inp)

	inp = '../hits_and_superfamily80.clstr'
	num_superfamily(inp)

if __name__ == '__main__':
	main()