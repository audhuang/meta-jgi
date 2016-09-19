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


def num_sequences(oid): 
	url = 'https://img.jgi.doe.gov/cgi-bin/m/main.cgi?section=TaxonDetail&page=taxonDetail&taxon_oid=' + oid
	req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
	response = urllib2.urlopen(req)
	html = response.read()
	
	soup = bs(html, 'html.parser')
	table = soup.find_all('table')[1]
	sequences = table.find_all('a')[0].string

	return sequences


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
	oid = '3300005254'
	# num = num_sequences(oid)
	meta = metadata(oid)
	
	

if __name__ == '__main__':
	main()