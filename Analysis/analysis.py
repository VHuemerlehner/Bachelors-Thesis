# -*- coding: utf-8 -*-
"""
@author: Valentin Huemerlehner
"""
import numpy as np

#Our input: A list with a list for each row of the .csv, containing either:
#TS - 3/4 OR Grp - 0.0 OR - Bar - (Harmonic Rhythm) 0 2  - cont.
#(Melodic Rhythm) 0 1 2 3 - (Pitches) 66 68 70 71

#The following function creates five lists of equal length: tsinf, grpinf
#hrinf, mrinf and mpinf. Each of them contains for each bar in sequence: Time
#Signature, grouping (1 = beginning of group, 2 = intermediate, 3 = ending)
#, harmonic rhythm, melodic rhythm, or melody pitches respectively.

def splitintolists(data):
	#We need five lists and two counting variables
	hrinf = []
	mrinf = []
	mpinf = []
	grpinf = []
	tsinf = []
	tsstring = ''
	grpint = 0

	#Iterating over the entire data
	for i in range(len(data)):
		#If we find a new TS, change the counting variable accordingly
		if data[i][0] == 'TS':
			tsstring = data[i][1]
		#If we find a new Grouping boundary, set grouping info to 1
		elif data[i][0] == 'Grp':
			grpint = 1
		#Now the complicated part: If we find a bar pattern, add it to the
		#lists and add the TS to the list. Change Grouping info accordingly:
		#If the next info in data is a grouping boundary, set to 3; if there
		#is a TS in between, but no bar, also set to 3; if it is a TS and
		#a bar, set it to 2; if the next data point is a bar, set it to 2;
		#If we are at the end of our data, set to 3; If we just had a grouping
		#boundary, leave the counting variable at 3 or 1, if it is a 2, change
		#to 1 (Explanation: We consider a group ending to be more significant
		#than a group beginning, should they occur at the same time (meaning
		#that the group is only one bar long), so the priority is: 3-1-2).
		elif data[i][0] == 'Bar':
			hrinf.append(data[i][1])
			mrinf.append(data[i][2])
			mpinf.append(data[i][3])
			tsinf.append(tsstring)
			if len(data)>i+1:
				if data[i+1][0] == 'Grp':
					grpint = 3
				elif data[i+1][0] == 'TS':
					if data[i+2][0] == 'Grp':
						grpint = 3
					elif data[i+2][0] == 'Bar':
						grpint = 2
				elif data[i+1][0] == 'Bar':
					grpint = 2
			else:
				grpint = 3
			if data[i-1][0] == 'Grp':
				if grpint == 2:
					grpint = 1
			grpinf.append(grpint)

	#Convert hrinf, mrinf and mpinf from string to tuple of 'floats':
	#Find all one-letter words (=integers) in hrinf and add '.0' behind them.
	for i in range(len(hrinf)):
		for word in hrinf[i].split():
			if len(word) == 1:
				place = hrinf[i].find(word) + 1
				temp = hrinf[i]
				hrinf[i] = temp[:place] + '.0' + temp[place:]
		hrinf[i] = list(hrinf[i].split())
		mrinf[i] = list(mrinf[i].split())
		mpinf[i] = list(mpinf[i].split())

	#Write it all in one list so we only hand around one object
	returnlist = []
	returnlist.append(hrinf)
	returnlist.append(mrinf)
	returnlist.append(mpinf)
	returnlist.append(grpinf)
	returnlist.append(tsinf)
	return returnlist


#-------------------------------------------------------------------------------


# The following function compares melodic and harmonic rhythmic patterns:
# It counts the number of cooccurring onsets, gives a percentage for each
# melodic and harmonic overall onsets and measures the difference in number
# of onsets in each bar. Output: [cooccurences abs, per measure, percentage of
# harmony onsets, percentage of melody onsets, absolute difference between
# number of melody and harmony onsets, same per measure, syncopation]


