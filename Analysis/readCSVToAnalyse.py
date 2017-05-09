# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 18:28:03 2016

@author: User
"""
#This script analyses .csv-files given in the following format:
#Category (TS; Grp; Bar) | Harmonic rhythm offsets | Melody offsets | Melody pitches
#String | String(Float) | String(List(Float)) | String(List(Int))

import csv;
import analysis;

rows = [];
with open('BC_001_026900B_a1.txt.csv', newline='') as file:
    dialect = csv.Sniffer().sniff(file.read(500));
    file.seek(0);
    reader = csv.reader(file, dialect);
    for row in reader:
        if 'Bar' in row:
            row[2] = row[2].replace('[', '');
            row[2] = row[2].replace(']', '');
            row[2] = row[2].replace(',', '');
            row[3] = row[3].replace('[', '');
            row[3] = row[3].replace(']', '');
            row[3] = row[3].replace(',', '');
        rows.append(row);

giant_list = analysis.splitintolists(rows);
#giant_list contains hr, mr, mp, grp, ts in chronological lists
# harmonic_rhythm = analysis.patfrequency(giant_list[0]);
# melodic_rhythm = analysis.patfrequency(giant_list[1]);
# print('Harmonic Rhythm\n')
# print(harmonic_rhythm);
# pattern_comparison = analysis.patcomparison(giant_list[0], giant_list[1]);
# print('\n\n\nPattern Comparison\n' + str(pattern_comparison));
pitch_analysis = analysis.pitchana(giant_list[2]);
print('\n\n\nPitch Analysis\n' + str(pitch_analysis))
