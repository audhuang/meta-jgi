from __future__ import print_function
from __future__ import division
import math
import random
import time
import sys
import argparse
import re

import numpy as np 
import csv
import subprocess
import requests 
import urllib2
from bs4 import BeautifulSoup as bs
import os
from os import listdir
from os.path import isfile, join 
import cPickle as cp
from HTMLParser import HTMLParser


def num_and_metadata(): 

	with open(r'project_hit_dic.pickle', 'rb') as inp: 
		projects = cp.load(inp).keys()
	
	project_num_dic = {}
	project_meta_dic = {}
	count = 0
	
	for oid in projects: 
		url = 'https://img.jgi.doe.gov/cgi-bin/m/main.cgi?section=TaxonDetail&page=taxonDetail&taxon_oid=' + oid
		req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
		response = urllib2.urlopen(req)
		html = response.read()
		
		soup = bs(html, 'html.parser')
		th = soup.find_all('th')
		num = 0
		meta = ['' for i in range(4)]

		for header in th: 
			if header.string == 'Number of sequences':
				num = int(header.find_next('td').text)
			elif header.string == 'Ecosystem': 
				meta[0] = header.find_next('td').text
			elif header.string == 'Ecosystem Category': 
				meta[1] = header.find_next('td').text
			elif header.string == 'Ecosystem Subtype': 
				meta[2] = header.find_next('td').text
			elif header.string == 'Ecosystem Type': 
				meta[3] = header.find_next('td').text
	
		project_num_dic[oid] = num
		project_meta_dic[oid] = meta

		count += 1
		if count % 100 == 0: 
			print('count: ', count)
			print('oid: ', oid)
			print('num: ', num)
			print('meta: ', meta)

	with open(r'project_num_dic.pickle', 'wb') as out: 
		cp.dump(project_num_dic, out)
	with open(r'project_meta_dic.pickle', 'wb') as out: 
		cp.dump(project_meta_dic, out)



def metadata(oid): 
	url = 'https://img.jgi.doe.gov/cgi-bin/m/main.cgi?section=TaxonDetail&page=taxonDetail&taxon_oid=' + oid
	req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
	response = urllib2.urlopen(req)
	html = response.read()

	meta = []
	soup = bs(html, 'html.parser')
	th = soup.find_all('th')
	for header in th: 
		if header.string == 'Ecosystem': 
			meta.append(header.find_next('td').text)
		elif header.string == 'Ecosystem Category': 
			meta.append(header.find_next('td').text)
		elif header.string == 'Ecosystem Subtype': 
			meta.append(header.find_next('td').text)
		elif header.string == 'Ecosystem Type': 
			meta.append(header.find_next('td').text)
	
	return meta





def main(): 
	num_and_metadata()
	

	
	
	

if __name__ == '__main__':
	main()