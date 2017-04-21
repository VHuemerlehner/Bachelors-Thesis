# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 16:45:11 2016

@author: User
"""

from music21 import stream;
from music21 import meter;
import os;

#This method extracts the melody of a given music21-Stream (p) with the
#following structure: 2 parts surface, tonality, grouping, 2 parts reduction
#and writes it into a .TXT-file using its pieceName and destFolder

def writeMelodyToFile(p, pieceName, currFolder, destFolder):
    
    #get necessary parts (tonality, grouping, 1st part);
    #p0 = 1st part (includes melody), p1 = tonality, p2 = grouping
    p0 = p.parts[0];
#    p1 = p.parts[-4];
    p2 = p.parts[-3];
    
    #extract measure offsets
    meas = p0.getElementsByClass(stream.Measure);
    
    #extract melody
    if p0.voicesToParts().parts[0]:
        p0 = p0.voicesToParts().parts[0];

    #chordify the stuff
    #c0 = p0.chordify();
#    c1 = p1.chordify();
    c2 = p2.chordify();

    #flatten it
    f0 = p0.flat;
#    f1 = c1.flat;
    f2 = c2.flat;
    
    #get all notes, time signatures, tonalities and groupings
    ts = f0.getTimeSignatures();
    mel = f0.getElementsByClass('Note');
#    ton = f1.getElementsByClass('Chord');
    gr = f2.getElementsByClass('Chord');

    #get all melody note offsets, pitches and beats
    meloff = [];
    melpitch = [];
    melbeats = [];
    for i in mel:
        meloff.append(i.offset);
        melpitch.append(i.pitch.midi);
        melbeats.append(i.beat-1);

    #get all grouping and measure offsets, remove duplicates, order them
    groff, measureoff, patternoff = [], [], [];
    for i in gr:
        groff.append(i.offset);
    for i in meas:
        measureoff.append(i.offset);
    patternoff = sorted(set(groff + measureoff));
    
    #don't try this at home...
    patternoff.append(patternoff[len(patternoff)-1]+50);
    ts.append(meter.TimeSignature('7/8'));
    ts[len(ts)-1].offset = patternoff[len(patternoff)-1]+50;
    measureoff.append(measureoff[len(measureoff)-1]+50.0);
    
    # create as many lists as there are patterns
    offlists = [[] for i in range(len(patternoff)-1)];
    mellists = [[] for i in range(len(patternoff)-1)];
    beatlists = [[] for i in range(len(patternoff)-1)];

    #create a copy of offset list to use later
    meloffcopy = list(meloff);
    
    #normalise for measures: subtract each measure offset from the respective
    #measure
    for i in range(len(meloffcopy)):
        for j in range(len(measureoff)):
            if meloffcopy[i] >= measureoff[j] and meloffcopy[i] < measureoff[j+1]:
                meloffcopy[i] = meloffcopy[i] - measureoff[j];
    
    
    #get the offsets and pitches of one pattern into one list
    for i in range(len(offlists)):
        for j in range(len(meloffcopy)):
            if meloff[j] >= patternoff[i] and meloff[j] < patternoff[i+1]:
                offlists[i].append(meloffcopy[j]);
                mellists[i].append(mel[j].pitch.midi);
                beatlists[i].append(melbeats[j]);


    #create the string: on each pattern beginning, check for a time signature
    #and grouping occurence and print them, then print the offsets of the melody
    tmpStr = str();
#    explanation: ".beat" counts from the back of the bar, so it gets
#    appoggiaturas right, but not last bars that are truncated due to the
#    appoggiatura at the beginning of a piece. Therefore, we need to use another
#    way for everything except the first bar (actually, everything except the
#    last bar, but Python makes it easier this way), so we use a boolean to
#    do something once at the beginning of the loop, then change the procedure
#    when the boolean is false.
    halpbool = True;
    for i in range(len(offlists)):
        if halpbool:
            if ts[0].offset == patternoff[i]:
                tmpStr += 'TS\t' + str(ts[0].numerator) + '/' + str(ts[0].denominator) + '\t\n';
            if gr[0].offset == patternoff[i]:
                tmpStr += 'Grp\t' + str(gr[0].beat-1) + '\t\n'; 
            tmpStr += 'Bar\t' + str(beatlists[i]) + '\t' + str(mellists[i]) + '\n';                            
            halpbool = False;
        else:
            #time signatures
            for j in range(0, len(ts)):
                if ts[j].offset == patternoff[i]:
                    tmpStr += 'TS\t' + str(ts[j].numerator) + '/' + str(ts[j].denominator) + '\t\n';
            #tonality
#            for l in range(0, len(ton)):
#                if ton[l].offset == patternoff[i]:
#                    tmpStr += 'Ton\t' + str([tone.midi for tone in ton[l].pitches]) + '\t\n';
            #grouping                               
            for k in range(len(gr)):
                if gr[k].offset == patternoff[i]:
                    tmpStr += 'Grp\t' + str(gr[k].beat-1) + '\t\n';
            #melody                               
            tmpStr += 'Bar\t' + str(offlists[i]) + '\t' + str(mellists[i]) + '\n';
                                
    #a little tweaking to delete the empty line at the end
    tmpStr = tmpStr[:-1];

    #name management of file, open it
    splitName = pieceName.split('.');
    noExtName = splitName[0];
    finalName = noExtName+'.txt';
    text_file = open(finalName, 'w');

    #write file
    text_file.write(tmpStr);
    text_file.close();
    os.rename(currFolder+finalName, destFolder+finalName);