def patcomparison(hr, mr, ts):
	# Initialising variables
	results = []
	coocc = 0
	honsets = 0
	monsets = 0
	# Since there are as many harmonic patterns as melodic ones, iterate
	# over one list and simply count the number of elements in all the lists
	# inside it. Then check if in one pattern (which can be maximally one bar
	# long, thus never repeating the same number within itself) both lists show
	# the same number, meaning that harmony and melody cooccur.
	for i in range(len(hr)):
		honsets += len(hr[i])
		monsets += len(mr[i])
		for k in hr[i]:
			for l in mr[i]:
				 if k == l:
					 coocc += 1

	# Syncopation measure: Weighted Note-to-Beat Distance.
	# Algorithm: Each note has a minimal distance to a strong beat (e.g. an
	# eighth in a 4 fourths meter would have a distance of 1/2).
	# If this distance is 0 for x, then D(x)=0; if it is non-zero and the note
	# stops before or at the next strong beat, D(x)=1/(T(x)); if it is non-zero
	# and the note stops after the next strong beat, but not later than the
	# following one, D(x)=2/(T(x)). If it ends even later, D(x)=1/(T(x))
	# Take the average of all notes in a rhythm to get the WNBD.
	# See also the thesis on this topic.
	# In code more like: If on strong beat: 0; else: if ends between next two
	# strong beats, 2/T(x); else: 1/T(x)
	# Sum all these, divide by number of notes.
	# Do this for each pattern, add the result times the number of notes.

	wnbdList = []
	for i in range(len(mr)):
		# Write one pattern into a new list
		onsets = mr[i]
		# In case the bar is empty of melody notes, skip it.
		if onsets != []:

			# turn list from str into float
			for m in range(len(onsets)):
				onsets[m] = float(onsets[m])
			number = len(onsets)
			distance = 0
			# Note down the strong beats of the pattern (may be different each bar,
			# so we need to do it for each pattern)
			strong = []
			# The denominator of the time signature
			denom = ts[i].split('/')[1]
			# 0 is always the first strong beat
			beat = 0
			# which is then incremented depending on the denominator: Our rhythm
			# onsets are calculated in fourths, therefore, a denominator of 4 needs
			# to increment by 1, a denominator of 2 by 2, one of 8 by 0.5 etc.
			# This is achieved by taking the reciprocal value of denominator/4.
			incr = 1/(int(denom)/4)
			# Add strong beats as often as the numerator tells us.
			for j in range(int(ts[i].split('/')[0])):
				strong.append(beat)
				beat += incr

			# Loop until the last onset in the pattern, which is treated differently
			# Check, if pattern is longer than one beat, else only do the last
			# onset actions
			if len(onsets) > 1:

				for k in range(len(onsets) - 1):
					dtn = 0
					dtta = 0
					if onsets[k] in strong:
						distance += 0
					else:
						# Distance to next strong beat (no matter the direction):
						# Minimum of the differences between the onset and all strong
						# beats, absolute value so direction does not matter
						dtb = min(abs(onsets[k] - l) for l in strong)
						# print(dtb)
						for l in strong:
							if l > onsets[k]:
								# Distance to the next occurring beat (forwards)
								dtn = l - onsets[k]
								# Distance to two beats ahead
								if l < strong[-1]:
									dtta = dtn + incr
								break
						# If the offbeat note stops between the next two strong beats,
						# the distance measure added is doubled
						if ((onsets[k+1] - onsets[k]) > dtn) and ((onsets[k+1] - onsets[k]) <= dtta):
							distance += 2/dtb
						else:
							distance += 1/dtb
			# Treat the last onset differently (assume it ends on the pattern ending)
			# need to reset distances
			dtn = 0
			dtta = 0
			last_onset = onsets[-1]
			# If on a strong beat, ignore
			if last_onset in strong:
				distance += 0
			# Else assume it ends the latest on the pattern ending
			else:
				# Get minimal distance to beat
				dtb = min(abs(last_onset - l) for l in strong)
				# Get distance to following strong beat (if applicable)
				followed = False
				for l in strong:
					if l > last_onset:
						followed = True
						dtn = l - last_onset
						dtta = dtn + incr
						# Get the next beat's index (no duplicates, so this works)
						ind = strong.index(l)
						break
				# If the pattern ending is between 1 and 2 beats after the onset,
				# double the distance measure.
				if followed:
					if (ind <= len(strong) - 1):
						distance += 2/dtb
					else:
						distance += 1/dtb
				else:
					distance += 1/dtb

			# In the end, divide the pattern's distance measure by its onset count
			wnbd = distance/number
			# And add it to the distance-list once for each note in the pattern
			for i in range(number):
				wnbdList.append(wnbd)
		else:
			pass

	# We only need the percentage of cooccurences on melody onsets as a
	# conditional probability and the wnbD measure.
	results.append(coocc/monsets)
	results.append(wnbdList)
	return results

