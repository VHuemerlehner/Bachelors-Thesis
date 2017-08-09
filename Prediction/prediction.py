# This script will create a predicted harmonic rhythm for a given melody and
# a .txt-file containing a 2X9 matrix of probabilities

import analysis as a
import numpy as np

#TODO ana = a.splitintolists(file)
# ana[0] are hr; ana[1] are mr; ana[4] are ts
# hr = ana[0]
# mr = ana[1]
# mp = ana[2]
# ts = ana[4]
# patana = a.patcomparison(hr, mr, ts)
# sync = patana[1]
# pitchanalysis = a.pitchana(mp, hr, mr, ts)
# intervals = pitchanalysis[0]
# contour = pitchanalysis[1]

#What we want: Overall percentage of hr on mr to be close to txt[0,1] (prob for
#hr given mr) distributed such that the most likely mr's receive them. Thus:
#Give likelihoods to all mr's, then choose the highest ones until percentage is
#reached.


for i in mr:
