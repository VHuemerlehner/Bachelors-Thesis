# -*- coding: utf-8 -*-
"""
@author: Valentin Huemerlehner
"""
#TODO: Rewrite documentation
#Helper function to find word in string:

def smart_find(haystack, needle):
	if haystack.startswith(needle+" "):
		return 0
	if haystack.endswith(" "+needle):
		return len(haystack)
	if haystack.find(" "+needle+" ") != -1:
		return haystack.find(' ' + needle + ' ')
	return -1

#This function splits the long list of rows of the .csv-files into five
#separate ones containing information about harmonic rhythm, melodic rhythm,
#melody pitches, grouping and time signatures. These lists get appended into
#one list as return value.

#Our input: A list with a list for each row of the .csv, containing either:
#TS - 3/4 OR Grp - 0.0 OR - Bar - (Harmonic Rhythm) 0 2  - cont.
#(Melodic Rhythm) 0 1 2 3 - (Pitches) 66 68 70 71

##DOCUMENTATIONISFORPUSSIES #IHATEMYSELFALREADY #GOTLUCKYREMEMBEREDEVERYTHING
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

#    For debugging:
#    print('Harmonic Rhythm\n')
#    print(hrinf)
#    print('\n\nMelodic Rhythm\n')
#    print(mrinf)
	# print('\n\nMelody Pitches\n')
	# print(mpinf)
#    print('\n\nGrouping\n')
#    print(grpinf)
#    print('\n\nTime Signatures\n')
#    print(tsinf)
#    print('\n\n\nAre all lists of equal length?\n' + str((len(hrinf) == len(mrinf)) and (len(mpinf) == len(grpinf)) and (len(grpinf) == len(tsinf))))

	#Write it all in one list so we only hand around one object. Like a folder. Just dumb.
	returnlist = []
	returnlist.append(hrinf)
	returnlist.append(mrinf)
	returnlist.append(mpinf)
	returnlist.append(grpinf)
	returnlist.append(tsinf)
	return returnlist


#-------------------------------------------------------------------------------


# The following function sums over a list of given rhythmic patterns to
# determine the frequency of each occuring pattern. It outputs a dictionary
# with 'pattern: [sum, frequency]'.
def patfrequency(rpinf):
	# Initialising variables: 2 lists for patterns and occurences and the dict
	# to put it all in
	rpdict = {}
	patlist = []
	occurencelist = []

	# Running through the data, make a marker for new or old pattern
	for i in rpinf:
		newTS = True
		for j in patlist:
			if i == j:
				newTS = False
		# If the pattern is new, add it to the list and add an occurence entry
		if newTS:
			patlist.append(i)
			occurencelist.append(1)
		# Else find it in the list and edit the corresponding occurence entry
		else:
			k = 0
			while (i != patlist[k]) and (k<len(patlist)):
				k += 1
			occurencelist[k] += 1

	# Write it all into the dict
	for i in range(len(patlist)):
		rpdict.update({tuple(patlist[i]): [occurencelist[i], occurencelist[i]/len(rpinf)]})
	return rpdict


#-------------------------------------------------------------------------------


# The following function compares melodic and harmonic rhythmic patterns:
# It counts the number of cooccurring onsets, gives a percentage for each
# melodic and harmonic overall onsets and measures the difference in number
# of onsets in each bar. Output: [cooccurences abs, per measure, percentage of
# harmony onsets, percentage of melody onsets, absolute difference between
# number of melody and harmony onsets, same per measure, syncopation]


