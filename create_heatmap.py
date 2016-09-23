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
import cPickle as cp

def cut_length(seq_path, out, low, high): 
	'''
	Input: 
	  - fasta file path 
	  - output file path 
	  - smallest length of sequences to keep
	  - longest length of sequences to keep
	  
	Output:
	  none, writes to output fasta file path
	  
	Comments: 
	  - copies sequences from input fasta file, with length between the input 
	    low and high values, to the output fasta file path 
	'''
	# counts number of sequences that haven't been copied over
	cut = 0

	# copies accepted sequences to output fasta file path
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
	'''
	Input: 
	  - path to CDHIT program
	  - path to fasta file to be clustered WITHOUT .fasta or .faa extension
	  - CDHIT threshold as decimal
	  - CDHIT word size between 2 and 5, if threshold is 0.9 then this is 5
	    	see http://weizhongli-lab.org/lab-wiki/doku.php?id=cd-hit-user-guide

	Output:
	  none, writes CDHIT result files 
	  
	Comments: 
	  - runs CDHIT on sequences in fasta file and writes file to output file with
	    name fasta_path_threshold%.clstr
	    	e.g. if fasta_path = '../fasta and thresh=0.9, output = '../fasta_90.clstr'

	  - CDHIT command limits header length in clstr file to 100 characters which for JGI
	    should be the entire header
	'''
	command = cdhit_path + 'cd-hit -i ' + fasta_path + '.faa -o ' + fasta_path + '_'+ \
	str(int(thresh * 100)) + ' -c ' + str(thresh) + ' -n ' + str(c) + ' -M 16000 -d 100 -T 8'

	status = subprocess.call(command, shell=True)


def projectsurvey_dic(project_path): 
	'''
	Input: 
	  - path to csv file of projects downloaded from IMG database

	Output:
	  none, saves 2 dictionaries as pickle files: 
	  - ./project_survey_dic.pickle, dict of {project title : [survey IDs]}
	  - ./survey_project_dic.pickle, dict of {survey ID : 'project title'}
	  
	Comments: 
	  - parses csv file of studies to create 2 dicts: 
		  - project_survey_dic: maps project title to list of survey IDs
			  	useful since each project has multiple surveys and in the future we want 
			  	to choose the survey from each project with the most clusters
	  	  - survey_project_dic: lets us map each survey ID back to its project title
	  	    	useful for coloring rows of the heatmap by the project it came from

	  	    	# add URL 
	'''
	# initiate empty dicts
	project_survey_dic = {}
	survey_project_dic = {}

	# parse csv file of projects from JGI to fill dicts with relevant data
	with open(project_path, 'rb') as inp: 
		reader = csv.reader(inp, delimiter = ',')
		next(reader)
		for row in reader: 
			if row[15] != '': 
				links = row[15].split(' ')
				for link in links: 
					survey = link.split(',')[1][1:-2] 

					# project is key, survey ID list is value
					if row[7] not in project_survey_dic: 
						project_survey_dic[row[7]] = [str(survey)] 
					else: 
						project_survey_dic[row[7]].append(str(survey))

					# survey ID is key, project name is value
					if survey not in survey_project_dic: 
						survey_project_dic[survey] = str(row[7])

	
	# save dicts as pickle files
	with open(r'./pickles/project_survey_dic.pickle', 'wb') as out: 
		cp.dump(project_survey_dic, out)
	with open(r'./pickles/survey_project_dic.pickle', 'wb') as out: 
		cp.dump(survey_project_dic, out)



def cluster_dic(cluster_path): 
	'''
	Input: 
	  - path to CDHIT cluster file

	Output:
	  none, saves 2 dictionaries as pickle files: 
	  - ./id_cluster_dic.pickle, dict of {fasta ID: ['clusters']}
	  - ./survey_cluster_dic.pickle, dict of {survey ID : ['clusters']}
	  
	Comments: 
	  - parses the CDHIT cluster file to produce 2 dicts: 
	  	  - id_cluster_dic: maps specific fasta identifier to a list of clusters
	  	    that it is found in
		  	    useful for counting number of unique clusters a 
		  	    fasta sequence is found in for the heatmap cells 
	  	  - survey_cluster_dic: maps survey ID to a list of clusters that it's 
	  	    found in
		  	    useful for finding surveys found in the greatest number of
		  	    unique clusters when choosing rows to include in the heatmap
	'''

	# initiate empty dicts to hold data
	id_cluster_dic = {}
	survey_cluster_dic = {}

	# parse CDHIT output file to file dicts with data
	with open(cluster_path, 'r') as f: 
		cluster = -1
		for line in f: 
			# handle cluster number lines
			if line[0] == '>': 
				cluster = line.strip().split(' ')[-1]
			
			# handle sequence lines 
			else: 
				survey = line.strip().split(' ')[1][1:11] # survey id
				fid = line.strip().split(' ')[1][1:-3] # fasta id
				
				# map fasta identifier to string cluster number
				if fid not in id_cluster_dic: 
					id_cluster_dic[fid] = [cluster]
				else: 
					id_cluster_dic[fid].append(cluster) 

				# map survey id to string cluster number
				if survey not in survey_cluster_dic: 
					survey_cluster_dic[survey] = [cluster]
				else: 
					survey_cluster_dic[survey].append(cluster)


	# save dicts as pickle files
	with open(r'./pickles/id_cluster_dic.pickle', 'wb') as out: 
		cp.dump(id_cluster_dic, out)
	with open(r'./pickles/survey_cluster_dic.pickle', 'wb') as out: 
		cp.dump(survey_cluster_dic, out)


