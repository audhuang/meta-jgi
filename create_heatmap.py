from __future__ import print_function
from __future__ import division
import math
import random
import time
import sys
import argparse

import numpy as np 
import csv
import subprocess
import os
from os import listdir
from os.path import isfile, join 
import pandas as pd
from collections import Counter 
import cPickle as cp

def cut_length(seq_path, out, low, high): 
	cut = 0
	with open(seq_path, 'r') as f: 
		with open(out, 'w') as out:
			for line in f: 
				fa = line.split()
				if len(fa[1].strip()) >= low and len(fa[1].strip()) <= high: 
					out.write('>' + fa[0].strip() + '\n')
					out.write(fa[1].strip() + '\n')
				else: 
					cut += 1
	print('# cut sequences: ', cut)


def cluster(cdhit_path, fasta_path, thresh, c): 
	command = cdhit_path + 'cd-hit -i ' + fasta_path + '.faa -o ' + fasta_path + '_'+ \
	str(int(thresh * 100)) + ' -c ' + str(thresh) + ' -n ' + str(c) + ' -M 16000 -d 100 -T 8'

	status = subprocess.call(command, shell=True)


def projectimg_dic(project_path, pickle_path): 
	project_img_dic = {}
	img_project_dic = {}

	with open(project_path, 'rb') as inp: 
		reader = csv.reader(inp, delimiter = ',')
		next(reader)
		for row in reader: 
			if row[15] != '': 
				links = row[15].split(' ')
				for link in links: 
					name = link.split(',')[1][1:-2]

					if row[7] not in project_img_dic: 
						project_img_dic[row[7]] = [str(name)] 
					else: 
						project_img_dic[row[7]].append(str(name))

					if name not in img_project_dic: 
						img_project_dic[name] = str(row[7])

	
	with open(r'project_img_dic.pickle', 'wb') as out: 
		cp.dump(project_img_dic, out)
	with open(r'img_project_dic.pickle', 'wb') as out: 
		cp.dump(img_project_dic, out)

	return project_img_dic, img_project_dic
	# df = pd.read_csv(project_path)
	# groups = list(df['IMG Portal'].groupby(df['Proposal']))
	# print(groups)
	# portal_ids = df['Portal ID'].apply(str)
		#15


def projecthit_dic(cluster_path): 
	project_hit_dic = {}
	id_cluster_dic = {}
	project_cluster_dic = {}

	with open(cluster_path, 'r') as f: 
		cluster = -1
		for line in f: 
			if line[0] == '>': 
				cluster = line.strip().split(' ')[-1]
			else: 
				name = line.strip().split(' ')[1][1:11]
				if name not in project_hit_dic: 
					project_hit_dic[name] = 1
				else: 
					project_hit_dic[name] += 1

				name_cluster = line.strip().split(' ')[1][1:-3]
				if name_cluster not in id_cluster_dic: 
					id_cluster_dic[name_cluster] = [cluster]
				else: 
					id_cluster_dic[name_cluster].append(cluster) 

				if name not in project_cluster_dic: 
					project_cluster_dic[name] = [cluster]
				else: 
					project_cluster_dic[name].append(cluster)


	with open(r'project_hit_dic.pickle', 'wb') as out: 
		cp.dump(project_hit_dic, out)
	with open(r'id_cluster_dic.pickle', 'wb') as out: 
		cp.dump(id_cluster_dic, out)
	with open(r'project_cluster_dic.pickle', 'wb') as out: 
		cp.dump(project_cluster_dic, out)

	# return project_hit_dic, id_cluster_dic, project_cluster_dic


def get_subgroups(table_path): 
	subgroups = []
	with open(table_path, 'r') as f: 
		for i in range(3): 
			f.next()
		for line in f: 
			col = line.split()
			if line[0] != '#': 
				subgroup = col[2]
				if subgroup not in subgroups: 
					subgroups.append(subgroup)

	with open(r'subgroups.pickle', 'wb') as out: 
		cp.dump(subgroups, out)
	
	return subgroups


