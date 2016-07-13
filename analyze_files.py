from __future__ import print_function
from __future__ import division
import math
import random
import time
import sys
import getpass

import numpy as np 
# import matplotlib.pyplot as plt
import pandas as pd

from Bio import SeqIO
import subprocess
import os
from os import listdir
from os.path import isfile, join 
import tarfile
import requests
from collections import Counter 
import pprint
from itertools import groupby, imap

#===============================================================================
# Helper Functions
#===============================================================================

def open_fasta(inp_file): 
	handle = open('../fasta/' + inp_file, 'rU')
	for fa in SeqIO.parse(handle, 'fasta'): 
		print(fa.seq.tostring())
	handle.close()


def test_ave(inp_file): 
	tot = 0
	num = 0
	with open('../fasta/' + inp_file) as handle:
		for header, group in groupby(handle, lambda x:x.startswith('>')):
			if not header:
				print(imap(lambda x: len(x.strip()), group))
				num += 1
				tot += sum(imap(lambda x: len(x.strip()), group))
	result = float(tot)/num
	print(result)

#===============================================================================
# Analyze Files
#===============================================================================


if __name__ == '__main__':
	inp = '3300003150.a.faa'

	test_ave(inp)