def get_subgroups(table_path): 
	'''
	Input: 
	  - path to HMMsearch results table file 

	Output:
	  - list of HMM/subgroup names found in the HMMsearch results, which is also saved as
	    a pickle file 
	  
	Comments: 
	  - parses the HMMsearch results table to obtain list of subgroups found there 
	  		useful because the list of subgroups will be used to count number of hits
	  		per subgroup later 
	  - saves subgroups list in 'subgroups.pickle'
	'''

	#initiate empty list to hold subgroup name strings 
	subgroups = []

	# parse HMMsearch table and when a new HMM name/subgroup is encountered, 
	# append it to the list
	with open(table_path, 'r') as f: 
		for i in range(3): 
			f.next()
		for line in f: 
			col = line.split()
			if line[0] != '#': 
				subgroup = col[2]
				if subgroup not in subgroups: 
					subgroups.append(subgroup)

	# save subgroup list as pickle 
	with open(r'./pickles/subgroups.pickle', 'wb') as out: 
		cp.dump(subgroups, out)
	
	return subgroups


def parse_table(table_path): 
	'''
	Input: 
	  - path to HMMsearch results table file 

	Output:
	none, saves 1 dictionary as pickle file: 
	  - ./survey_hit_counts.pickle, dict of {survey ID : [# unique clusters for each subgroup]}
	  
	Comments: 
	  - parses the HMMsearch results table and produces 2 dicts for heatmap construction: 
	  	  - survey_hit_counts: maps survey to number of unique clusters its hits were found in, for 
	  	    each subgroup HMM run against the metagenomic database 
	  	    	each entry in this dictionary corresponds straight-up to a row in the heatmap 
	  	    	e.g. if the subgroups are ['NfsA', 'NfsB', 'Hub', 'SagB'], an example 
	  	    		 survey_hit_counts dict pair is {3300002454 : [1, 0, 0, 24]}, which means 
	  	    		 that survey ID 330002454 had 1 unique cluster of hits for the NfsA HMM, 
	  	    		 0 unique hit clusters in NfsB and hub, and 24 unique hit clusters in SagB

	  	  - survey_hit_clusters: maps survey to list of nonunique clusters its hits were found in, 
	  	    for each subgroup HMM run against the metagenomic database (NOT SAVED)
	  	    	used to create survey_hit_counts dict
	  	  
	'''

	# retrieve dict of {id : ['clusters']} so as we parse HMMsearch table we can map each 
	# hit to the cluster it's in, in order to count the number of unique clusters for heatmap
	with open(r'./pickles/id_cluster_dic.pickle', 'rb') as inp: 
		id_cluster_dic = cp.load(inp)
	# retrieve list of subgroups in order to create dict values, which are number of hits
	# per subgroup for each survey 
	with open(r'./pickles/subgroups.pickle', 'rb') as inp: 
		subgroups = cp.load(inp)

	survey_hit_clusters = {} # dict of survey ID to list of hit clusters per subgroup
	survey_hit_counts = {} # dict of survey ID to # unique hit clusters per subgroup

	# each non-comment line of HMMsearch has a hit's fasta identifier and HMM name 
	with open(table_path, 'r') as f: 
		for line in f: 
			if line[0] != '#': 
				col = line.split() # split table line into list of column entries 
				subgroup = col[2] # HMM subgroup name is index 2
				survey = col[0].split('|')[0] # fastaID is index 0, survey is 1st part of ID

				# if a survey ID isn't in survey_hit_clsuters dict yet, initiate its value to 
				# empty list of lists for each subgroup, which will hold the hit clusters
				# the survey has in each subgruop
				if survey not in survey_hit_clusters: 
					survey_hit_clusters[survey] = [[] for i in subgroups]
				# if the hit was in the CDHIT result file, append the names of clusters it was 
				# found in to the list corresponding to the right subgroup HMM name in 
				# the survey's dict value 
				if id_cluster_dic.has_key(col[0].strip()): 
					for clu in id_cluster_dic[col[0].strip()]:
						survey_hit_clusters[survey][subgroups.index(subgroup)].append(clu)
				# some hits are found in multiple clusters so i just appended all of those
				# some hits in the HMMsearch results aren't in the cluster file because 
				# CDHIT didnt recognize it as a fasta sequence or it was outside the
				# length restrictions (50-1000aa) set earlier

	# we currently have a list of nonunique cluster names each survey had hits in for each 
	# subgroup. we now find the number of unique clusters each survey had hits in for each 
	# subgroup and add that data to the survey_hit_counts dict 
	for key in survey_hit_clusters: 
		survey_hit_counts[key] = []
		for i in range(len(subgroups)): 
			survey_hit_counts[key].append(len(set(survey_hit_clusters[key][i])))

	# save dict of survey to # unique clusters in pickle file
	with open(r'./pickles/survey_hit_counts.pickle', 'wb') as out: 
		cp.dump(survey_hit_counts, out)