def parse_table(table_path): 
	dic = {}
	cluster_dic = {}

	with open(r'id_cluster_dic.pickle', 'rb') as inp: 
		id_cluster_dic = cp.load(inp)
	with open(r'subgroups.pickle', 'rb') as inp: 
		subgroups = cp.load(inp)

	linecount = 0

	with open(table_path, 'r') as f: 
		for line in f: 
			if line[0] != '#': 
				col = line.split()
				subgroup = col[2]
				name = col[0].split('|')[0]

				if test_key in col[0]: 
					print('test key: ', col[0], col[2])

				if name not in dic: 
					dic[name] = [[] for i in subgroups]
				if id_cluster_dic.has_key(col[0].strip()): 
					for clu in id_cluster_dic[col[0].strip()]:
						dic[name][subgroups.index(subgroup)].append(clu)
					# print('cluster: ', id_cluster_dic[col[0]])
					# print(dic[name])
					# print("\n")
				else: 
					with open('no_index.txt', 'a') as f: 
						f.write(col[0] + '\n')
			linecount += 1

			if (linecount % 10000) == 0: 
				print('parsing line: ', linecount)



	for key in dic: 
		cluster_dic[key] = []
		for i in range(len(subgroups)): 
			cluster_dic[key].append(len(set(dic[key][i])))

	with open(r'cluster_ids.pickle', 'wb') as out: 
		cp.dump(dic, out)
	with open(r'cluster_counts.pickle', 'wb') as out: 
		cp.dump(cluster_dic, out)

	return cluster_dic


# hits or unique clusters?
def choose_surveys(num): 
	with open(r'project_img_dic.pickle', 'rb') as inp: 
		project_img_dic = cp.load(inp)
	# with open(r'project_hit_dic.pickle', 'rb') as inp: 
	# 	project_hit_dic = cp.load(inp)
	with open(r'project_cluster_dic.pickle', 'rb') as inp: 
		project_cluster_dic = cp.load(inp)

	test_key = '3300002662'

	biggest_list = []
	for key in project_img_dic: 
		biggest = 0
		biggest_index = 0
		imgs = project_img_dic[key]

		for i in range(len(imgs)): 
			if imgs[i] in project_cluster_dic: 
				num = len(set(project_cluster_dic[imgs[i]]))
				if num > biggest: 
					biggest = num
					biggest_index = i

		biggest_list.append((imgs[biggest_index], biggest))

	sorted_biggest = sorted(biggest_list, key=lambda tup: tup[1], reverse=True)
	# print(sorted_biggest[:10])
	projects = [x[0] for x in sorted_biggest][:num]
	# print(projects[:10])



	# with open(r'most_hits_dic.pickle', 'wb') as out: 
	# 	cp.dump(biggest_dic, out)
	with open(r'biggest_list.pickle', 'wb') as out: 
		cp.dump(biggest_list, out)
	with open(r'projects.pickle', 'wb') as out: 
		cp.dump(projects, out)



def write_rfile(rout_path): 
	with open(r'cluster_counts.pickle', 'rb') as inp: 
		cluster_dic = cp.load(inp)
	with open(r'subgroups.pickle', 'rb') as inp: 
		subgroups = cp.load(inp)
	with open(r'projects.pickle', 'rb') as inp: 
		projects = cp.load(inp)


	with open(rout_path, 'w') as f: 
		write = csv.writer(f, delimiter=',')
		write.writerow([''] + subgroups[1:])

		for project in projects: 
			norm = [x/sum(cluster_dic[project][1:]) for x in cluster_dic[project][1:]]
			write.writerow([project] + norm)


def get_colors(no_phyla=False): 
	if no_phyla: 
		open('./no_phylum.txt', 'w').close()

	with open(r'img_project_dic.pickle', 'rb') as inp: 
		img_project_dic = cp.load(inp)
	with open(r'projects.pickle', 'rb') as inp: 
		projects = cp.load(inp)
	color_dic = {}

	for project in projects: 
		phylum = ''
		order = ''
		if isfile('../config/' + project + '.config'): 
			with open('../config/' + project + '.config', 'r') as f: 
				for line in f: 
					linelist = line.split(' ')
					if 'phylum' in linelist[0]: 
						phylum = linelist[1].strip().lower()
					if 'order' in linelist[0]: 
						order = linelist[1].strip().lower()
			if phylum == 'environmental': 
				color_dic[project] = order
			else: 
				color_dic[project] = phylum
		elif isfile('../new_config/' + project + '.config'): 
			with open('../new_config/' + project + '.config', 'r') as f: 
				for line in f: 
					linelist = line.split(' ')
					if 'phylum' in linelist[0]: 
						phylum = linelist[1].strip().lower()
					if 'order' in linelist[0]: 
						order = linelist[1].strip().lower()
			if phylum == 'environmental': 
				color_dic[project] = order
			else: 
				color_dic[project] = phylum
		else: 
			if no_phyla: 
				with open('./no_phylum.txt', 'a') as f: 
					write = csv.writer(f, delimiter=',')
					write.writerow([str(img_project_dic[project])] + [project])


	print(color_dic)
	with open(r'color_dic.pickle', 'wb') as out: 
		cp.dump(color_dic, out)

