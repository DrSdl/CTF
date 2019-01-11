"""
COBRA-TF full core, subchannel-by-subchannel model
(c) DrSdl 2018
simple CTF output read routines for transient cases
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import h5py

# activate for DISPLAY-less systems
#plt.switch_backend('agg')

# check online how far the transient calculation proceeded:
# grep 'Fluid properties for channel    2  (table 1)' *090119.ctf.chans.*
#
# first, open ctf.chan.out and read some channel properties
# for a full core with ~44000 channels this is really a big data task,
# but for our 3x3 FA toy problem, we do not need the help of Spark or HDF

fileout = 'KXX_SIM5_1-1-1_090119.ctf.{:s}'
fileh5  = 'KXX_SIM5_1-1-1_090119.h5'

fileout_chan=fileout.format('chans.out')
fileout_gaps=fileout.format('gaps.out')

# for the time being we only want to read the liq. mass flow rate and the pressure per channel from chans.out
#
# https://stackoverflow.com/questions/3277503/how-to-read-a-file-line-by-line-into-a-list
# https://stackoverflow.com/questions/3437059/does-python-have-a-string-contains-substring-method
# https://stackoverflow.com/questions/16729574/how-to-get-a-value-from-a-cell-of-a-dataframe

#df_chan = pd.DataFrame()
# we assume a maximum of 100 time steps
Ntime=100
df_chan = np.zeros((36,2209,Ntime))
df_pres = np.zeros((36,2209,Ntime))
df_temp = np.zeros((36,2209,Ntime))
df_cros = np.ones((2209*2,3+36,Ntime)) # maximum of 2 neighboring channels per channel

rangX=2209
rangY=2209,
rangN=36

xtimeSet=[]
print("get info of the number of time steps ...")
# ------------------------------------------------------------------------------------------------------------
# read channel mass flux and pressure
with open(fileout_chan) as f:
    for line in f:
        if "Fluid properties for channel" in line and "(table 1)" in line:
            xtime=float(line[71:81])
            if xtime not in xtimeSet:
                xtimeSet.append(xtime)
# ------------------------------------------------------------------------------------------------------------
print('found ',len(xtimeSet), 'time steps: ')
print(xtimeSet)
NXtime=len(xtimeSet)

check=0
sum=0
ars=[]
print("read channel information ...")
# ------------------------------------------------------------------------------------------------------------
# read channel mass flux and pressure
with open(fileout_chan) as f:
    for line in f:
        ## read in liq. mass flow rate ----------------------------------------------
        if "Fluid properties for channel" in line and "(table 1)" in line:
            chnr = int(line[34:40])
            xtime = float(line[71:81])
            timeID = xtimeSet.index(xtime)
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
            df_chan[level-1, chnr-1,timeID] = fliq
            sum += 1
            if level == 1:
                check =0
                sum=0
        ## read in pressure ---------------------------------------------------------
        if "Fluid properties for channel" in line and "(table 2)" in line:
            chnr = int(line[34:40])
            xtime = float(line[71:81])
            timeID = xtimeSet.index(xtime)
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
            df_pres[level-1, chnr-1, timeID] = press
            sum += 1
            if level == 1:
                check =0
                sum=0

# ------------------------------------------------------------------------------------------------------------
# read channel temperatures
with open(fileout_chan) as f:
    for line in f:
        ## read in channel temperatures ----------------------------------------------
        if "Fluid properties for channel" in line and "(table 3)" in line:
            chnr = int(line[34:40])
            xtime = float(line[71:81])
            timeID = xtimeSet.index(xtime)
            #print(line, ' ** ', chnr)
            check=1
        if check==1:
            sum += 1
        if check==1 and sum==15:
            #print(line)
            check=2
            sum=0
        if check==2:
            #print(line)
            level=int(line[0:3])
            temp=float(line[80:88])
            #df_chan.iat[level,chnr]=fliq
            df_temp[level-1, chnr-1,timeID] = temp
            sum += 1
            if level == 2:
                df_temp[level - 2, chnr - 1, timeID]=df_temp[level - 1, chnr - 1, timeID]
                check =0
                sum=0


# ------------------------------------------------------------------------------------------------------------
# we want to read out cross-flow between channels, too
# ------------------------------------------------------------------------------------------------------------
# read channel temperatures
NrGaps=0
sum=0
check=0

print("read gaps information ...")
with open(fileout_gaps) as f:
    for line in f:
        ## read in channel temperatures ----------------------------------------------
        if "Fluid properties for gap" in line and "(table 1)" in line:
            chnr = int(line[30:36])
            xtime = float(line[67:77])
            timeID = xtimeSet.index(xtime)
            NrGaps = chnr - 1
            #print(line, ' ** ', chnr)
            check=1
        if check==1:
            sum += 1
        if check==1 and sum==4:
            chnrFrom=int(line[39-1:44-1])
            chnrTo=int(line[48-1:53-1])
            df_cros[NrGaps, 0, timeID] = NrGaps
            df_cros[NrGaps, 1, timeID] = chnrFrom
            df_cros[NrGaps, 2, timeID] = chnrTo
            #print(line," ** ", chnrFrom, ", ", chnrTo)
        if check==1 and sum==13:
            #print(line)
            check=2
            sum=0
        if check==2:
            #print(line)
            level=int(line[0:3])
            cross=float(line[47-1:55-1])
            #
            df_cros[NrGaps, 2 + level, timeID] = cross
            sum += 1
            if level == 2:
                #df_cros[NrGaps, 2 + 1] = df_cros[NrGaps, 2 + 1 + 1]
                # 0 cross flow at inlet
                df_cros[NrGaps, 2 + 1, timeID] = 0
                check =0
                sum=0
                #NrGaps += 1

print('total number of gaps: ', NrGaps)
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

# read in channel layout data
with h5py.File(fileh5, 'r') as hf:
    rodS = hf["channel_IDs"][:]
    rodK = hf["rod_IDs"][:]
    rodH = hf["rod_types"][:]
    rodU = hf["rod_FA_ID"][:]

# in this example central assembly has all rods with FA name "14", "15"
# get all channel IDs within this fuel assembly
centralS14=[]
neighbrS15=[]

nX,nY = rodS.shape
for i in range(nY):
    for j in range(nX):
        if j>=17-1 and j<=31-1 and i>=17-1 and i<=31-1:
            centralS14.append(rodS[i,j])

for i in range(nY):
    for j in range(nX):
        if j>=33-1 and j<=47-1 and i>=17-1 and i<=31-1:
            neighbrS15.append(rodS[i,j])

#print(centralS14)

# finally we have to select all the gaps of a fuel assemblies' boundary
# first, collect the inner boundary channels of fuel assembly "14"
# second, collect the outer boudary channels of fuel assembly "14"
innerS14=[]
outerS14=[]

for i in range(nY):
    for j in range(nX):
        if (j>=17-1 and j<=31-1 and i==17-1) or (j>=17-1 and j<=31-1 and i==31-1) or (i>17-1 and i<31-1 and j==17-1) or (i>17-1 and i<31-1 and j==31-1):
            innerS14.append(rodS[i,j])

for i in range(nY):
    for j in range(nX):
        if (j>=16-1 and j<=32-1 and i==16-1) or (j>=16-1 and j<=32-1 and i==32-1) or (i>16-1 and i<32-1 and j==16-1) or (i>16-1 and i<32-1 and j==32-1):
            outerS14.append(rodS[i,j])


sx=len(innerS14)
sy=len(outerS14)
gapFence=[]

for i in range(sx):
    for j in range(sy):
        ch1 = innerS14[i]
        ch2 = outerS14[j]
        for k in range(NrGaps):
            if (df_cros[k,1,0]==ch1 and df_cros[k,2,0]==ch2) or (df_cros[k,1,0]==ch2 and df_cros[k,2,0]==ch1):
                gapFence.append(k)

print("number of fence gaps for central assembly: ", len(gapFence))

debugg=0
# ------------------------------------------------------------------------------------------------
# print inlet mass flux for central assembly channels to check if all has gone to plan
# print outlet mass flux for central assembly channels to check if all has gone to plan

plt.subplot(211)
x=df_chan[0,centralS14,0:NXtime].T
plt.plot(x)

plt.subplot(212)
x=df_chan[35,centralS14,0:NXtime].T
plt.plot(x)
if debugg==1:
    plt.show()
else:
    plt.savefig('ctf.transient.fig1.jpeg')
    plt.clf()

# Temperature plot as a function of time ----------------------------------------------

plt.subplot(211)
xLevel0 =df_temp[0,centralS14,0:NXtime].T   ; plt.plot(xLevel0)
xLevel10=df_temp[10,centralS14,0:NXtime].T  ; plt.plot(xLevel10)
xLevel20=df_temp[20,centralS14,0:NXtime].T  ; plt.plot(xLevel20)
xLevel30=df_temp[30,centralS14,0:NXtime].T  ; plt.plot(xLevel30)

plt.subplot(212)
xLevel0 =df_temp[0,neighbrS15,0:NXtime].T   ; plt.plot(xLevel0)
xLevel10=df_temp[10,neighbrS15,0:NXtime].T  ; plt.plot(xLevel10)
xLevel20=df_temp[20,neighbrS15,0:NXtime].T  ; plt.plot(xLevel20)
xLevel30=df_temp[30,neighbrS15,0:NXtime].T  ; plt.plot(xLevel30)

if debugg==1:
    plt.show()
else:
    plt.savefig('ctf.transient.fig2.jpeg')
    plt.clf()


timeID=5
# Mass flux plot at one specific point in time ---------------------------------------------
plt.subplot(211)
plt.plot(df_chan[:,centralS14,timeID])   # Mittenkanal
plt.subplot(212)
plt.plot(df_chan[:,neighbrS15,timeID])   # rechter Seitenkanal

if debugg==1:
    plt.show()
else:
    plt.savefig('ctf.transient.fig3.jpeg')
    plt.clf()

# Pressure plot at one specific point in time ----------------------------------------------
plt.subplot(211)
plt.plot(df_pres[:,centralS14,timeID])   # Mittenkanal
plt.subplot(212)
plt.plot(df_pres[:,neighbrS15,timeID])   # rechter Seitenkanal

if debugg==1:
    plt.show()
else:
    plt.savefig('ctf.transient.fig4.jpeg')
    plt.clf()

# Temperature plot at one specific point in time ----------------------------------------------
plt.subplot(211)
plt.plot(df_temp[:,centralS14,timeID])   # Mittenkanal
plt.subplot(212)
plt.plot(df_temp[:,neighbrS15,timeID])   # rechter Seitenkanal

if debugg==1:
    plt.show()
else:
    plt.savefig('ctf.transient.fig5.jpeg')
    plt.clf()

# gap flux plot at one specific point in time -------------------------------------------------
plt.subplot(211)
h=df_cros[gapFence,3:39,timeID]
h=h.T
plt.plot(h)   # Mittenkanal

if debugg==1:
    plt.show()
else:
    plt.savefig('ctf.transient.fig6.jpeg')
    plt.clf()


"""
file sizes for 18 seconds with 0.1s resolution:

[drsdl@localhost work]$ du -sh  *090119*
8.3G    KXX_SIM5_1-1-1_090119.ctf.chans.out
60M     KXX_SIM5_1-1-1_090119.ctf.chans.vtk
4.0G    KXX_SIM5_1-1-1_090119.ctf.dnb.out
3.8G    KXX_SIM5_1-1-1_090119.ctf.gaps.out
40K     KXX_SIM5_1-1-1_090119.ctf.heat.out
716K    KXX_SIM5_1-1-1_090119.ctf.krysolv.out
0       KXX_SIM5_1-1-1_090119.ctf.log
32K     KXX_SIM5_1-1-1_090119.ctf.mass.out
18G     KXX_SIM5_1-1-1_090119.ctf.out
460K    KXX_SIM5_1-1-1_090119.ctf.run.out
5.1M    KXX_SIM5_1-1-1_090119.inp
13M     KXX_SIM5_1-1-1_090119.zip

"""