def choose_surveys(number, chosen_surveys_path): 
	'''
	Input: 
	  - number of surveys or rows desired in the heatmap
	  - path to output list of chosen surveys to 

	Output:
	none, saves list of chosen surveys to input chosen_surveys_path
	  
	Comments: 
	  chooses, from each project, the survey with the greatest # of
	  unique hit clusters, then from this set of surveys

	  chooses top 'number' of surveys with the greatest number of 
	  unique hit clusters, saves the IDs of these surveys in a list, 
	  and saves list as pickle file at 'chosen_surveys_path'
	'''
	# retrieve dict which maps project to list of surveys
	with open(r'./pickles/project_survey_dic.pickle', 'rb') as inp: 
		project_survey_dic = cp.load(inp)
	# retrieve dict which maps survey to # cluster counts for each subgroup
	with open(r'./pickles/survey_cluster_dic.pickle', 'rb') as inp: 
		survey_cluster_dic = cp.load(inp)


	# initiate empty list of biggest survey from each project
	biggest_list = []
	
	# each key in project_survey_dic is a project, each value is a list of 
	# survey IDs. for each project, go through the list of survey IDs 
	# and append the ID with the most total unique clusters to biggest_list
	for key in project_survey_dic: 
		biggest = 0 # saves largest number unique clusters
		biggest_index = 0 # saves index of largest survey
		surveys = project_survey_dic[key] # list of surveys 

		# go through list of surveys and save index of ID with most total clusters
		for i in range(len(surveys)): 
			if surveys[i] in survey_cluster_dic: 
				num = len(set(survey_cluster_dic[surveys[i]]))
				if num > biggest: 
					biggest = num
					biggest_index = i

		# add tuple of (survey name, # clusters) to biggest_list
		biggest_list.append((imgs[biggest_index], biggest))

	# sort list of biggest surveys by their cluster counts 
	sorted_biggest = sorted(biggest_list, key=lambda tup: tup[1], reverse=True)
	
	# final list of surveys is top 'number' of biggest surveys
	surveys = [x[0] for x in sorted_biggest][:number]

	# savel ist of chosen surveys as pickle file 
	with open(chosen_surveys_path, 'wb') as out: 
		cp.dump(surveys, out)


def write_rfile(rout_path, chosen_surveys_path): 
	'''
	Input: 
	  - path to where heatmap data should be written 
	  - path to list of chosen surveys 

	Output:
	none, writes heatmap data to 'rout_path'
	  
	Comments: 
	  writes heatmap data entries to 'rout_path'. each row is a survey from 
	  list at chosen_surveys_path. each is a subgroup from list of subgroups. 
	  data values are normalized unique cluster counts per subgroup
	'''

	# retrieve dict which maps survey to number of unique surveys per subgroup
	with open(r'./pickles/survey_hit_counts.pickle', 'rb') as inp: 
		survey_hit_counts = cp.load(inp)
	# retrieve list of subgroups/HMMs 
	with open(r'./pickles/subgroups.pickle', 'rb') as inp: 
		subgroups = cp.load(inp)
	# retrieve list of chosen surveys
	with open(chosen_surveys_path, 'rb') as inp: 
		surveys = cp.load(inp)

	# first write to 'rout_path' list of subgroups in csv format. then for each survey,
	# write a row of survey ID followed by normalized cluster counts for each subgroup
	with open(rout_path, 'w') as f: 
		write = csv.writer(f, delimiter=',')
		write.writerow([''] + subgroups[1:])
		for survey in surveys: 
			if survey in survey_hit_counts: 
				norm = [x/sum(survey_hit_counts[survey][1:]) \
				for x in survey_hit_counts[survey][1:]]
				write.writerow([survey] + norm)
			else: 
				print('survey ID not found in dict survey_hit_counts: ', survey)


