from music21 import stream
from music21 import meter
from music21 import converter
import sys
import os
import glob

if len(sys.argv) < 3:
	sys.exit("readAllXMLfiles.py: Not enough input arguments")

currFolder = sys.argv[1];
destFolder = sys.argv[2];


os.chdir(currFolder)
allDocs = glob.glob("*.xml")

if len(allDocs) < 1:
	sys.exit("readAllXMLfiles.py: No XML files there!")

def isfloat(value):
	try:
		float(value)
		return True
	except ValueError:
		return False

# parse all pieces
for pieceName in allDocs:
	print ("Parsing piece: "+pieceName+"... ");
	p = converter.parse(currFolder+pieceName);
	print ("Writing "+pieceName+" to file...");

	# Get parts
	p0 = p.parts[0]
	p1 = p.parts[-2]
	p2 = p.parts[-1]

	# Extract melody
	if p0.voicesToParts().parts[0]:
		p0 = p0.voicesToParts().parts[0];

	# chordify
	c1 = p1.chordify();
	c2 = p2.chordify();

	# flatten
	f0 = p0.flat;
	f1 = c1.flat;
	f2 = c2.flat;

	# Get Notes and chords
	red0 = f1.getElementsByClass('Chord');
	red1 = f2.getElementsByClass('Chord');
	mel = f0.getElementsByClass('Note');

	# Initialise lists
	off = []
	hoff = []
	off0 = []
	off1 = []

	# Get Melody offsets
	for i in mel:
		if isfloat(i.offset):
			off.append(float(i.offset));
		else:
			tmp = i.offset.split('/')
			num = tmp[0][-1]
			den = tmp[1][0]
			off.append(float(num)/float(den))

	# Get Harmony offsets, make set (remove duplicates), sort
	for i in red0:
		if isfloat(i.offset):
			off0.append(float(i.offset));
		else:
			tmp = i.offset.split('/')
			num = tmp[0][-1]
			den = tmp[1][0]
			off0.append(float(num)/float(den))

	for i in red1:
		if isfloat(i.offset):
			off1.append(float(i.offset));
		else:
			tmp = i.offset.split('/')
			num = tmp[0][-1]
			den = tmp[1][0]
			off1.append(float(num)/float(den))
	hoff = sorted(set(off0 + off1));

	# Put into string
	tmpStr = str(off) + '\n' + str(hoff)

	#filename
	splitName = pieceName.split('.')
	noExtName = splitName[0]
	finalName = destFolder+noExtName+'.txt'
	text_file = open(finalName, 'w')

	#write file
	text_file.write(tmpStr)
	text_file.close()
