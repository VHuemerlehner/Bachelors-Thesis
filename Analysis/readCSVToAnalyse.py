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

# BC_001_026900B_a1.txt.csv
# Calalang_Pater_Noster [Checked - Giannos].txt.csv

if len(sys.argv) < 3:
	sys.exit("readCSVToAnalyse.py: Not enough input arguments")

currFolder = sys.argv[1]
destFolder = sys.argv[2]

os.chdir(currFolder)
allDocs = glob.glob("*.csv")

if len(allDocs) < 1:
	sys.exit("readCSVToAnalyse.py: No CSV files there!")

sync = []

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
	# print('Melodic Rhythm')
	# print(giant_list[1])
	# print('Time Signatures')
	# print(giant_list[4])
	# print('Harmonic Rhythm\n')
	# print(harmonic_rhythm)
	pattern_comparison = analysis.patcomparison(giant_list[0], giant_list[1], giant_list[4])
	# print('\n\n\nPattern Comparison\n' + str(pattern_comparison))
	pitch_analysis = analysis.pitchana(giant_list[2], giant_list[0], giant_list[1], giant_list[4])

	sync.append(pattern_comparison[1])

	print('Writing into file...')
	#file management, open file
	splitName = pieceName.split('.')
	noExtName = splitName[0]
	finalName = noExtName+'.txt'
	text_file = open(finalName, 'w')

	#write file
	text_file.write(str(pitch_analysis) + '\n' + str(pattern_comparison))
	text_file.close()
	os.rename(currFolder+finalName, destFolder+finalName)

file = open('/home/waldo/Desktop/Bachelors_Thesis/Analysis/Output/Syncopation/' + 'Tango.txt', 'w')
file.write(str(sync))
file.close()
