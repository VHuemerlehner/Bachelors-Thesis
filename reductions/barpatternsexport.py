# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 15:11:36 2016

@author: VH
"""

# This function extracts the rhythmic patterns of the reduction given in the
# last two parts of a musicXML file in patterns with boundaries of bars and
# groupings.
# Only use with 2-part reductions, no error included! Only use with pieces
# whose parts have the same number of measures and time signatures in both
# parts, no error included!

from music21 import stream;
from music21 import meter;
import os;

def writeBarPatternsToFile(p,pieceName,currFolder,destFolder):
    
    #get necessary parts (reduction and grouping)
    p0 = p.parts[-2];
    p1 = p.parts[-1];
    p2 = p.parts[-3];

    #get measures
    meas0 = p0.getElementsByClass(stream.Measure);

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
    stream0 = [];
    stream1 = [];
    for i in red0:
        off0.append(i.offset);
        stream0.append(i);
    for i in red1:
        off1.append(i.offset);
        stream1.append(i);
    offs = sorted(set(off0 + off1));
    #explanation: we need beats of the first bar, but don't know how long it
    #is. Therefore, we take both streams, combine them, order them according
    #to offset (at least that's what music21 documentation tells us) and take
    #their beats afterwards.
    beatstream = stream.Stream();
    for i in (stream0):    
        beatstream.append(i);
    for i in (stream1):
        beatstream.append(i);
    beats = [i.beat - 1 for i in beatstream.sorted];

    #get all grouping and measure offsets, put them in a set to delete
    #duplicates, order it, add one element to avoid out of range error
    groffs, measureoffs, patternoffs = [], [], [];
    for i in gr:
        groffs.append(i.offset);
    for i in meas0:
        measureoffs.append(i.offset);
    patternoffs = sorted(set(groffs + measureoffs));
    
    #hacky solution... we need to avoid an index out of range error later =/
    patternoffs.append(patternoffs[len(patternoffs)-1]+50);
    ts0.append(meter.TimeSignature('7/8'));
    ts0[len(ts0)-1].offset = patternoffs[len(patternoffs)-1]+50;
    measureoffs.append(measureoffs[len(measureoffs)-1]+70);
    
    #create copy for later use
    offscopy = list(offs);
    
    #normalise offsets to measures
    for i in range(len(offscopy)):
        for j in range(len(measureoffs)-1):
            if offscopy[i] >= measureoffs[j] and offscopy[i] < measureoffs[j+1]:
                offscopy[i] = offscopy[i] - measureoffs[j];
    
    # create as many lists as there are patterns
    lists = [[] for i in range(len(patternoffs)-1)];
    beatlists = [[] for i in range(len(patternoffs)-1)];
    
    #get the offsets of one pattern into one list
    for i in range(len(lists)):
        for j in range(len(offs)):
            if offs[j] >= patternoffs[i] and offs[j] < patternoffs[i+1]:
                lists[i].append(offscopy[j]);
                beatlists[i].append(beats[j]);

    #create the string: on each pattern beginning, check for a time signature
    #and grouping occurence and print them, then print the offsets of chords
    #occurring
    tmpStr = str();
    
#    explanation: ".beat" counts from the back of the bar, so it gets
#    appoggiaturas right, but not last bars that are truncated due to the
#    appoggiatura at the beginning of a piece. Therefore, we need to use another
#    way for everything except the first bar (actually, everything except the
#    last bar, but Python makes it easier this way), so we use a boolean to
#    do something once at the beginning of the loop, then change the procedure
#    when the boolean is false.
    halpbool = True;
    for i in range(len(lists)):
        if halpbool:
            if ts0[0].offset == patternoffs[i]:
                tmpStr += 'TS\t' + str(ts0[0].numerator) + '/' + str(ts0[0].denominator) + '\n';
            if gr[0].offset == patternoffs[i]:
                tmpStr += 'Grp\t' + str(gr[0].beat-1) + '\n';
            tmpStr += 'Bar\t' + str(beatlists[i]) + '\n';                            
            halpbool = False;
        else:
            #time signatures
            for j in range(0, len(ts0)):
                if ts0[j].offset == patternoffs[i]:
                    tmpStr += 'TS\t' + str(ts0[j].numerator) + '/' + str(ts0[j].denominator) + '\n';
            #grouping                               
            for k in range(len(gr)):
                if gr[k].offset == patternoffs[i]:
                    tmpStr += 'Grp\t' + str(gr[k].beat-1) + '\n';
            #chords                                
            tmpStr += 'Bar\t' + str(lists[i]) + '\n';
                                
    #change string so there no empty last line
    tmpStr = tmpStr[:-1];

    #create filename
    splitName = pieceName.split('.');
    noExtName = splitName[0];
    finalName = noExtName+'.txt';
    text_file = open(finalName, 'w');

    #write 
    text_file.write(tmpStr);
    text_file.close();
    os.rename(currFolder+finalName, destFolder+finalName);