#-------------------------------------------------------------------------------

#This function analyses the melody in terms of pitch: It extracts its contour,
#i.e. when it rises or falls and calculates a measure for movement by adding up
#the distances between (time-)adjacent pitches. Another idea might be to scale
#pitches in terms of their relation (i.e. octave/unison score low, septs and
#tritones very high) and add this up. This can then be correlated to the number
#of harmony changes in the corresponding bar/piece.
def pitchana(mp, hr, mr, ts):

	# Initialising result list, helper lists and counting variables
	results = []
	pitches = []
	offsets = []
	hr_offsets = []
	bar_count = 0
	addendum = 0

	# First, we need to get all pitches into one long list of integers, same
	# with their offsets and the harmonic rhythm offsets, those as floats
	# because they contain .5 values and we actually do maths on them
	for i in mp:
		for j in i:
			pitches.append(int(j))

	# Melodic rhythm
	for i in mr:
		# What we need to add is determined by the time signature: take its
		# numerator divided by the denominator (splitting the string at the '/'
		# will give you those) and then multiply by 4 since we calculate in base
		# fourth (by which I mean fourths are our unit)
		addendum += (int(ts[bar_count].split('/')[0])/int(ts[bar_count].split('/')[1]))*4
		# Then add this to all following patterns
		for j in i:
			m = float(j) + addendum
			offsets.append(float(m))
		# Go to the next bar to get the correct time signature
		bar_count += 1

	# Harmonic rhythm
	# Reset the two counting variables
	addendum = 0
	bar_count = 0
	# Same thing for harmonic rhythm, see above
	for i in hr:
		addendum += (int(ts[bar_count].split('/')[0])/int(ts[bar_count].split('/')[1]))*4
		for j in i:
			m = float(j) + addendum
			hr_offsets.append(float(m))
		bar_count += 1

	# Since for some reason, melodic rhythm sometimes starts with non-zero
	# values while harmonic rhythm always starts with 0, we need to adapt by
	# subtracting the corresponding number from all melodic offsets
	if offsets[0] != 0:
		subtractor = offsets[0]
		for k in range(len(offsets)):
			offsets[k] -= subtractor

	# Initialising more variables: lists for results
	intervals = [None] * (len(pitches))
	contour = [None] * (len(pitches))
	intervals_abs = [None] * (len(pitches))

	# Given interval size, how probable are harmonic rhythmic events? I counted
	# all intervals separately in the beginning, but because of the lack of
	# more data, I toned it down to the four categories of unison, step, jump
	# and jump equal or bigger to/than an octave. Direction was also left out.
	# In the end I decided to count the hr cooccurences with the intervals
	# in the following method "probabilities", thus much of the following code
	# is unnecessary and therefore commented out.

	# interval_counter = []
	# intervals_up = [0] * 14
	# intervals_down = [0] * 14
	# interval_abs_counter = [0] * 14
	# intervals_up_change = [0] * 14
	# intervals_down_change = [0] * 14
	# intervals_abs_change = [0] * 14

	# 'contour' extracts only the direction of
	# movement, 'intervals_abs' only the amount of movement

	# First, we need to get all pitches into one list to iterate through.
	# The first interval is always 0, since there is no movement to be found.
	intervals[0] = 0
	# There will always be one less interval than notes because you need two
	# notes to relate them.
	for i in range(len(pitches)-1):
		# Definition of an interval applied: the distance between two adjacent
		# pitches
		intervals[i+1] = pitches[i+1]-pitches[i]
		# Different cases: Upwards interval
		# Contour and absolute intervals are denoted, and the counters for
		# each interval size are adjusted.
	for i in range(len(intervals)):
		if intervals[i] > 0:
			contour[i] = 1
			intervals_abs[i] = intervals[i]
			# if (intervals[i] > 12):
			# 	intervals_up[13] += 1
			# 	interval_abs_counter[13] += 1
			# 	if offsets[i] in hr_offsets:
			# 		intervals_up_change[13] += 1
			# 		intervals_abs_change[13] += 1
			# else:
			# 	intervals_up[intervals[i]] += 1
			# 	interval_abs_counter[intervals[i]] += 1
			# 	if offsets[i] in hr_offsets:
			# 		intervals_up_change[intervals[i]] += 1
			# 		intervals_abs_change[intervals[i]] += 1
		# Or downwards interval
		elif intervals[i] < 0:
			contour[i] = -1
			intervals_abs[i] = -intervals[i]
			# if intervals[i] < -12:
			# 	intervals_down[13] += 1
			# 	interval_abs_counter[13] += 1
			# 	if offsets[i] in hr_offsets:
			# 		intervals_down_change[13] += 1
			# 		intervals_abs_change[13] += 1
			# else:
			# 	intervals_down[intervals_abs[i]] += 1
			# 	interval_abs_counter[intervals_abs[i]] += 1
			# 	if offsets[i] in hr_offsets:
			# 		intervals_down_change[intervals_abs[i]] += 1
			# 		intervals_abs_change[intervals_abs[i]] += 1
		# Or unison, so no direction.
		# Since both directional lists start with the unison, it is counted
		# twice.
		else:
			contour[i] = 0
			intervals_abs[i] = 0
			# intervals_up[0] += 1
			# intervals_down[0] += 1
			# interval_abs_counter[0] += 1
			# intervals_up_change[0] += 1
			# intervals_down_change[0] += 1
			# intervals_abs_change[0] += 1

	# interval_counter = list(reversed(intervals_down[1:])) + intervals_up
	# interval_change_counter = list(reversed(intervals_down_change[1:])) + intervals_up_change

	# Actual contour definition: only direction changes are denoted. Here I
	# apply the idea of monotony, as opposed to strict monotony, i.e. pitch
	# repetitions do not count as direction change.
	contourdir = [0] * len(contour)
	for i in range(len(contour)):
		# First direction is always new, thus first run through loop gives a 1
		if i == 0:
			contourdir[i] = 1
		# Lateron: if the contour is 0 (pitch repetition), it does not count
		# as change; else: if the direction is the same as before, denote no
		# change, else do so.
		else:
			if contour[i] == 0:
				contourdir[i] = 0
			elif contour[i] == contour[i-1]:
				contourdir[i] = 0
			else:
				contourdir[i] = 1

	# Write everything into the results-handle for return
	results.append(intervals_abs)
	results.append(contourdir)

	return results


