# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 16:43:16 2016

@author: User
"""

from music21 import converter;
import sys;
import os;
import glob;
import extractMelody;

if len(sys.argv) < 3:
    sys.exit("readAllXMLfiles.py: Not enough input arguments")

currFolder = sys.argv[1];
destFolder = sys.argv[2];
    

os.chdir(currFolder)
allDocs = glob.glob("*.xml")

if len(allDocs) < 1:
    sys.exit("readAllXMLfiles.py: No XML files there!")

# parse all pieces
for pieceName in allDocs:
    print ("Parsing piece: "+pieceName+"... ");
    p = converter.parse(currFolder+pieceName);
    print ("DONE");
    print ("Writing "+pieceName+" to file...");
    extractMelody.writeMelodyToFile(p, pieceName, currFolder, destFolder);
    print ("DONE");