"""
COBRA-TF full core, subchannel-by-subchannel model
(c) DrSdl 2018
simple CTF output read routines
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random


# first, open ctf.chan.out and read some channel properties
# for a full core with ~44000 channels this is really a big data task,
# but for our 3x3 FA toy problem, we do not need the help of Spark or HDF

fileout = 'KXX_SIM5_1-1-1_281218.ctf.{:s}'

fileout_chan=fileout.format('chans.out')
fileout_gaps=fileout.format('gaps.out')

# for the time being we only want to read the liq. mass flow rate and the pressure per channel from chans.out
#
# https://stackoverflow.com/questions/3277503/how-to-read-a-file-line-by-line-into-a-list
# https://stackoverflow.com/questions/3437059/does-python-have-a-string-contains-substring-method
# https://stackoverflow.com/questions/16729574/how-to-get-a-value-from-a-cell-of-a-dataframe

#df_chan = pd.DataFrame()
df_chan = np.zeros((36,2209))
df_pres = np.zeros((36,2209))

check=0
sum=0
ars=[]
with open(fileout_chan) as f:
    for line in f:
        ## read in liq. mass flow rate ----------------------------------------------
        if "Fluid properties for channel" in line and "(table 1)" in line:
            chnr = int(line[34:40])
            #print(line, ' ** ', chnr)
            check=1
        if check==1:
            sum += 1
        if check==1 and sum==11:
            #print(line)
            check=2
            sum=0
        if check==2:
            level=int(line[0:3])
            fliq=float(line[50:60])
            #df_chan.iat[level,chnr]=fliq
            df_chan[level-1, chnr-1] = fliq
            sum += 1
            if level == 1:
                check =0
                sum=0
        ## read in pressure ---------------------------------------------------------
        if "Fluid properties for channel" in line and "(table 2)" in line:
            chnr = int(line[34:40])
            #print(line, ' ** ', chnr)
            check=10
        if check==10:
            sum += 1
        if check==10 and sum==11:
            #print(line)
            check=20
            sum=0
        if check==20:
            level=int(line[0:3])
            press=float(line[16:26])
            df_pres[level-1, chnr-1] = press
            sum += 1
            if level == 1:
                check =0
                sum=0
# ------------------------------------------------------------------------------------------------------------
# plot a couple of channels
#
#plt.subplot(211)
#plt.plot(df_chan[:,15:16])   # Mittenkanal
#plt.subplot(212)
#plt.plot(df_pres[:,1000:1010]) # Mittenkanal
#plt.show()

# ------------------------------------------------------------------------------------------------------------
# plot all channels for a single fuel assembly
#

