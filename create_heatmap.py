from __future__ import print_function
from __future__ import division
import math
import random
import time
import sys
import argparse

import numpy as np 
import subprocess
import os
from os import listdir
from os.path import isfile, join 
from collections import Counter 


def cut_length(fasta_path, out, low, high): 
	cut = 0
	with open(fasta_path, 'r') as f: 
		with open(out, 'w') as out:
			for line in f: 
				fa = line.split()
				if len(fa[1].strip()) >= low and len(fa[1].strip()) <= high: 
					out.write('>' + fa[0].strip() + '\n')
					out.write(fa[1].strip() + '\n')
				else: 
					cut += 1
	print('# cut sequences: ', cut)


def main(): 
	fasta_path = '../proteins_that_were_hit.sequences'
	fasta_cut_path = '../hits_50_1000.faa' 

	cut_length(fasta_path, fasta_cut_path, 50, 1000)



if __name__ == '__main__':
	main()