#----------------------------------------------------------------------------

# This function calculates conditional probabilities for the likelihood of a new
# harmony being used dependent on each feature on which harmonic rhythm may
# depend, i.e. intervals, contour, syncopation and overall melody onsets. For all
# of these but the syncopation measure, this is straight forward, for the
# syncopation measure, the list is split into patterns already. A problem about
# this is that the window should actually be of different sizes.
# This would however require a deep understanding
# of the musical score on the system's side and is thus not feasible.
# The functions takes 4 lists and returns a 2 x 9 matrix, containing the
# conditional probabilities (and their counterprobabilities) of a harmonic onset
# on:
# a contour change; a melody onset; unisons; steps; jumps; jumps bigger than or
# equal to an octave; low syncopation; medium syncopation; high syncopation.


def probabilities(intervals, contour, coocc, syncopation, hr, mr, ts):
	# Initialising offset lists and counting variables
	offsets = []
	hr_offsets = []
	bar_count = 0
	addendum = 0

	# Melodic rhythm
	for i in mr:
		# What we need to add is determined by the time signature: take its
		# numerator divided by the denominator (splitting the string at the '/'
		# will give you those) and then multiply by 4 since we calculate in base
		# fourth (by which I mean fourths are our unit)
		addendum += (int(ts[bar_count].split('/')[0])/int(ts[bar_count].split('/')[1]))*4
		# Then add this to all following patterns
		for j in i:
			m = float(j) + addendum
			offsets.append(float(m))
		# Go to the next bar to get the correct time signature
		bar_count += 1

	# Harmonic rhythm
	# Reset the two counting variables
	addendum = 0
	bar_count = 0
	# Same thing for harmonic rhythm, see above
	for i in hr:
		addendum += (int(ts[bar_count].split('/')[0])/int(ts[bar_count].split('/')[1]))*4
		for j in i:
			m = float(j) + addendum
			hr_offsets.append(float(m))
		bar_count += 1

	# Since for some reason, melodic rhythm sometimes starts with non-zero
	# values while harmonic rhythm always starts with 0, we need to adapt by
	# subtracting the corresponding number from all melodic offsets
	if offsets[0] != 0:
		subtractor = offsets[0]
		for k in range(len(offsets)):
			offsets[k] -= subtractor


	# Counting variables
	counter = 0
	changes = 0
	# Whenever the contour changes, count one up and check if the timing of the
	# melody at that point is also a harmonic rhythm timing. If so, count 1 up.
	for i in range(len(contour)):
		if contour[i] == 1:
			changes += 1
			if offsets[i] in hr_offsets:
				counter += 1

	# The conditional probability of a harmonic rhythm change given a contour
	# change is then simply the counter divided by all contour changes.
	contprob = counter/changes

	# Counting variables for unisons, steps, jumps and big jumps as well as
	# occurences of harmonic changes on them
	unicount = 0
	stepcount = 0
	jumpcount = 0
	octcount = 0
	uniharm = 0
	stepharm = 0
	jumpharm = 0
	octharm = 0

	# Iterate through interval list: Count each category and check if the
	# melody offset cooccurs with a harmony offset.
	for i in range(len(intervals)):

		# Unison
		if intervals[i] == 0:
			unicount += 1
			if offsets[i] in hr_offsets:
				uniharm += 1

		# Step
		elif abs(intervals[i]) == 1 or abs(intervals[i]) == 2:
			stepcount += 1
			if offsets[i] in hr_offsets:
				stepharm += 1

		# Jump
		elif abs(intervals[i]) >= 12:
			octcount += 1
			if offsets[i] in hr_offsets:
				octharm += 1
		# Big jump (octave+)
		else:
			jumpcount += 1
			if offsets[i] in hr_offsets:
				jumpharm += 1

	# Conditional probabilities are then easily calculated by dividing the
	# cooccurence counter by the overall category counter.
	if unicount != 0:
		uniprob = uniharm / unicount
	else: uniprob = 0
	if stepcount != 0:
		stepprob = stepharm / stepcount
	else: stepcount = 0
	if jumpcount != 0:
		jumpprob = jumpharm / jumpcount
	else: jumpprob = 0
	if octcount != 0:
		octprob = octharm / octcount
	else: octprob = 0

	# More counting variables, again for occurences and corresponding harmony
	# changes
	low_sync = 0
	med_sync = 0
	high_sync = 0
	lowharm = 0
	medharm = 0
	highharm = 0

	# For the three syncopation categories found, count their occurences and
	# how often harmonic changes cooccur.
	for i in range(len(syncopation)):

		# Low syncopation
		if syncopation[i] <= 0.5:
			low_sync += 1
			if offsets[i] in hr_offsets:
				lowharm += 1

		# Medium syncopation
		elif syncopation[i] <= 1:
			med_sync += 1
			if offsets[i] in hr_offsets:
				medharm += 1

		# High syncopation
		else:
			high_sync += 1
			if offsets[i] in hr_offsets:
				highharm += 1

	# Calculate the probabilities
	if low_sync != 0:
		lowprob = lowharm / low_sync
	else: lowprob = 0
	if med_sync != 0:
		medprob = medharm / med_sync
	else: medprob = 0
	if high_sync != 0:
		highprob = highharm/high_sync
	else: highprob = 0

	# Put everything in a numpy array as a result.
	results = np.array([[contprob, coocc, uniprob, stepprob, jumpprob, octprob,\
	lowprob, medprob, highprob], [1-contprob, 1-coocc, 1-uniprob, 1-stepprob,\
	1-jumpprob, 1-octprob, 1-lowprob, 1-medprob, 1-highprob]])

	return results
