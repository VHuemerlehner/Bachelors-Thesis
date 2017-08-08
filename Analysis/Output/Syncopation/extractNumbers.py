import glob
import numpy

# This script was only used to get syncopation thresholds, i.e. to find values
# that split the syncopation values roughly in thirds. I found 0.5 and 1.0 to
# be on the edges between the thirds, so decided to define low syncopation as
# all wnbd values up to (and including) 0.5, medium syncopation as those between
# 0.5 and (including) 1.0 and high syncopation all values above 1.0.


allDocs = glob.glob("*.txt")

if len(allDocs) < 1:
	sys.exit("extractNumbers.py: No TXT files there!")

all_idioms = ''

for idiom in allDocs:
	print(idiom)
	file = open(idiom, 'r')
	all_idioms += file.read()

all_idioms = all_idioms.replace('[', ',')
all_idioms = all_idioms.replace(']', ',')
all_idioms = all_idioms.replace(',,', ',')
all_idioms = all_idioms.replace(', ,', ',')
all_idioms = all_idioms[:-1]

all_syncs = all_idioms.split(',')
all_syncs = list(filter(None, all_syncs))
all_syncs = [float(x) for x in all_syncs]
max_sync = max(all_syncs)
avg_sync = sum(all_syncs)/len(all_syncs)
median_sync = numpy.median(all_syncs)
for x in range(len(all_syncs)):
	if all_syncs[x]<0:
		print(all_syncs[x])
		print(x)

print(max_sync)
print(avg_sync)
print(median_sync)
chunked = numpy.array_split(numpy.array(sorted(all_syncs)), 3)
print(chunked[1][1])
print(chunked[2][1])