def fill_dic():
	with open(r'color_dic.pickle', 'rb') as inp: 
		color_dic = cp.load(inp)
	with open(r'no_phylum.txt', 'r') as f: 
		for line in f: 
			words = line.split(',')
			if words[2] == 'environmental': 
				color_dic[words[1]] = words[3].strip()
			elif words[2] != 'environmental': 
				color_dic[words[1]] = words[2].strip()
	with open(r'color_dic.pickle', 'wb') as out: 
		cp.dump(color_dic, out)



def write_colors(): 
	dic = {
	'soil':'green', 
	'terrestrial':'green', 
	'freshwater':'light blue',
	'marine':'dark blue',
	'thermal':'cyan',
	'engineered':'purple',
	'host-associated':'red'
	}
	
	with open(r'color_dic.pickle', 'rb') as inp: 
		color_dic = cp.load(inp)
	with open(r'projects.pickle', 'rb') as inp: 
		projects = cp.load(inp)

	print(color_dic)
	with open('rowsidecolors.txt', 'w') as out: 
		out.write('RowSideColors = c(\n')	
		for project in projects: 
			if project in color_dic: 
				env = color_dic[project]
				if env in dic: 
					out.write('  rep("' + dic[env] + '", 1),\n')
				else: 
					out.write('  rep("' + 'grey' + '", 1),\n')
			else: 
				out.write('  rep("' + 'dark blue' + '", 1),\n')
		out.write('),\n')


def generate_heatmap(): 
	command = 'R CMD BATCH heatmap_all.R'
	status = subprocess.call(command, shell=True)

def color_analysis(): 
	dic = {
	'soil':'green', 
	'terrestrial':'green', 
	'freshwater':'light blue',
	'thermal':'cyan', 
	'marine':'dark blue',
	'engineered':'purple',
	'host-associated':'red'
	}

	with open(r'color_dic.pickle', 'rb') as inp: 
		color_dic = cp.load(inp)

	print(color_dic)
	print(len(color_dic))

	for key in color_dic: 
		if color_dic[key] not in dic: 
			print(key, color_dic[key])


def print_titles(): 
	with open(r'projects.pickle', 'rb') as inp: 
		projects = cp.load(inp)
	with open(r'img_project_dic.pickle', 'rb') as inp: 
		img_project_dic = cp.load(inp)

	with open('../project_titles.txt', 'wb') as out: 
		write = csv.writer(out, delimiter = ',')

		for project in projects: 
			write.writerow([project] + [img_project_dic[project]])




				
def main(): 
	seq_path = '../proteins_that_were_hit.sequences'
	fasta_cut_path = '../hits_150_1000.faa' 
	cdhit_path = '../tools/cdhit/'

	project_path = '../files/genome-projects.csv'
	cluster_path = '../hits_150_1000_90.clstr'
	# table_path = '../example.table'
	table_path = '../results.table'

	rout_path = './data_all'

	# cut_length(seq_path, fasta_cut_path, 150, 1000)
	# cluster(cdhit_path, fasta_cut_path[:-4], 0.9, 5)

	# project_img_dic, img_project_dic = projectimg_dic(project_path, pickle_path)
	# project_hit_dic, id_cluster_dic = projecthit_dic(cluster_path)
	# projecthit_dic(cluster_path)
	# subgroups = get_subgroups(table_path)

	# parse_table(table_path)
	# choose_surveys(100)

	# write_rfile(rout_path)
	# get_colors()
	# fill_dic()
	# write_colors()
	# generate_heatmap()

	# color_analysis()
	print_titles()


if __name__ == '__main__':
	main()

