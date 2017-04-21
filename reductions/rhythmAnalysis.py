# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 15:49:08 2016

@author: User
"""

import numpy;

def analysis(s, pieceName, currFolder, destFolder):
    lines = s.split('\n');
    tscount = 0;
    for i in lines:
        #counter for amount of categories
        if lines[i][0] == 'T':
            tscount += 1;
#            
#    #create the correct amount of categories
#    ts = [[] for i in tscount];
#
#    #categorise
#    for i in lines:
#        k = 0;
#        for j in ts:
#            j[k] = i;
#    
#    patterns = [[] for i in tscount];
#    counts = [[0] for i in tscount];
#    onlyPatterns = lines
#    #count each pattern needs recursion...
#    for 
#    
#    
#def recursion(self, lins, pats, cots):
#    for i in lins:
#        for j in pats:
#            if lins[i] == pats[j]:
#                cots[j] += 1;
#            else:
#                pats.append(lins[i]);
#                cots.append(1);