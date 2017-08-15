# -*- coding: utf-8 -*-
"""
@author: Valentin Huemerlehner
"""
#This script analyses .csv-files given in the following format:
#Category (TS; Grp; Bar) | Harmonic rhythm offsets | Melody offsets | Melody pitches
#String | String(Float) | String(List(Float)) | String(List(Int))

import csv
import analysis
import sys
import os
import glob
import numpy as np


if len(sys.argv) < 3:
	sys.exit("readCSVToAnalyse.py: Not enough input arguments")

currFolder = sys.argv[1]
destFolder = sys.argv[2]

os.chdir(currFolder)
allDocs = glob.glob("*.csv")

if len(allDocs) < 1:
	sys.exit("readCSVToAnalyse.py: No CSV files there!")

# For calculating syncopation thresholds only
# sync = []

# Counting variables for the idiom probabilities
all_mr = 0
all_probs = np.zeros((2,9))

for pieceName in allDocs:
	print('Analysing piece: ' + pieceName + '...')
	rows = []
	with open(currFolder+pieceName, newline='') as file:
		dialect = csv.Sniffer().sniff(file.read())
		file.seek(0)
		reader = csv.reader(file, dialect)
		for row in reader:
			if 'Bar' in row:
				row[2] = row[2].replace('[', '')
				row[2] = row[2].replace(']', '')
				row[2] = row[2].replace(',', '')
				row[3] = row[3].replace('[', '')
				row[3] = row[3].replace(']', '')
				row[3] = row[3].replace(',', '')
			rows.append(row)
	# Get harmonic rhythm, melodic rhythm, melody pitches and time signatures
	giant_list = analysis.splitintolists(rows)
	hr = giant_list[0]
	mr = giant_list[1]
	mp = giant_list[2]
	ts = giant_list[4]

	# Get cooccurences and syncopation
	pattern_comparison = analysis.patcomparison(hr, mr, ts)
	# Get intervals and contour
	pitch_analysis = analysis.pitchana(mp, hr, mr, ts)

	# For calculating syncopation thresholds only
	# sync.append(pattern_comparison[1])

	# Get the probabilities from the above calculated parameters
	probabilities = analysis.probabilities(pitch_analysis[0], pitch_analysis[1],\
	pattern_comparison[0], pattern_comparison[1], giant_list[0], giant_list[1],\
	giant_list[4])

	# Get the probabilities for the entire idiom by weighting each pieces'
	# probabilities according to melody onsets and then averaging.
	# For this, we first need a proper count of all mr events.
	offsets = []
	for i in giant_list[1]:
		for j in i:
			offsets.append(j)
	offcount = len(offsets)

	# Probabilities get weighted accordingly
	weighted_probs = probabilities * offcount

	# And added to the overall probabilities
	all_probs = np.add(weighted_probs, all_probs)

	# For later averaging
	all_mr += offcount

	# File management, open file
	splitName = pieceName.split('.')
	noExtName = splitName[0]
	finalName = noExtName+'.txt'
	text_file = open(finalName, 'w')

	# Write file
	text_file.write(str(probabilities) + '\n' + str(len(giant_list[1])))
	text_file.close()
	os.rename(currFolder+finalName, destFolder+finalName)

# 2X9 matrix with probabilities for one idiom, averaging over all pieces
idiom_probs = all_probs / all_mr

# Write idiom file
print('Writing idiom file')
file = open('/home/waldo/Desktop/Bachelors_Thesis/Analysis/Probabilities/Idioms/' + 'Tango.txt', 'w')
file.write(str(idiom_probs))
file.close()

# For debugging and finding syncopation thresholds
# file = open('/home/waldo/Desktop/Bachelors_Thesis/Analysis/Output/Syncopation/' + 'Rebetika.txt', 'w')
# file.write(str(sync))
# file.close()
