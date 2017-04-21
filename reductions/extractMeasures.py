# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 17:12:03 2016

@author: User
"""

from music21 import stream;
import os;

def getMeasureOffsets(p, pieceName, currFolder, destFolder):
    
    #get a part
    p0 = p.parts[1];
    c0 = p0.chordify();
    f0 = c0.flat;

    #get measures and time signatures
    ts = f0.getTimeSignatures();
    meas0 = p0.getElementsByClass(stream.Measure);

    #get measure offsets
    measureoffs = [];
    tsoffs = [];
    for i in ts:
        tsoffs.append(i.offset);
    for i in meas0:
        measureoffs.append(i.offset);
    
    #write string
    tmpStr = '';     
    for i in measureoffs:
        for j in range(len(ts)):
            if ts[j].offset == i:
                tmpStr += 'TS\t' + str(ts[j].numerator) + '/' + str(ts[j].denominator) + '\n';
        tmpStr += 'MS\t' + str(i) + '\n';
    
    #create filename
    splitName = pieceName.split('.');
    noExtName = splitName[0];
    finalName = noExtName+'.txt';
    text_file = open(finalName, 'w');

    #write 
    text_file.write(tmpStr);
    text_file.close();
    os.rename(currFolder+finalName, destFolder+finalName);