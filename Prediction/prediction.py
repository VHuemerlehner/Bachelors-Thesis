# This script will create a predicted harmonic rhythm for a given melody and
# a .txt-file containing a 2X9 matrix of probabilities

import numpy as np
import csv
import sys
sys.path.insert(0, '/home/waldo/Desktop/Bachelors_Thesis/Analysis')
import analysis as a

# Check number of input arguments
if len(sys.argv) != 5:
	sys.exit('Prediction.py: I need exactly 5 input arguments (myself, a musicXML, its conditional probabilities, its exact offsets and a target file')

print('Creating prediction for ' + sys.argv[1])

# Read in the probabilities: Get the string and put it into a format such that
# only numbers and commata remain, then split at the commata to get a list
# of number strings and convert this into a numpy array.
probs_file = open(sys.argv[2], 'r')
probs_str = probs_file.read()
probs_str = probs_str.replace('\n', '')
probs_str = probs_str.replace('  ', ' ')
probs_str = probs_str.replace('  ', ' ')
probs_str = probs_str.replace('[ ', '[')
probs_str = probs_str.replace('[', '')
probs_str = probs_str.replace(']', '')
probs_str = probs_str.replace(' ', ',')
probs_str = probs_str.replace(',,', ',')
if probs_str[-1].isdigit() == False:
	probs_str = probs_str[:-1]
probs_list = probs_str.split(',')

# Transforming strings into floats
for i in range(len(probs_list)):
	probs_list[i] = float(probs_list[i])

# Creating a numpy array and reshaping
probs = np.array(probs_list)
probs = probs.reshape(2,9)
probs_file.close()

# Initialising offset-lists
offsets = []
hr_offsets = []
# Read in the offsets, splitting at the line boundary
off_file = open(sys.argv[3], 'r')
off_str = off_file.read()
off_str = off_str.split('\n')
# Cut off the brackets, split the rest at commata and convert to float
for i in off_str[0][1:-1].split(','):
	offsets.append(float(i))
for i in off_str[1][1:-1].split(','):
	hr_offsets.append(float(i))

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
# Initialise likelihood-list
likelihood = [None] * len(offsets)

# Sum the probabilities for each melody onset, and get the
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

# Create a copy so we don't lose the old info
offsetcopy = list(offsets)

# Add strong beats as possible further harmony onsets, if not yet in there
for i in range(int(offsets[-1])):
	if i not in offsets:
		offsets.append

# Sort the new list
offsets = sorted(offsets)

# Initialise longer likelihood list
longlikelihood = [None] * len(offsets)

# Copy old values, for new ones, assign the probability given the absence of
# a melody event (further improvement may result from using adjacent syncopation
# and interval values)
for i in range(len(offsets)):
	if i in offsetcopy:
		longlikelihood[i] = offsetcopy.index(i)
	else:
		longlikelihood[i] = probs[1,1]

# Number of harmonies we want to set
target = int(len(offsetcopy) * probs[0,1]) + int((len(offsets) - len(offsetcopy)) * probs[1,1])

# Convert the list into a numpy array for sorting
longlikelihood = np.array(longlikelihood)

# Get the indeces of the highest likelihoods by sorting the array and choosing
# only the last n indices.
indices = (longlikelihood).argsort()[:target]
indices.sort()

# Initialise prediction list
prediction = []

# Get the actual timings from the indices.
for i in indices:
	prediction.append(offsets[i])

# For calculating percentages of correct guesses
success = 0
for i in prediction:
	if i in hr_offsets:
		success += 1

# Percentage of actual events correctly predected
percent = success/len(hr_offsets)
# Percentage of predicted events that hit an actual event
otherway = success/len(prediction)
# Jaccard distance between the two sets
jd = len((set(prediction) & set(hr_offsets)))/len((set(prediction) | set(hr_offsets)))

# Create the string to be written into the file
tmpStr = str(prediction) + '\n' + str(hr_offsets) + '\n' + 'Jaccard distance of\
 the two sets: ' + str(jd) + '\nPercentage of actual\
 harmonic rhythmic events hit: ' + str(percent) + '\nPercentage of set rhythmic\
 events that hit an actual rhythmic event: ' + str(otherway) + '\nEvents \
predicted: ' + str(len(prediction)) + '\nActual events: ' + str(len(hr_offsets))

# File printing
print('Writing file')
output = open(sys.argv[4], 'w')
output.write(tmpStr)
output.close()