def patcomparison(hr, mr, ts):
	results = []
	coocc = 0
	honsets = 0
	monsets = 0
	#Missing documentation... Smort. Not.
	#Since there should be as many harmonic patterns as melodic ones, iterate
	#over one list and simply count the number of elements in all the lists
	#inside it. Then check if in one pattern (which can be maximally one bar
	#long, thus never repeating the same number within itself) both lists show
	#the same number, meaning that harmony and melody cooccur. Interestingly
	#enough, harmonic changes need not necessarily fall onto melodic ones
	#(although this is rare enough even in the most complicated idioms tested
	#to be ignored without a significant performance hit)
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
	# In code more like: If on strong beat: 0; else: if ends between next two
	# strong beats, 2/T(x); else: 1/T(x)
	# Sum all these, divide by number of notes.
	# Do this for each pattern, add the result times the number of notes.

	wnbdList = []
	for i in range(len(mr)):
		# Write one pattern into a new list
		onsets = mr[i]
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
		for k in range(len(onsets) - 1):
			if onsets[k] in strong:
				distance += 0
			else:
				# distance to next strong beat (no matter the direction):
				# Minimum of the differences between the onset and all strong
				# beats, absolute value so direction does not matter
				dtb = min(abs(onsets[k] - l) for l in strong)
				# print(dtb)
				for l in strong:
					if l > onsets[k]:
						# distance to the next occurring beat (forwards)
						dtn = l - onsets[k]
						# distance to two beats ahead
						dtta = dtn + incr
						break
				# If the offbeat note stops between the next two strong beats,
				# the distance measure added is doubled
				if ((onsets[k+1] - onsets[k]) > dtn) and ((onsets[k+1] - onsets[k]) <= dtta):
					distance += 2/dtb
				else:
					distance += 1/dtb
		# treat the last onset differently (assume it ends on the pattern ending)
		# need to reset distances
		dtn = 0
		dtta = 0
		last_onset = onsets[-1]
		# if on a strong beat, ignore
		if last_onset in strong:
			distance += 0
		# else assume it ends on the pattern ending (the latest)
		else:
			# get minimal distance to beat
			dtb = min(last_onset - l for l in strong)
			# print(dtb)
			# get distance to following strong beat (if applicable)
			# MAYBE ADD ONE MORE BEAT TO MEASURE SO THIS BECOMES EASIER?
			followed = False
			for l in strong:
				if l > last_onset:
					followed = True
					dtn = l - last_onset
					dtta = dtn + incr
					# get the next beat's index (no duplicates, so this works)
					ind = strong.index(l)
					break
			# If the pattern ending is between 1 and 2 beats after the onset,
			# double the distance measure.
			if followed:
				if (ind == len(strong) - 1):
					distance += 2/dtb
				else:
					distance += 1/dtb
			else:
				distance += 1/dtb

		# In the end, divide the pattern's distance measure by its onset count
		wnbd = distance/number
		# And add it to the distance-list
		for i in range(number):
			wnbdList.append(wnbd)


	results.append(coocc)
	results.append(coocc/len(hr))
	results.append(coocc/honsets)
	results.append(coocc/monsets)
	results.append(monsets-honsets)
	results.append((monsets-honsets)/len(hr))
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
	results = []
	pitches = []
	offsets = []
	hr_offsets = []
	# First, we need to get all pitches into one long list of integers, same
	# with their offsets and the harmonic rhythm offsets, those as floats
	# because they contain .5 values and we actually do maths on them
	for i in mp:
		for j in i:
			pitches.append(int(j))
	for i in mr:
		for j in i:
			offsets.append(float(j))
	for i in hr:
		for j in i:
			hr_offsets.append(float(j))

	#Restore actual timings for melodic rhythm by adding the numerator of the
	#TS for each bar to the offsets (hacky solution, but that's what you get for
	#not thinking projects through in the beginning...)
	bar_count = 0
	for i in range(len(offsets)-1):
		if offsets[i+1] <= offsets[i]:
			for j in range(i+1, len(offsets)):
				#Not as complicated as it seems: TS are stored as strings that
				#we now split at "/" and divide the numerator by the denominator,
				#then casting as integers and multiplying with 4 since our timings
				#are thought in 4ths
				offsets[j] += (int(ts[bar_count].split('/')[0])/int(ts[bar_count].split('/')[1]))*4
			bar_count += 1

	#Same bs for harmonic rhythm.
	bar_count = 0
	for i in range(len(hr_offsets)-1):
		if hr_offsets[i+1] <= hr_offsets[i]:
			for j in range(i+1, len(hr_offsets)):
				hr_offsets[j] += (int(ts[bar_count].split('/')[0])/int(ts[bar_count].split('/')[1]))*4

	intervals = [None] * (len(pitches)-1)
	contour = [None] * (len(pitches)-1)
	intervals_abs = [None] * (len(pitches)-1)
	distanceabs = 0
	distancerel = 0

	# "Tonal" distance in the melody: correlate occurence of interval with
	# occurence of new harmony, thus finding probabilities for a harmony change
	# given an interval. We create 2 counting buckets for all intervals from
	# unison (0 half tones) to octave (12 half tones) each and two bucket for
	# all intervals bigger than one octave. Thus, direction is preserved. In
	# case direction is not important, we also count the absolute intervals in
	# interval_abs_counter, thusly only half the size of interval_counter.
	# Unisons are counted in both directions, later halfed
	interval_counter = []
	intervals_up = [0] * 14
	intervals_down = [0] * 14
	interval_abs_counter = [0] * 14
	intervals_up_change = [0] * 14
	intervals_down_change = [0] * 14
	intervals_abs_change = [0] * 14

	# 'intervals' contains the direction and size of melodic steps, 'contour'
	# extracts only the direction of
	# movement, intervals_abs only the amount of movement
	# First, we need to get all pitches into one list to iterate through.
	# ------- IDEA: delete unisons? pro: does not contribute to contour
	# con: may contribute to harmonic rhythm (harmonically reinterpreted
	# "equal" pitches) -- Check how often unisons are harmonically reinterpreted
	# to see if deleting them is a problem or not.
	for i in range(len(pitches)-1):
		# definition of an interval applied: the distance between two adjacent
		# pitches
		intervals[i] = pitches[i+1]-pitches[i]
		# Different cases: Upwards interval
		# Contour and absolute intervals are denoted, and the counters for
		# each interval size are adjusted. Usage of separate counters for up-
		# and downwards motion is justified so as to make indexing easier.
		if intervals[i] > 0:
			contour[i] = 1
			intervals_abs[i] = intervals[i]
			if (intervals[i] > 12):
				intervals_up[13] += 1
				interval_abs_counter[13] += 1
				if offsets[i] in hr_offsets:
					intervals_up_change[13] += 1
					intervals_abs_change[13] += 1
			else:
				intervals_up[intervals[i]] += 1
				interval_abs_counter[intervals[i]] += 1
				if offsets[i] in hr_offsets:
					intervals_up_change[intervals[i]] += 1
					intervals_abs_change[intervals[i]] += 1
		# Or downwards interval
		elif intervals[i] < 0:
			contour[i] = -1
			intervals_abs[i] = -intervals[i]
			if intervals[i] < -12:
				intervals_down[13] += 1
				interval_abs_counter[13] += 1
				if offsets[i] in hr_offsets:
					intervals_down_change[13] += 1
					intervals_abs_change[13] += 1
			else:
				intervals_down[intervals_abs[i]] += 1
				interval_abs_counter[intervals_abs[i]] += 1
				if offsets[i] in hr_offsets:
					intervals_down_change[intervals_abs[i]] += 1
					intervals_abs_change[intervals_abs[i]] += 1
		# Or unison, so no direction.
		# Since both directional lists start with the unison, it is counted
		# twice.
		else:
			contour[i] = 0
			intervals_abs[i] = 0
			intervals_up[0] += 1
			intervals_down[0] += 1
			interval_abs_counter[0] += 1
			intervals_up_change[0] += 1
			intervals_down_change[0] += 1
			intervals_abs_change[0] += 1

	# Joining of the respective two directional lists, reversing the downwards
	# one and taking out one of the unisons.
	# Result: [down more than octave, down octave, down major seventh, ...
	# unison, up minor second, up major second, ... up more than octave]
	interval_counter = list(reversed(intervals_down[1:])) + intervals_up
	interval_change_counter = list(reversed(intervals_down_change[1:])) + intervals_up_change


	for i in range(len(intervals_abs)):
		distanceabs = distanceabs + intervals_abs[i]

	distancerel = distanceabs/(len(pitches)-1)
	# actual contour definition: only direction changes are denoted. Here I
	# apply the idea of monotony, as opposed to strict monotony, i.e. pitch
	# repetitions do not count as direction change.
	contourdir = [0] * len(contour)
	for i in range(len(contour)):
		# first direction is always new, thus first run through loop gives a 1
		if i == 0:
			contourdir[i] = 1
		# lateron: if the contour is 0 (pitch repetition), it does not count
		# as change; else: if the direction is the same as before, denote no
		# change, else do so.
		else:
			if contour[i] == 0:
				contourdir[i] = 0
			elif contour[i] == contour[i-1]:
				contourdir[i] = 0
			else:
				contourdir[i] = 1

	# print('Overall absolute interval size')
	# print(distanceabs)
	# print('Average interval size')
	# print(distancerel)
	# print('Interval counts')
	# print(interval_counter)
	# print('Absolute interval counts')
	# print(interval_abs_counter)
	# print('Interval change counts')
	# print(interval_change_counter)
	# print('Absolute interval change counts')
	# print(intervals_abs_change)

	# Write everything into the results-handle for return
	results.append(intervals)
	results.append(intervals_abs)
	results.append(contour)
	results.append(contourdir)
	results.append(distanceabs)
	results.append(distancerel)
	results.append(interval_counter)
	results.append(interval_abs_counter)
	results.append(interval_change_counter)
	results.append(intervals_abs_change)

	return results


