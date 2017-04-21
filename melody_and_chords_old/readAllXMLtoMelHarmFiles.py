from music21 import *
import sys
import os
import glob
import melodyExport
# import voicesTonGrToFile

# currFolder = "/Users/maximoskaliakatsos-papakostas/Documents/python/music21tuts/BachChorales/"
# destFolder = "/Users/maximoskaliakatsos-papakostas/Documents/python/music21tuts/BachChoralesHarmTXT/"

# print 'Number of arguments:', len(sys.argv), 'arguments.'
# print 'Argument List:', str(sys.argv)

if len(sys.argv) < 2:
    sys.exit("readAllXMLfiles.py: Not enough input arguments")

currFolder = sys.argv[1];
destFolder = sys.argv[2];
    
os.chdir(currFolder)
allDocs = glob.glob("*.xml")

if len(allDocs) < 1:
    sys.exit("readAllXMLfiles.py: No XML files there!")

# parse all pieces
for pieceName in allDocs:
    print("Parsing piece: " + pieceName + "...");
    p = converter.parse(currFolder+pieceName);
    print("DONE");
    print("Writing "+pieceName+" to file...");
    # voicesTonGrToFile.writeHarmToFile(p,pieceName,currFolder,destFolder)
    melodyExport.writeHarmToFile(p,pieceName,currFolder,destFolder);
    print ("DONE");



# pieceName = "BC_068_043100B_a1.xml"
# p = converter.parse(currFolder+pieceName)
# import piece ===========================================================================