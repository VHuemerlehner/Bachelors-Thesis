# This script will create a predicted harmonic rhythm for a given melody and
# a .txt-file containing a 2X9 matrix of probabilities

import numpy as np
import csv
import sys
sys.path.insert(0, '/home/waldo/Desktop/Bachelors_Thesis/Analysis')
import analysis as a

print('Creating prediction for ' + sys.argv[1])
# Read in the probabilities: Get the string and put it into a format such that
# only numbers and colons remain, then split at the colons to get a list
# of number strings and convert this into a numpy array.
probs_file = open(sys.argv[2], 'r')
probs_str = probs_file.read()
probs_str = probs_str.replace('\n', '')
probs_str = probs_str.replace('  ', ' ')
probs_str = probs_str.replace('  ', ' ')
probs_str = probs_str.replace(' ', ',')
probs_str = probs_str.replace('[,', '[')
probs_str = probs_str.replace('[', '')
probs_str = probs_str.replace(']', '')
probs_list = probs_str.split(',')

# Transforming strings into floats
for i in range(len(probs_list)):
	probs_list[i] = float(probs_list[i])

# Creating a numpy array and reshaping
probs = np.array(probs_list)
probs = probs.reshape(2,9)
probs_file.close()

# Read in the music XML for which we want a new prediction
rows = []
with open(sys.argv[1], newline='') as file:
	# Read the dialect with a csv-Sniffer
	dialect = csv.Sniffer().sniff(file.read())
	# Reset positioning to beginning of file
	file.seek(0)
	# Read in the csv with the earlier found dialect
	reader = csv.reader(file, dialect)
	# For each row, if it is a bar, replace the delimiters in mr and mp
	for row in reader:
		if 'Bar' in row:
			row[2] = row[2].replace('[', '')
			row[2] = row[2].replace(']', '')
			row[2] = row[2].replace(',', '')
			row[3] = row[3].replace('[', '')
			row[3] = row[3].replace(']', '')
			row[3] = row[3].replace(',', '')
		# Then, append the row into a new list
		rows.append(row)

# Use own method to get 5 lists of harmonic rhythm, melodic rhythm, melody pitches,
# grouping information and time signatures
ana = a.splitintolists(rows)
hr = ana[0]
mr = ana[1]
mp = ana[2]
ts = ana[4]
# Get all the needed parameters
patana = a.patcomparison(hr, mr, ts)
coocc = patana[0]
sync = patana[1]
pitchanalysis = a.pitchana(mp, hr, mr, ts)
intervals = pitchanalysis[0]
contour = pitchanalysis[1]

#What we want: Overall percentage of hr on mr to be close to txt[0,1] (prob for
#hr given mr) distributed such that the most likely mr's receive them. Thus:
#Give likelihoods to all mr's, then choose the highest ones until percentage is
#reached.

# First, we need to restore actual timings, see also analysis
############ BIG CHANGE TO MAKE!
offsets = []
hr_offsets = []
possible = []
bar_count = 0
addendum = 0
for i in mr:
	addendum += (int(ts[bar_count].split('/')[0])/int(ts[bar_count].split('/')[1]))*4
	for j in i:
		m = float(j) + addendum
		offsets.append(float(m))
	bar_count += 1

addendum = 0
bar_count = 0
for i in hr:
	addendum += (int(ts[bar_count].split('/')[0])/int(ts[bar_count].split('/')[1]))*4
	for j in i:
		m = float(j) + addendum
		hr_offsets.append(float(m))
	bar_count += 1

if offsets[0] != 0:
	subtractor = offsets[0]
	for k in range(len(offsets)):
		offsets[k] -= subtractor

# #Restore actual timings for melodic rhythm by adding the numerator of the
# #TS for each bar to the offsets (hacky solution, but that's what you get for
# #not thinking projects through in the beginning...)
# bar_count = 0
# for i in range(len(offsets)-1):
# 	if offsets[i+1] <= offsets[i]:
# 		for j in range(i+1, len(offsets)):
# 			#Not as complicated as it seems: TS are stored as strings that
# 			#we now split at "/" and divide the numerator by the denominator,
# 			#then casting as integers and multiplying with 4 since our timings
# 			#are thought in 4ths
# 			offsets[j] += (int(ts[bar_count].split('/')[0])/int(ts[bar_count].split('/')[1]))*4
# 		bar_count += 1
#
# #Same bs for harmonic rhythm.
# bar_count = 0
# for i in range(len(hr_offsets)-1):
# 	if hr_offsets[i+1] <= hr_offsets[i]:
# 		for j in range(i+1, len(hr_offsets)):
# 			hr_offsets[j] += (int(ts[bar_count].split('/')[0])/int(ts[bar_count].split('/')[1]))*4
# 		bar_count += 1

print(offsets)
# print(hr)
# print(mr)
# print(hr_offsets)
# print(offsets)

# ####a contour change; a melody onset; unisons; steps; jumps; jumps bigger than or
# ####equal to an octave; low syncopation; medium syncopation; high syncopation.

likelihood = [None] * len(offsets)

# Sum the probabilities for each melody onset and all strong beats, and get the
# mean as the overall probability for that time.
for i in range(len(offsets)):
	summedprobs = 0

	#contour
	if contour[i] == 1:
		summedprobs += probs[0,0]
	else:
		summedprobs += probs[1,0]

	#interval
	if intervals[i] == 0:
		summedprobs += probs[0,2]
	elif intervals[i] <= 2:
		summedprobs += probs[0,3]
	elif intervals[i] <= 11:
		summedprobs += probs[0,4]
	else:
		summedprobs += probs[0,5]

	#syncopation
	if sync[i] <= 0.5:
		summedprobs += probs[0,6]
	elif sync[i] <= 1:
		summedprobs += probs[0,7]
	else:
		summedprobs += probs[0,8]

	#average
	likelihood[i] = summedprobs / 3

# Number of harmonies we want to set
target = int(len(offsets) * probs[0,1])

likelihood = np.array(likelihood)

# Get the indeces of the highest likelihoods by sorting the array and choosing
# only the last n indices.
indices = (likelihood).argsort()[:target]
indices.sort()

prediction = []

# Get the actual timings from the indices.
for i in indices:
	prediction.append(offsets[i])

#
# correct = []
#
# for i in range(len(hr_offsets)):
# 	if hr_offsets[i] in offsets:
# 		correct.append(offsets.index(hr_offsets[i]))


print('Writing file')
output = open(sys.argv[3], 'w')
output.write(str(prediction) + '\n' + str(hr_offsets))
output.close()
