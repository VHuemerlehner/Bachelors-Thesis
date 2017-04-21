# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 15:40:20 2016

@author: User
"""

import sys
import os
import glob
import rhythmAnalysis

if len(sys.argv) < 3:
    sys.exit("readAllTXTForAnalysis: Not enough input arguments")

currFolder = sys.argv[1];
destFolder = sys.argv[2];
    
os.chdir(currFolder)
allDocs = glob.glob("*.txt")

if len(allDocs) < 1:
    sys.exit("readAllXMLfiles.py: No TXT files there!")
    
# parse all pieces
for pieceName in allDocs:
    print ("Analysing File: " + pieceName);
    thefile = open(pieceName, 'r');
    s = thefile.read();
    rhythmAnalysis.analysis(s, pieceName, currFolder, destFolder);
    print("DONE =)");