def get_colors_from_scrape(tiers, chosen_surveys_path): 
	'''
	Input: 
	  - list of classification levels to keep from 0-3 (e.g. [0, 1, 2] or [3])
	  - path to list of chosen surveys 

	Output:
	none, saves dictionary of {survey ID : ['selected metadata']} for heatmap 
	chosen surveys 
	  
	Comments: 
	  saves relevant metadata for chosen surveys into color_dic, which is saved
	  as pickle file

	  tier 0: ecosystem (e.g. environmental, host-associated, engineered)
	  tier 1: ecosystem category (e.g. aquatic, terrestrial)
	  tier 2: ecosystem subtype (e.g. oceanic)
	  tier 3: ecosystem type (e.g. marine)

	  choose tiers based on what you want the rows of the heatmap to be colored by
	'''

	# retrieve dict of {survey : ['metadata']}
	with open('./pickles/survey_meta_dic.pickle', 'rb') as inp: 
		meta_dic = cp.load(inp)
	# retrieve list of chosen survey IDs
	with open(chosen_surveys_path, 'rb') as inp: 
		surveys = cp.load(inp)
	
	# initiate empty dict to store {chosen survey : ['selected metadata']}
	color_dic = {}
	
	# for each chosen survey, store metadata from desired tiers in dict
	for survey in surveys: 
		meta = meta_dic[survey]
		color_dic[survey] = [meta[x] for x in tiers]

	# save color dict as pickle file 
	with open(r'./pickles/color_dic.pickle', 'wb') as out: 
		cp.dump(color_dic, out)



def get_colors_from_file(chosen_surveys_path, no_phyla=False): 
	'''
	Input: 
	  - path to list of chosen surveys 
	  - whether or not surveys without metadata info should be written to a 
	    fresh text file './no_phylum.txt'
	    	False: written to fresh file 
	    	True: appended to existing file 

	Output:
	none, saves dictionary of {survey ID : ['relevant metadata']} 
	for heatmap chosen surveys 
	  
	Comments: 
	parses downloaded config files in folders '../config' and '../new_config/'
	into metadata list 

	if ecosystem is 'environmental', color by ecosystem category (aquatic, terrestrial, air)
	if ecosystem is 'host-associated' or 'engineered', color by ecosystem
	'''
	# toggle whether or not to write surveys with no metadata to fresh file 
	if no_phyla: 
		open('./no_phylum.txt', 'w').close()

	# retrieve dict of survey to project title 
	with open(r'./pickles/survey_project_dic.pickle', 'rb') as inp: 
		survey_project_dic = cp.load(inp)
	# retrieve list of chosen survey IDs
	with open(chosen_surveys_path, 'rb') as inp: 
		surveys = cp.load(inp)
	
	# initiate empty dictionary
	color_dic = {}

	# for each chosen project parse config files for top two tiers of 
	# metadata and save in dictionary
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


	# save color dic as pickle 
	with open(r'./pickles/color_dic.pickle', 'wb') as out: 
		cp.dump(color_dic, out)


def write_colors(): 
	'''
	Input: 
	none

	Output:
	none, writes to './rowsidecolors.txt'
	  
	Comments: 
	writes row colors to './rowsidecolors.txt' for each chosen survey in heatmap. 
	contents of './rowsiecolors.txt' should then be copied to R script. 

	NOTE: last written color row has extra comma at the end that needs to be removed 
	before text is copied into R code

	maps environment to color based on dic below. if the environment is unclassified
	or not in the dic, color row grey 

	'''

	dic = {
	'soil':'green', 
	'terrestrial':'green', 
	'freshwater':'light blue',
	'marine':'dark blue',
	'thermal':'cyan',
	'engineered':'purple',
	'host-associated':'red'
	}
	
	# retrieve dict mapping chosen survey ID to relevant metadata
	with open(r'./pickles/color_dic.pickle', 'rb') as inp: 
		color_dic = cp.load(inp)
	
	# for each row, write color to 'rowsidecolors.txt' in R code format 
	with open('rowsidecolors.txt', 'w') as out: 
		out.write('RowSideColors = c(\n')	
		for key in color_dic: 
			env = color_dic[project]
			if env in dic: 
				out.write('  rep("' + dic[env] + '", 1),\n')
			else: 
				out.write('  rep("' + 'grey' + '", 1),\n')
		out.write('),\n')


