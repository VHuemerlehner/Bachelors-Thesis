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

#counting variables TODO: documentation
all_mr = 0
all_probs = np.zeros((2,9))



###Idea: take grouping info to calculate number of bars.
def getMROffsets(mr, rows):
	for i in range(len(mr)):




def getHROffsets(hr):


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

	giant_list = analysis.splitintolists(rows)

	#giant_list contains hr, mr, mp, grp, ts in chronological lists
	# harmonic_rhythm = analysis.patfrequency(giant_list[0])
	# melodic_rhythm = analysis.patfrequency(giant_list[1])
	pattern_comparison = analysis.patcomparison(giant_list[0], giant_list[1], giant_list[4])
	pitch_analysis = analysis.pitchana(giant_list[2], giant_list[0], giant_list[1], giant_list[4])

	# For calculating syncopation thresholds only
	# sync.append(pattern_comparison[1])
	probabilities = analysis.probabilities(pitch_analysis[0], pitch_analysis[1],\
	pattern_comparison[0], pattern_comparison[1], giant_list[0], giant_list[1],\
	giant_list[4])

	# Get the probabilities for the entire idiom by weighting each pieces'
	# probabilities according to melody onsets and then averaging.

	offcount = len(giant_list[1])

	weighted_probs = probabilities * offcount

	all_probs = np.add(weighted_probs, all_probs)

	all_mr += offcount

	#file management, open file
	splitName = pieceName.split('.')
	noExtName = splitName[0]
	finalName = noExtName+'.txt'
	text_file = open(finalName, 'w')

	#write file
	text_file.write(str(probabilities) + '\n' + str(len(giant_list[1])))
	text_file.close()
	os.rename(currFolder+finalName, destFolder+finalName)

# 2X9 matrix with probabilities for one idiom
idiom_probs = all_probs / all_mr

# write file
print('Writing idiom file')
file = open('/home/waldo/Desktop/Bachelors_Thesis/Analysis/Probabilities/Idioms/' + 'Tango.txt', 'w')
file.write(str(idiom_probs))
file.close()

# For debugging and finding syncopation thresholds
# file = open('/home/waldo/Desktop/Bachelors_Thesis/Analysis/Output/Syncopation/' + 'Rebetika.txt', 'w')
# file.write(str(sync))
# file.close()
