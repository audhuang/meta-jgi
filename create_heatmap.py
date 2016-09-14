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
	str(int(thresh * 100)) + ' -c ' + str(thresh) + ' -n ' + str(c) + ' -M 16000 -d 0 -T 8'

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
				name = line.strip().split(' ')[1][1:10]
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

	with open(table_path, 'r') as f: 
		if line[0] != '#': 
			for line in f: 
				col = line.split()
				subgroup = col[2]
				name = col[0].split('|')[0]

				if name not in dic: 
					dic[name] = [[]] * len(subgroups)
				dic[name][subgroups.index[subgroup]].append(id_cluster_dic[col[0]])

	for key in dic: 
		cluster_dic[key][:] = [len(set(dic[key][i])) for i in len(subgroups)]

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


	biggest = []
	for key in project_img_dic: 
		biggest = 0
		biggest_index = 0
		imgs = project_img_dic[key]

		for i in range(len(imgs)): 
			num = len(set(project_cluster_dic[imgs[i]]))
			if num > biggest: 
				biggest = num
				biggest_index = i

		biggest.append((key, biggest, biggest_index))

	sorted_biggest = sorted(biggest, key=lambda tup: tup[1])
	projects = [x[0] for x in sorted_biggest][:num]


	# with open(r'most_hits_dic.pickle', 'wb') as out: 
	# 	cp.dump(biggest_dic, out)
	with open(r'biggest_list.pickle', 'wb') as out: 
		cp.dump(biggest, out)
	with open(r'sorted_biggest_list.pickle', 'wb') as out: 
		cp.dump(sorted_biggest, out)

	return projects


def write_rfile(projects, rout_path): 
	with open(r'cluster_counts.pickle', 'rb') as inp: 
		cluster_dic = cp.load(inp)
	with open(r'subgroups.pickle', 'rb') as inp: 
		subgroups = cp.load(inp)

	with open(rout_path, 'w') as f: 
		write = csv.writer(f, delimiter=',')
		write.writerow([''] + subgroups)

		for project in projects: 
			write.writerow([project] + cluster_dic[project])


def get_colors(projects): 
	with open(r'img_project_dic.pickle', 'rb') as inp: 
		img_project_dic = cp.load(inp)
	color_dic = {}

	for project in projects: 
		if isfile('../config/' + project + '.config'): 
			with open('../config/' + project + '.config', 'r') as f: 
				for line in f: 
				linelist = line.split(' ')
					if 'phylum' in linelist[0]: 
						color_dic[project] = linelist[1].strip().lower()
		elif isfile('../new_config/' + project + '.config'): 
			with open('../new_config/' + project + '.config', 'r') as f: 
				for line in f: 
				linelist = line.split(' ')
					if 'phylum' in linelist[0]: 
						color_dic[project] = linelist[1].strip().lower()
		else: 
			with open('../no_phylum.txt', 'a') as f: 
				write = csv.writer(f, delimiter='\t')
				write.writerow(img_project_dic[project])


	with open(r'color_dic.pickle', 'wb') as out: 
		cp.dump(color_dic, out)


def write_colors(): 
	dic = {'soil':'green'}
	with open(r'color_dic.pickle', 'rb') as inp: 
		color_dic = cp.load(color_dic, out)

	with open('rowsidecolors.txt', 'w') as out: 
		out.write('RowSideColors = c(\n')	
		for key in color_dic: 
			out.write('  rep("' + dic[color_dic[key]] + '", 1),\n')
		out.write('),\n')


def generate_heatmap(): 
	command = 'R CMD BATCH heatmap_all.R'
	status = subprocess.call(command, shell=True)


				
def main(): 
	seq_path = '../proteins_that_were_hit.sequences'
	fasta_cut_path = '../hits_50_1000.faa' 
	cdhit_path = '../tools/cdhit/'

	project_path = '../files/genome-projects.csv'
	cluster_path = '../hits_50_1000_90.clstr'
	# table_path = '../example.table'
	table_path = '../results.table'

	rout_path = './data_all'

	# cut_length(seq_path, fasta_cut_path, 50, 1000)
	# cluster(cdhit_path, fasta_cut_path[:-4], 0.9, 5)

	# project_img_dic, img_project_dic = projectimg_dic(project_path, pickle_path)
	# project_hit_dic, id_cluster_dic = projecthit_dic(cluster_path)
	projecthit_dic(cluster_path)
	# subgroups = get_subgroups(table_path)

	parse_table(table_path, subgroups)
	projects = choose_surveys(100)

	write_rfile(projects, rout_path)
	get_colors(projects)
	# generate_heatmap()


if __name__ == '__main__':
	main()

