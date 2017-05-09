# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 14:15:38 2016

@author: User
"""
#Helper function to find word in string:

def smart_find(haystack, needle):
    if haystack.startswith(needle+" "):
        return 0;
    if haystack.endswith(" "+needle):
        return len(haystack);
    if haystack.find(" "+needle+" ") != -1:
        return haystack.find(' ' + needle + ' ');
    return -1;

#This function splits the long list of rows of the .csv-files into five
#separate ones containing information about harmonic rhythm, melodic rhythm,
#melody pitches, grouping and time signatures. These lists get appended into
#one list as return value.

#Our input: A list with a list for each row of the .csv, containing either:
#TS - 3/4 OR Grp - 0.0 OR - Bar - (Harmonic Rhythm) 0 2  - cont.
#(Melodic Rhythm) 0 1 2 3 - (Pitches) 66 68 70 71

##DOCUMENTATIONISFORPUSSIES #IHATEMYSELFALREADY #GOTLUCKYREMEMBEREDEVERYTHING
#The following function creates five lists of equal length: tsinf, grpinf
#hrinf, mrinf and mpinf. Each of them contains for each bar in sequence: Time
#Signature, grouping (1 = beginning of group, 2 = intermediate, 3 = ending)
#, harmonic rhythm, melodic rhythm, or melody pitches respectively.

def splitintolists(data):
    #We need five lists and two counting variables
    hrinf = [];
    mrinf = [];
    mpinf = [];
    grpinf = [];
    tsinf = [];
    tsstring = '';
    grpint = 0;

    #Iterating over the entire data
    for i in range(len(data)):
        #If we find a new TS, change the counting variable accordingly
        if data[i][0] == 'TS':
            tsstring = data[i][1];
        #If we find a new Grouping boundary, set grouping info to 1
        elif data[i][0] == 'Grp':
            grpint = 1;
        #Now the complicated part: If we find a bar pattern, add it to the
        #lists and add the TS to the list. Change Grouping info accordingly:
        #If the next info in data is a grouping boundary, set to 3; if there
        #is a TS in between, but no bar, also set to 3; if it is a TS and
        #a bar, set it to 2; if the next data point is a bar, set it to 2;
        #If we are at the end of our data, set to 3; If we just had a grouping
        #boundary, leave the counting variable at 3 or 1, if it is a 2, change
        #to 1 (Explanation: We consider a group ending to be more significant
        #than a group beginning, should they occur at the same time (meaning
        #that the group is only one bar long), so the priority is: 3-1-2).
        elif data[i][0] == 'Bar':
            hrinf.append(data[i][1]);
            mrinf.append(data[i][2]);
            mpinf.append(data[i][3]);
            tsinf.append(tsstring);
            if len(data)>i+1:
                if data[i+1][0] == 'Grp':
                    grpint = 3;
                elif data[i+1][0] == 'TS':
                    if data[i+2][0] == 'Grp':
                        grpint = 3;
                    elif data[i+2][0] == 'Bar':
                        grpint = 2;
                elif data[i+1][0] == 'Bar':
                    grpint = 2;
            else:
                grpint = 3;
            if data[i-1][0] == 'Grp':
                if grpint == 2:
                    grpint = 1;
            grpinf.append(grpint);

    #Convert hrinf, mrinf and mpinf from string to tuple of 'floats':
    #Find all one-letter words (=integers) in hrinf and add '.0' behind them.
    for i in range(len(hrinf)):
        for word in hrinf[i].split():
            if len(word) == 1:
                place = hrinf[i].find(word) + 1;
                temp = hrinf[i];
                hrinf[i] = temp[:place] + '.0' + temp[place:];
        hrinf[i] = list(hrinf[i].split());
        mrinf[i] = list(mrinf[i].split());
        mpinf[i] = list(mpinf[i].split());

#    For debugging:
#    print('Harmonic Rhythm\n');
#    print(hrinf);
#    print('\n\nMelodic Rhythm\n');
#    print(mrinf);
    # print('\n\nMelody Pitches\n');
    # print(mpinf);
#    print('\n\nGrouping\n')
#    print(grpinf);
#    print('\n\nTime Signatures\n')
#    print(tsinf);
#    print('\n\n\nAre all lists of equal length?\n' + str((len(hrinf) == len(mrinf)) and (len(mpinf) == len(grpinf)) and (len(grpinf) == len(tsinf))));

    #Write it all in one list so we only hand around one object. Like a folder. Just dumb.
    returnlist = [];
    returnlist.append(hrinf);
    returnlist.append(mrinf);
    returnlist.append(mpinf);
    returnlist.append(grpinf);
    returnlist.append(tsinf);
    return returnlist;


# The following function sums over a list of given rhythmic patterns to
# determine the frequency of each occuring pattern. It outputs a dictionary
# with 'pattern: [sum, frequency]'.
def patfrequency(rpinf):
    # Initialising variables: 2 lists for patterns and occurences and the dict
    # to put it all in;
    rpdict = {};
    patlist = [];
    occurencelist = [];

    # Running through the data, make a marker for new or old pattern
    for i in rpinf:
        newTS = True;
        for j in patlist:
            if i == j:
                newTS = False;
        # If the pattern is new, add it to the list and add an occurence entry
        if newTS:
            patlist.append(i);
            occurencelist.append(1);
        # Else find it in the list and edit the corresponding occurence entry
        else:
            k = 0;
            while (i != patlist[k]) and (k<len(patlist)):
                k += 1;
            occurencelist[k] += 1;

    # Write it all into the dict
    for i in range(len(patlist)):
        rpdict.update({tuple(patlist[i]): [occurencelist[i], occurencelist[i]/len(rpinf)]});
    return rpdict;


# The following function compares melodic and harmonic rhythmic patterns:
# It counts the number of cooccurring onsets, gives a percentage for each
# melodic and harmonic overall onsets and measures the difference in number
# of onsets in each bar. Output: [cooccurences abs, per measure, percentage of
# harmony onsets, percentage of melody onsets, mel_on-harm_on abs, per measure]

#########TODOOOOOOOOOO!!! Check for speed and complexity of melodic and harmonic
# rhythm, correlate them, find something?


def patcomparison(hr, mr):
    results = [];
    coocc = 0;
    honsets = 0;
    monsets = 0;
    for i in range(len(hr)):
        honsets += len(hr[i]);
        monsets += len(mr[i]);
        for k in hr[i]:
            for l in mr[i]:
                 monsets += 1;
                 if k == l:
                     coocc += 1;

    results.append(coocc);
    results.append(coocc/len(hr));
    results.append(coocc/honsets);
    results.append(coocc/monsets);
    results.append(monsets-honsets);
    results.append((monsets-honsets)/len(hr));
    return results;


#This function analyses the melody in terms of pitch: It extracts its contour,
#i.e. when it rises or falls and calculates a measure for movement by adding up
#the distances between (time-)adjacent pitches. Another idea might be to scale
#pitches in terms of their relation (i.e. octave/unison score low, septs and
#tritones very high) and add this up. This can then be correlated to the number
#of harmony changes in the corresponding bar/piece.
def pitchana(mp):
    results = [];
    pitches = [];
    # First, we need to get all pitches into one long list of integers
    for i in mp:
        for j in i:
            pitches.append(int(j));
    contour = [None] * (len(pitches)-1);
    contoursign = [None] * (len(pitches)-1);
    contourabs = [None] * (len(pitches)-1);
    distanceabs = 0;
    distancerel = 0;


########### FIND LITERATURE ON THE VALENCE OF INTERVALS
    # then, we could find a "tonal" distance of the melody.
    distancetonal = [];

    # Working definition of contour: Distances between adjacent tones. May need
    # to be revised later on! Contoursign extracts only the direction of
    # movement, contourabs only the amount of movement
    # First, we need to get all pitches into one list to iterate through.
    # ------- IDEA: delete unisons? pro: does not contribute to contour
    # con: may contribute to harmonic rhythm (harmonically reinterpreted "equal" pitches)
    for i in range(len(pitches)-1):
        contour[i] = pitches[i+1]-pitches[i];
        if contour[i] > 0:
    	    contoursign[i] = 1;
    	    contourabs[i] = contour[i];
        elif contour[i] < 0:
    	    contoursign[i] = -1;
    	    contourabs[i] = -contour[i];
        elif contour[i] == 0:
    	    contoursign[i] = 0;
    	    contourabs[i] = 0;

    for i in range(len(contourabs)):
    	distanceabs = distanceabs + contourabs[i];

    distancerel = distanceabs/(len(pitches)-1);
    print(distanceabs);
    print(distancerel);

    # Write everything into the results-handle for return
    results.append(contour);
    results.append(contourabs);
    results.append(contoursign);
    results.append(distanceabs);
    results.append(distancerel);
    results.append(distancetonal);

    return results;
