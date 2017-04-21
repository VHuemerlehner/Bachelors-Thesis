# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 15:11:36 2016

@author: VH
"""

# This function extracts the rhythmic patterns of the reduction given in the
# last two parts of a musicXML file barwise.
# Only use with 2-part reductions, no error included! Only use with pieces
# whose parts have the same number of measures and time signatures in both
# parts, no error included!

#from music21 import stream;
from music21 import meter;
import os;

def writePhrasesToFile(p,pieceName,currFolder,destFolder):
    
    #get necessary parts (reduction and grouping)
    p0 = p.parts[-2];
    p1 = p.parts[-1];
    p2 = p.parts[-3];

    #get measures
#    meas0 = p0.getElementsByClass(stream.Measure);

    #chordify them
    c0 = p0.chordify();
    c1 = p1.chordify();
    c2 = p2.chordify();

    #flatten them
    f0 = c0.flat;
    f1 = c1.flat;
    f2 = c2.flat;
    
    #get all chords, time signatures and groupings
    red0 = f0.getElementsByClass('Chord');
    red1 = f1.getElementsByClass('Chord');
    ts0 = f0.getTimeSignatures();
#    ts1 = f1.getTimeSignatures();
    gr = f2.getElementsByClass('Chord');

    #get all chord offsets, put them in a set (delete duplicates), order it
    off0 = [];
    off1 = [];
    for i in red0:
        off0.append(i.offset);
    for i in red1:
        off1.append(i.offset);
    offs = sorted(set(off0 + off1));

    #get all grouping and measure offsets, put them in a set to delete
    #duplicates, order it, add one element to avoid out of range error
#    measureoffs,  patternoffs  = [], [];
    groffs= [];
    for i in gr:
        groffs.append(i.offset);
#    for i in meas0:
#        measureoffs.append(i.offset);
#    patternoffs = sorted(set(groffs + measureoffs));

    #hacky solution... we need to avoid an index out of range error later =/
    groffs.append(groffs[len(groffs)-1]+50);
    ts0.append(meter.TimeSignature('7/8'));
    ts0[len(ts0)-1].offset = groffs[len(groffs)-1]+50;
    
    # create as many lists as there are patterns
    lists = [[] for i in range(len(groffs))];
    
    #get the offsets of one pattern into one list
    for i in range(len(lists)):
        for j in range(len(offs)):
            if offs[j] >= groffs[i] and offs[j] < groffs[i+1]:
                lists[i].append(offs[j]);

    #create a copy so we still have the original offsets to insert time
    #signatures at the right spot
    patterns = list(lists);

    #subtract the first offset of each pattern so they all become normalised
    for i in range(len(patterns)):
        patterns[i] = [n - groffs[i] for n in patterns[i]];

    #create the string: on each pattern beginning, check for a time signature
    #and grouping occurence and print them, then print the offsets of chords
    #occurring
    tmpStr = str();
    for i in range(len(lists)-1):
        #time signatures
        for j in range(0, len(ts0)):
            if ts0[j].offset == groffs[i]:
                tmpStr += 'TS\t' + str(ts0[j].numerator) + '/' + str(ts0[j].denominator) + '\n';
        #grouping                               
        for k in range(len(gr)):
            if gr[k].offset == groffs[i]:
                tmpStr += 'Grp\t' + str(gr[k].beat-1) + '\n';
        #chords                                
        tmpStr += 'Bar\t' + str(patterns[i]) + '\n';

    #create filename
    splitName = pieceName.split('.');
    noExtName = splitName[0];
    finalName = noExtName+'.txt';
    text_file = open(finalName, 'w');

    #write 
    text_file.write(tmpStr);
    text_file.close();
    os.rename(currFolder+finalName, destFolder+finalName);