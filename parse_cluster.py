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
				counts.append([0])

			else: 
				perc = int(ine.split(' ')[-1][:-3])
				print(perc)



def main(): 
	inp = '../proteins_that_were_hit90.clstr'
	num_redundancies(inp)

if __name__ == '__main__':
	main()