#----------------------------------------------------------------------------

# This function calculates conditional probabilities for the likelihood of a new
# harmony being used dependent on each feature on which harmonic rhythm may
# depend, i.e. intervals, contour, syncopation and overall melody onsets. For all
# of these but the syncopation measure, this is straight forward, for the
# syncopation measure, the list is split into patterns already. A problem about
# this is that the window should actually be of different sizes
# this would however require a deep understanding
# of the musical score on the system's side and is thus not feasible.
# The functions takes 4 lists and returns a 2 x 9 matrix, containing the
# conditional probabilities of a harmonic onset on:
# a contour change; a melody onset; unisons; steps; jumps; jumps bigger than or
# equal to an octave; low syncopation (threshold? maybe so that each category gets roughly one third of the values); medium syncopation;
# high syncopation.


def probabilities(contour, mr, coocc, intervals, syncopation):
	# Get all melody and harmony offsets into one list, not list of lists
	offsets = []
	hr_offsets = []
	for i in mr:
		for j in i:
			offsets.append(float(j))
	for i in hr:
		for j in i:
			hr_offsets.append(float(j))

	#Restore actual timings for melodic rhythm by adding the numerator of the
	#TS for each bar to the offsets (hacky solution, but that's what you get for
	#not thinking projects through in the beginning...)
	for i in range(len(offsets)-1):
		if offsets[i+1] <= offsets[i]:
			for j in range(i+1, len(offsets)):
				#Not as complicated as it seems: TS are stored as strings that
				#we now split at "/" and divide the numerator by the denominator,
				#then casting as integers and multiplying with 4 since our timings
				#are thought in 4ths
				offsets[j] += (int(ts[bar_count].split('/')[0])/int(ts[bar_count].split('/')[1]))*4
			bar_count += 1

	#Same bs for harmonic rhythm.
	bar_count = 0
	for i in range(len(hr_offsets)-1):
		if hr_offsets[i+1] <= hr_offsets[i]:
			for j in range(i+1, len(hr_offsets)):
				hr_offsets[j] += (int(ts[bar_count].split('/')[0])/int(ts[bar_count].split('/')[1]))*4

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
		if intervals[i] == 0:
			unicount += 1
			if offsets[i] in hr_offsets:
				uniharm += 1
		elif abs(intervals[i]) == 1 or abs(intervals[i]) == 2:
			stepcount += 1
			if offsets[i] in hr_offsets:
				stepharm += 1
		elif abs(intervals[i]) >= 12:
			octcount += 1
			if offsets[i] in hr_offsets:
				octharm += 1
		else:
			jumpcount += 1
			if offsets[i] in hr_offsets:
				jumpharm += 1

	# Conditional probabilities are then easily calculated by dividing the
	# cooccurence counter by the overall category counter.
	uniprob = uniharm / unicount
	stepprob = stepharm / stepcount
	jumpprob = jumpharm / jumpcount
	octprob = octharm / octcount
