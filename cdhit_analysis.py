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


def cluster(path, thresh, inp): 
	if thresh >= 0.6: 
		command = path + 'cd-hit -i ' + inp + '.sequences -o ' + inp + str(60) + '.sequences -c ' + \
		str(60) + ' -n 4'
		print(command)

		status = subprocess.call(command, shell=True)

	if thresh >= 0.8: 
		command = path + 'cd-hit -i ' + inp + str(60) + '.sequences -o ' + inp + str(thresh) + '.sequences -c ' + \
		str(thresh) + ' -n 5'

		status = subprocess.call(command, shell=True)


def main(): 
	cdhit = '../tools/cdhit/'
	thresh = 0.6
	inp = '../proteins_that_were_hit.sequences'
	cluster(cdhit, thresh, inp)


if __name__ == '__main__':
	main()