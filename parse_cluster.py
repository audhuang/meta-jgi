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
				print(line.split('\t'))


def main(): 
	inp = '../hits_and_superfamily90.clstr'
	num_redundancies(inp)

if __name__ == '__main__':
	main()