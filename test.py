import numpy as np

file = open('/home/waldo/Desktop/Bachelors_Thesis/Analysis/Probabilities/Idioms/BachChorales.txt')
content = file.read()
content = content.replace('\n', '')
content = content.replace('  ', ' ')
content = content.replace('  ', ' ')
content = content.replace(' ', ',')
content = content.replace('[,', '[')
content = content.replace('[', '')
content = content.replace(']', '')
contents = content.split(',')

for i in range(len(contents)):
	contents[i] = float(contents[i])

arr = np.array(contents)
arr = arr.reshape(2,9)
print(arr)