def parse_surveys(parse_path, chosen_surveys_path): 
	'''
	Input: 
	  - path to downloaded csv file of IMG projects to parse 
	  - 

	Output:
	none, saves list of chosen surveys as pickle file
	  
	Comments: 
	parses excel file of projects downloaded from IMG database for list of
	survey IDs, which is saved as a pickle file to chosen_surveys_path

	'''
	studies = []
	surveys = []
	with open(parse_path, 'r') as f: 
		reader = csv.reader(f, delimiter='\t')
		next(reader)
		for row in reader: 
			img = row[6]
			surveys.append((img, row[3]))

	with open(chosen_surveys_path, 'wb') as out: 
		cp.dump(surveys, out)


def write_custom_colors(): 
	'''
	Input: 
	none

	Output:
	none, writes to './rowsidecolors_engineered.txt'
	  
	Comments: 
	writes row colors to './rowsidecolors.txt' for each chosen survey in heatmap. 
	contents of './rowsidecolors.txt' should then be copied to R script. 

	NOTE: last written color row has extra comma at the end that needs to be removed 
	before text is copied into R code

	maps survey to color based on project title, so surveys from the same project have
	the same row colors 

	'''
	with open(r'./pickles/engineered_projects.pickle', 'rb') as inp: 
		projects = cp.load(inp)

	titles = [x[1] for x in projects]
	unique = list(set(titles))

	dic = {
	0 : 'red', 
	1 : 'orange', 
	2 : 'yellow', 
	3 : 'green', 
	4 : 'cyan', 
	5 : 'blue', 
	6 : 'purple', 
	7 : 'pink', 
	8 : 'brown', 
	9 : 'black'
	}


	with open('rowsidecolors_engineered.txt', 'w') as out: 
		out.write('RowSideColors = c(\n')	
		for title in titles: 
			out.write('  rep("' + dic[unique.index(title)] + '", 1),\n')
		out.write('),\n')
	
	for i in range(9): 
		print(i, unique[i]) 


def fill_dic():
	with open(r'./pickles/color_dic.pickle', 'rb') as inp: 
		color_dic = cp.load(inp)
	with open(r'no_phylum.txt', 'r') as f: 
		for line in f: 
			words = line.split(',')
			if words[2] == 'environmental': 
				color_dic[words[1]] = words[3].strip()
			elif words[2] != 'environmental': 
				color_dic[words[1]] = words[2].strip()
	with open(r'./pickles/color_dic.pickle', 'wb') as out: 
		cp.dump(color_dic, out)


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

	with open(r'./pickles/color_dic.pickle', 'rb') as inp: 
		color_dic = cp.load(inp)

	print(color_dic)
	print(len(color_dic))

	for key in color_dic: 
		if color_dic[key] not in dic: 
			print(key, color_dic[key])


def print_titles(): 
	with open(r'./pickles/projects.pickle', 'rb') as inp: 
		projects = cp.load(inp)
	with open(r'img_project_dic.pickle', 'rb') as inp: 
		img_project_dic = cp.load(inp)

	with open('../project_titles.txt', 'wb') as out: 
		write = csv.writer(out, delimiter = ',')

		for project in projects: 
			write.writerow([project] + [img_project_dic[project]])




				
def main(): 
	
	project_path = '../files/genome-projects.csv'
	cdhit_path = '../tools/cdhit/'
	seq_path = '../proteins_that_were_hit.sequences'
	fasta_cut_path = '../hits_150_1000.faa' 

	cluster_path = '../hits_150_1000_90.clstr'
	table_path = '../results.table'
	chosen_surveys_path = './pickles/projects.pickle'
	rout_path = './data' 

	# cut_length(seq_path, fasta_cut_path, 150, 1000)
	# cluster(cdhit_path, fasta_cut_path[:-4], 0.9, 5)

	projectsurvey_dic(project_path)
	cluster_dic(cluster_path)
	subgroups = get_subgroups(table_path)

	parse_table(table_path)
	choose_surveys(100, chosen_surveys_path)
	
	# write_rfile(rout_path, chosen_surveys_path)
	# get_colors()

	# write_custom_rfile(rout_path, chosen_surveys_path)
	# parse_surveys(parse_chosen_surveys_path, chosen_surveys_path)
	# fill_dic()


if __name__ == '__main__':
	main()

