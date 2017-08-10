# This script will create a predicted harmonic rhythm for a given melody and
# a .txt-file containing a 2X9 matrix of probabilities

import analysis as a
import numpy as np
import sys

# Read in the probabilities
probs_file = open(sys.argv[2], 'r')
probs = np.loadtxt(probs_file)

with open(sys.argv[1], newline='') as file:
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

ana = a.splitintolists(rows)
ana[0] are hr; ana[1] are mr; ana[4] are ts
hr = ana[0]
mr = ana[1]
mp = ana[2]
ts = ana[4]
patana = a.patcomparison(hr, mr, ts)
coocc = patana[0]
sync = patana[1]
pitchanalysis = a.pitchana(mp, hr, mr, ts)
intervals = pitchanalysis[0]
contour = pitchanalysis[1]
# TODO:
# probs = other file

#What we want: Overall percentage of hr on mr to be close to txt[0,1] (prob for
#hr given mr) distributed such that the most likely mr's receive them. Thus:
#Give likelihoods to all mr's, then choose the highest ones until percentage is
#reached.

# ####a contour change; a melody onset; unisons; steps; jumps; jumps bigger than or
# ####equal to an octave; low syncopation; medium syncopation; high syncopation.

likelihood = [] * len(mr)

# Sum the probabilities for each melody onset, and get the mean as the Overall
# probability for this onset.
for i in range(len(mr)):
	summedprobs = 0

	#contour
	if contour[i] == 1:
		summedprobs += probs[0,0]
	else:
		summedprobs += probs[0,1]

	#interval
	if intervals[i] == 0:
		summedprobs += probs[2,0]
	elif intervals[i] <= 2:
		summedprobs += probs[3,0]
	elif intervals[i] <= 11:
		summedprobs += probs[4,0]
	else:
		summedprobs += probs[5,0]

	#syncopation
	if syncopation[i] <= 0.5:
		summedprobs += probs[6,0]
	elif syncopation[i] <= 1:
		summedprobs += probs[7,0]
	else:
		summedprobs += probs[8,0]

	#average
	likelihood[i] = summedprobs/3

# Number of harmonies we want to set
target = int(len(mr) * probabilities[1,0])

# Get the indeces of the highest likelihoods by sorting the array and choosing
# only the last n indices.
indices = (-likelihood).argsort()[:target]
