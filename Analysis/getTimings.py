import sys

file = open(sys.argv[1], 'r')
contents = file.read()
content_list = contents.split('\n')

#MR
melody = []
for i in content_list:
	if len(i) != 0:
		if i[0] == 'm':
			melody.append(i)

for j in range(len(melody)):
	melody[j] = melody[j].split('\t')

offsets = []

for k in melody:
	offsets.append(float(k[1]))

#HR

harmony = []
for i in content_list:
	if len(i) != 0:
		if i[0] == 'r':
			harmony.append(i)

for j in range(len(harmony)):
	harmony[j] = harmony[j].split('\t')

hr_offsets = []

for k in harmony:
	hr_offsets.append(float(k[1]))
