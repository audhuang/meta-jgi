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

#===============================================================================
# Helper Functions
#===============================================================================

def open_fasta(inp_file): 
	handle = open('../fasta/' + inp_file, 'rU')
	for fa in SeqIO.parse(handle, 'fasta'): 
		print(fa.seq.tostring())


#===============================================================================
# Analyze Files
#===============================================================================


if __name__ == '__main__':
	inp = '3300003150.a.faa'

	open_fasta(inp)