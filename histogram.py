from __future__ import print_function
from __future__ import division
import math
import random
import time
import sys

import numpy as np 
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import csv

import subprocess
import os
import cPickle as cp
from collections import Counter



# with open(r'lengths.pickle') as inp: 
# 	lengths = cp.load(inp)


# n = 6
# ind = np.arange(n)
# width = 0.35

# hist = [0] * 6

# for i in lengths: 
# 	if i < 50: 
# 		hist[0] += 1
# 	elif i >= 50 and i < 150: 
# 		hist[1] += 1
# 	elif i >= 150 and i < 250: 
# 		hist[2] += 1
# 	elif i >= 250 and i < 500: 
# 		hist[3] += 1 
# 	elif i >= 500 and i < 1000: 
# 		hist[4] += 1
# 	else: 
# 		hist[5] += 1


# with open(r'survey_counts.pickle') as inp: 
# 	counts = cp.load(inp)

# keys = list(np.log(counts.values()))

# n = 1
# ind = np.arange(int(max(keys) / n) + 1)
# print(len(ind))
# width = 0.35

# hist = [0] * int(max(keys) / n + 1)
# for key in keys: 
# 	hist[int(key / n)] += 1


with open(r'cluster_super.pickle') as inp: 
	counts = cp.load(inp)


n = 5
ind = np.arange(n)
width = 0.35

hist = [0] * n

for i in counts: 
	if i == 0: 
		hist[0] += 1
	elif i == 1: 
		hist[1] += 1
	elif i > 0 and i <= 10: 
		hist[2] += 1
	elif i > 10 and i <= 100: 
		hist[3] += 1
	elif i > 100 and i <= 1000: 
		hist[4] += 1



fig, ax = plt.subplots()
rects = ax.bar(ind, hist, width)

ax.set_xlabel('# superfamily members per cluster')
ax.set_ylabel('# of clusters')
ax.set_title('# superfamily members')
ax.set_xticks(ind)
ax.set_xticklabels(('0', '1', ' <10', '<10^2', '<10^3'))


def autolabel(rects): 
	for rect in rects: 
		height = rect.get_height()
		ax.text(rect.get_x() + rect.get_width()/2, 1.05*height, '%f' % (height / 351623), ha='center', va='bottom')
autolabel(rects)

plt.show()
