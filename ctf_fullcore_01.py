"""
COBRA-TF full core, subchannel-by-subchannel model
(c) DrSdl 2018
simple CTF input write routine
"""

import numpy as np
import matplotlib.pyplot as plt
import random
import hdf5

# defines the basic RPI asset class
class SubChannel:

    myID='SubChannel'             # class variable shared by all instances

    def __init__(self, SubChannelID):
        self.name = SubChannelID       # instance variable unique to each instance
        self.typus='SubChannel'
        self.ChannelNumber=0
        self.ChannelArea=0
        self.ChannelNeighbors = [0, 0, 0, 0]    ## number ID of neighboring channels
        self.RodNeighbors = [0, 0, 0, 0]        ## number ID of neighboring rods
        self.RodTypeNeighbors = [0, 0, 0, 0]    ## type of rod neighbors
        self.FANumberNeighbors = [0, 0, 0, 0]   ## fuel assembly IDs of each neighbor rod
        self.ChannelX=0
        self.ChannelY=0
        self.PerimeterWet=0
        self.PositionX=0
        self.PositionY=0
        self.SizeX=0
        self.SizeY=0

    def getId(self):
        return self.name

    # set and get class type ------------------------------------------

    def setType(self, myType):
        self.typus = myType

    def getType(self):
        return self.typus

    # set and get subchannel number ------------------------------------
    def setChannelNumber(self, myNumber):
        self.ChannelNumber = myNumber

    def getChannelNumber(self):
        return self.ChannelNumber

    # set and get subchannel area (cm2) --------------------------------
    def setChannelArea(self, myX):
        self.ChannelArea = myX

    def getChannelArea(self):
        return self.ChannelArea

    # set and get array which contains the 4 subchannel neighbors ------
    def setChannelNeighbors(self, n, myX):
        self.ChannelNeighbors[n] = myX

    def getChannelNeighbors(self):
        return self.ChannelNeighbors

    # set and get array which contains the 4 neighboring rods ----------
    def setRodNeighbors(self, n, myX):
        self.RodNeighbors[n] = myX

    def getRodNeighbors(self):
        return self.RodNeighbors

    # set and get the channel X-coordinate -----------------------------
    def setChannelX(self, myX):
        self.ChannelX = myX

    def getChannelX(self):
        return self.ChannelX

    # set and get the channel Y-coordinate -----------------------------
    def setChannelY(self, myX):
        self.ChannelY = myX

    def getChannelY(self):
        return self.ChannelY

    # set and get the channel wetted perimeter -----------------------------
    def setPerimeterWet(self, myX):
        self.PerimeterWet = myX

    def getPerimeterWet(self):
        return self.PerimeterWet

    # set and get the channel x-position       -----------------------------
    def setPositionX(self, myX):
        self.PositionX = myX

    def getPositionX(self):
        return self.PositionX

    # set and get the channel y-position       -----------------------------
    def setPositionY(self, myX):
        self.PositionY = myX

    def getPositionY(self):
        return self.PositionY

    # set and get the channel x-size           -----------------------------
    def setSizeX(self, myX):
        self.SizeX = myX

    def getSizeX(self):
        return self.SizeX

    # set and get the channel y-size           -----------------------------
    def setSizeY(self, myX):
        self.SizeY = myX

    def getSizeY(self):
        return self.SizeY

    # print CTF channel data                   -----------------------------
    def printCTFchannel(self):
        #print('   ',self.ChannelNumber,'   ',self.getChannelArea()*0.01*0.01,'   ',self.getPerimeterWet()*0.01*0.01, '   0 0 0 ', '   ',self.getPositionX(), '   ',self.getPositionY(), '   ',self.getSizeX(), '   ',self.getSizeY())
        #x='   '+str(self.ChannelNumber)+'   '+str(self.getChannelArea()*0.01*0.01)+'   '+str(self.getPerimeterWet()*0.01)+'   0 0 0 '+'   '+str(self.getPositionX()*0.01)+'   '+str(self.getPositionY()*0.01)+'   '+str(self.getSizeX()*0.01)+'   '+str(self.getSizeY()*0.01)
        x='   '
        x = x + '{:5n}'.format(self.ChannelNumber)
        x = x + '   '
        x = x + '{:10.8f}'.format(self.getChannelArea() * 0.01 * 0.01)
        x = x + '   '
        x = x + '{:10.8f}'.format(self.getPerimeterWet() * 0.01)
        x = x + '   0 0 0   '
        x = x + '{:10.8f}'.format(self.getPositionX() * 0.01)
        x = x + '   '
        x = x + '{:10.8f}'.format(self.getPositionY() * 0.01)
        x = x + '   '
        x = x + '{:10.8f}'.format(self.getSizeX() * 0.01)
        x = x + '   '
        x = x + '{:10.8f}'.format(self.getSizeY() * 0.01)
        return x

    # set and get array which contains the 4 neighboring rod types ------------------------
    def setRodTypeNeighbors(self, n, myX):
        self.RodTypeNeighbors[n] = myX

    def getRodTypeNeighbors(self):
        return self.RodTypeNeighbors

    # set and get array which contains the 4 neighboring rod's fuel assembly IDs ----------
    def setFANumberNeighbors(self, n, myX):
        self.FANumberNeighbors[n] = myX

    def getFANumberNeighbors(self):
        return self.FANumberNeighbors

    # return number of fuel rod types in neighborhood
    def getNumberOfRodTypes(self):
        x=set(self.RodTypeNeighbors)
        return len(x)

    # return number of fuel assembly names in neighborhood
    def getNumberOfNeighborFuel(self):
        x=set(self.FANumberNeighbors)
        return len(x)


# define template file
filein  = 'KXX_SIM5_1-1-1_template'
# define destination file
fileout = 'KXX_SIM5_1-1-1_281218.inp'
fileh5  = 'KXX_SIM5_1-1-1_281218.h5'

# define fuel assembly NxN matrix
N_x=3
# define number of fuel rods nxn per fuel assembly
N_r=16
# define pitch between fuel rods (cm)
r_p=1.43
# define pitch between fuel assemblies (cm)
r_f=23.0
# define radius of fuel rods (cm)
r_r=1.075/2
# define radius of guide tube (cm)
r_g=1.380/2
# define fuel assembly IDs
FAIds=[10, 11, 12, 13, 14, 15, 16, 17, 18]
# define fuel assembly type layout, i.e. rod (1) versus guide tube (0) (has to be consistent with Nr)
rodN=np.array([ [1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1],
                [1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1],
                [1,  1,  0,  1,  1,  0,  1,  1,  1,  1,  0,  1,  1,  0,  1,  1],
                [1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1],
                [1,  1,  1,  1,  1,  1,  0,  1,  1,  0,  1,  1,  1,  1,  1,  1],
                [1,  1,  0,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  0,  1,  1],
                [1,  1,  1,  1,  0,  1,  1,  1,  1,  1,  1,  0,  1,  1,  1,  1],
                [1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1],
                [1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1],
                [1,  1,  1,  1,  0,  1,  1,  1,  1,  1,  1,  0,  1,  1,  1,  1],
                [1,  1,  0,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  0,  1,  1],
                [1,  1,  1,  1,  1,  1,  0,  1,  1,  0,  1,  1,  1,  1,  1,  1],
                [1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1],
                [1,  1,  0,  1,  1,  0,  1,  1,  1,  1,  0,  1,  1,  0,  1,  1],
                [1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1],
                [1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1]])

# rodN: fuel assembly rod type layout
# rodH: total fuel assembly rod type layout
# rodU: total fuel assembly ID matrix per rod
# rodS: total subchannel number layout
# rodK: total fuel rod number layout

# define active height of core (cm)
core_h=390.0
# define active core start from bottom (cm)
core_s=40.0
# define active core end from bottom (cm)
core_s=520.0
# define spacer grid locations botton to top (cm)
spacer=[ 60.0, 70.0, 80.0, 90.0,100.0,110.0,120.0,130.0,140.0]

# create global matrix of fuel rod type layout
# stack horizontally
rodG=np.copy(rodN)
for i in range(N_x-1):
    rodG=np.hstack((rodG,rodN))
# stack vertically
rodH=np.copy(rodG)
for i in range(N_x-1):
    rodH=np.vstack((rodH,rodG))

# https://stackoverflow.com/questions/1987694/how-to-print-the-full-numpy-array
# https://docs.scipy.org/doc/numpy/reference/generated/numpy.set_printoptions.html
np.set_printoptions(linewidth=1000) # doesn't seem to work...
np.set_printoptions(threshold=np.nan)
print('shape of rod type matrix: ', rodH.shape)
#print(rodH)

# create global matrix of fuel rod numbering layout
# total number of rods
N_total=N_r*N_r*N_x*N_x
print('total number of rods: ',N_total)
rodK=np.copy(rodH)
sum=1
for i in range(N_x*N_r):
    for j in range(N_x * N_r):
        rodK[i,j]=sum
        sum+=1

#print(rodK)
print('shape of rod number matrix: ', rodK.shape)

# create global matrix of subchannel layout
# total number of channels
S_total=(N_r*N_x-1)*(N_r*N_x-1)
print('total number of subchannels: ',S_total)
rodS=np.zeros((N_r*N_x-1, N_r*N_x-1), dtype=int)

sum=1
for i in range(N_x*N_r-1):
    for j in range(N_x * N_r-1):
        rodS[i,j]=sum
        sum+=1

#print(rodS)
print('shape of subchannel matrix: ', rodS.shape)

# how is the logic between rod number and subchannel numbers?                                   - - -x (j)
# rod numbers:         1  2  3  4  5  6  7  8  9  10  11  12  13  14  15  16     17 ...        |
# subchannel numbers:    1  2  3  4  5  6  7  8  9  10  11  12  13  14  15    16    17 ...     |
# rod numbers:         49 50 51 52 53 54 55 56 57 58  59  60  61  62  63  64     65 ...        y
# subchannel numbers:    48 49 50 51 52 53 54 55 56 57  58  59  60  61  62    63    64 ...    (i)
# ...

# Create the list of subchannel objects
#
S_list=[]
sum=1
for i in range(N_x*N_r-1):
    for j in range(N_x * N_r-1):
        sname=str(i+1)+';'+str(j+1)
        x = SubChannel(sname)
        x.setChannelNumber(sum)
        x.setChannelX(j+1)
        x.setChannelY(i+1)
        S_list.append(x)
        sum += 1

print('length of subchannel list: ', len(S_list))

# set neighbour channel list
##############################
#             N2
#    N1    Channel    N3
#             N4
##############################

for ch in S_list:
    #print('channel number: ',ch.getChannelNumber(), 'coord: ', ch.getChannelX(), '; ', ch.getChannelY())
    """
    if ch.getChannelNumber() == 1:
        ch.setChannelNeighbors(0, 0)
        ch.setChannelNeighbors(1, 0)
        ch.setChannelNeighbors(2, rodS[0,1])
        ch.setChannelNeighbors(3, rodS[1,0])

    if ch.getChannelNumber() == rodS[0,-1]:
        ch.setChannelNeighbors(0, rodS[0,-2])
        ch.setChannelNeighbors(1, 0)
        ch.setChannelNeighbors(2, 0)
        ch.setChannelNeighbors(3, rodS[2,-1])

    if ch.getChannelNumber() == rodS[-1,1]:
        ch.setChannelNeighbors(0, 0)
        ch.setChannelNeighbors(1, rodS[-2,1])
        ch.setChannelNeighbors(2, rodS[-1,2])
        ch.setChannelNeighbors(3, 0)

    if ch.getChannelNumber() == rodS[-1,-1]:
        ch.setChannelNeighbors(0, rodS[-1,-2])
        ch.setChannelNeighbors(1, rodS[-2,-1])
        ch.setChannelNeighbors(2, 0)
        ch.setChannelNeighbors(3, 0)
    """
    nrX=ch.getChannelX()
    nrY=ch.getChannelY()
    # ------------------------------------------------------------
    if (nrX-1)-1 < 0:
        ch.setChannelNeighbors(0, 0)
    else:
        ch.setChannelNeighbors(0, rodS[(nrY - 1), (nrX - 1) - 1] )
    # ------------------------------------------------------------
    if (nrY-1)-1 < 0:
        ch.setChannelNeighbors(1, 0)
    else:
        ch.setChannelNeighbors(1, rodS[(nrY - 1) - 1, (nrX - 1)] )
    # ------------------------------------------------------------
    if (nrX-1)+1 > N_r*N_x-2:
        ch.setChannelNeighbors(2, 0)
    else:
        ch.setChannelNeighbors(2, rodS[(nrY - 1), (nrX - 1) + 1 ])
    # ------------------------------------------------------------
    if (nrY-1)+1 > N_r*N_x-2:
        ch.setChannelNeighbors(3, 0)
    else:
        ch.setChannelNeighbors(3,  rodS[(nrY - 1) + 1, (nrX - 1) ])

    #print('channel number: ', ch.getChannelNumber(), 'neighbours: ', ch.getChannelNeighbors())


#for ch in S_list:
#    print('channel number: ',ch.getChannelNumber(), 'neighbours: ', ch.getChannelNeighbors())

##############################
# create fuel assembly ID layout
##############################
rodI = np.ones((N_r,N_r))
sum=0

for i in range(N_x):
    # stack vertically ----------
    rodx = rodI * FAIds[sum]
    for j in range(N_x-1):
        # stack horizontally ----
        rodx=np.hstack((rodx,rodI*FAIds[sum+1]))
        sum +=1
    if i==0:
        rodU=np.copy(rodx)
    else:
        rodU=np.vstack((rodU,rodx))
    sum += 1

##############################
# set neighbour rod list
##############################
#       R1           R2
#           Channel
#       R3           R4
##############################
# 24.12.2018
# we assume that all channels are surrounded by 4 rods, but corner rods do not need a full channel neighborhood
# i.e. corner rod power needs to be reduced by a factor 4

for ch in S_list:
    #print('channel number: ',ch.getChannelNumber(), 'coord: ', ch.getChannelX(), '; ', ch.getChannelY())
    nrX=ch.getChannelX()
    nrY=ch.getChannelY()
    ch.setRodNeighbors(0, rodK[(nrY - 1), (nrX - 1) ])
    ch.setRodNeighbors(1, rodK[(nrY - 1), (nrX - 1) +1 ])
    ch.setRodNeighbors(2, rodK[(nrY - 1) +1, (nrX - 1) ])
    ch.setRodNeighbors(3, rodK[(nrY - 1) +1, (nrX - 1) +1 ])

    ch.setRodTypeNeighbors(0, rodH[(nrY - 1), (nrX - 1) ])
    ch.setRodTypeNeighbors(1, rodH[(nrY - 1), (nrX - 1) +1 ])
    ch.setRodTypeNeighbors(2, rodH[(nrY - 1) +1, (nrX - 1) ])
    ch.setRodTypeNeighbors(3, rodH[(nrY - 1) +1, (nrX - 1) +1 ])

    ch.setFANumberNeighbors(0, rodU[(nrY - 1), (nrX - 1) ])
    ch.setFANumberNeighbors(1, rodU[(nrY - 1), (nrX - 1) +1 ])
    ch.setFANumberNeighbors(2, rodU[(nrY - 1) +1, (nrX - 1) ])
    ch.setFANumberNeighbors(3, rodU[(nrY - 1) +1, (nrX - 1) +1 ])
    # ------------------------------------------------------------
    #print('channel number: ', ch.getChannelNumber(), 'rod neighbours: ', ch.getRodNeighbors())


#for ch in S_list:
#    print('channel number: ',ch.getChannelNumber(), 'neighbours: ', ch.getChannelNeighbors())

# -----------------------------------------------------------------------------------------------------------
# fill channels with area size, wetted perimeter and x,y coordinate and size-x,size-y data
for ch in S_list:
    nrX=ch.getChannelX()
    nrY=ch.getChannelY()
    # calculate flow area
    condi=0
    xA = r_p * r_p - np.pi * r_r * r_r # standard area for subchannel
    # check if there is a guide tube
    # we assume that guide tube is NOT an an edge location
    x=ch.getNumberOfRodTypes()
    if x>1:
        condi=1
    if condi==1:
        xA=r_p * r_p - 0.75*np.pi * r_r * r_r - 0.25*np.pi * r_g * r_g
    # check if there is a gap between fuel assemblies in x OR y direction, i.e. edge channel
    addaGap = r_f - N_r*r_p
    x=ch.getNumberOfNeighborFuel()
    if x==2:
        condi=2 # edge location
    else:
        condi=4 # corner location
    if condi==2:
        xA=r_p * (r_p + addaGap) - np.pi * r_r * r_r
    # check if there is a gap between fuel assemblies in x AND y direction, i.e. corner channel
    if condi==4:
        xA=(r_p + addaGap) * (r_p + addaGap) - np.pi * r_r * r_r
    #
    ch.setChannelArea(xA)
    # calculate wetted perimeter
    xR=2*np.pi*r_r
    # according to CTF manual section 2.2.5 Pw=2*pi*sqrt(A/pi)
    xR=2*np.pi*np.sqrt(xA/np.pi)
    ch.setPerimeterWet(xR)
    # calculate x position
    # additional gaps between fuel assemblies not taken into account
    # different size of flow areas between assembies and at guide tubes not accounted for
    x=nrX*r_p
    ch.setPositionX(x)
    # calculate y position
    x=nrY*r_p
    ch.setPositionY(x)
    # calculate x- and y- size
    x=r_p
    ch.setSizeX(x)
    ch.setSizeY(x)

# -----------------------------------------------------------------------------------------------------------
# do sanity check
# --- check normal channel, edge channel, corner channel in a 3x3 array of 16x16 assemblies
# normal channel
print('sanity check for some channels:')
s1=S_list[1-1]
print('rod neighbor types: ', s1.getRodTypeNeighbors() ,' rod neighbor IDs: ', s1.getRodNeighbors() ,' rod neighbor FA name: ', s1.getFANumberNeighbors() ,' subchannel neighbor IDs: ', s1.getChannelNeighbors(), ' number of fuel rod types: ', s1.getNumberOfRodTypes(), ' number of FA names: ', s1.getNumberOfNeighborFuel())
# edge channel
s2=S_list[N_r-1]
print('rod neighbor types: ', s2.getRodTypeNeighbors() ,' rod neighbor IDs: ', s2.getRodNeighbors() ,' rod neighbor FA name: ', s2.getFANumberNeighbors() ,' subchannel neighbor IDs: ', s2.getChannelNeighbors(), ' number of fuel rod types: ', s2.getNumberOfRodTypes(), ' number of FA names: ', s2.getNumberOfNeighborFuel())
# edge channel
s3=S_list[(N_r*N_x-1)*(N_r-1)+1-1]
print('rod neighbor types: ', s3.getRodTypeNeighbors() ,' rod neighbor IDs: ', s3.getRodNeighbors() ,' rod neighbor FA name: ', s3.getFANumberNeighbors() ,' subchannel neighbor IDs: ', s3.getChannelNeighbors(), ' number of fuel rod types: ', s3.getNumberOfRodTypes(), ' number of FA names: ', s3.getNumberOfNeighborFuel())
# corner channel
s4=S_list[(N_r*N_x-1)*(N_r-1)+16-1]
print('rod neighbor types: ', s4.getRodTypeNeighbors() ,' rod neighbor IDs: ', s4.getRodNeighbors() ,' rod neighbor FA name: ', s4.getFANumberNeighbors() ,' subchannel neighbor IDs: ', s4.getChannelNeighbors(), ' number of fuel rod types: ', s4.getNumberOfRodTypes(), ' number of FA names: ', s4.getNumberOfNeighborFuel())
# guide-tube channel
s5=S_list[(N_r*N_x-1)*1+2-1]
print('rod neighbor types: ', s5.getRodTypeNeighbors() ,' rod neighbor IDs: ', s5.getRodNeighbors() ,' rod neighbor FA name: ', s5.getFANumberNeighbors() ,' subchannel neighbor IDs: ', s5.getChannelNeighbors(), ' number of fuel rod types: ', s5.getNumberOfRodTypes(), ' number of FA names: ', s5.getNumberOfNeighborFuel())

# -----------------------------------------------------------------------------------------------------------
card_group02 = ''
card_group03 = ''
card_group04 = ''
card_group07 = ''
card_group08 = ''
card_group11 = ''
card_group13 = ''
debugg = 0
# python literals: https://docs.python.org/2.0/ref/strings.html
# https://docs.python.org/2/library/stringio.html
# https://docs.python.org/3/library/io.html
# https://pandas.pydata.org/pandas-docs/stable/text.html
# http://ogrisel.github.io/scikit-learn.org/sklearn-tutorial/tutorial/text_analytics/working_with_text_data.html


print('*******************************************************************************')
print('* CARD GROUP 2 - Channel Description                                          *')
print('*******************************************************************************')
# -----------------------------------------------------------------------------------------------------------
# print out card 2.1
if debugg==1: print('* Card 2.1');
card_group02 = card_group02 + '* Card 2.1' + '\n'
if debugg==1: print('* NCHA NDM2 NDM3 NDM4 NDM5 NDM6 NDM7 NDM8 NDM9 NM10 NM11 NM12 NM13 NM14');
card_group02 = card_group02 + '* NCHA NDM2 NDM3 NDM4 NDM5 NDM6 NDM7 NDM8 NDM9 NM10 NM11 NM12 NM13 NM14' + '\n'
x = '{:5n}'.format(S_total)
x = x + '  0    0    0    0    0    0    0    0    0    0    0    0    0 '
if debugg==1: print(x);
card_group02 = card_group02 + x +'\n'

# -----------------------------------------------------------------------------------------------------------
# print out card 2.2
# python format strings
# https://docs.python.org/3/library/string.html#formatstrings
if debugg==1: print('* Card 2.2');
card_group02 = card_group02 + '* Card 2.2' + '\n'
if debugg==1: print('*      I       AREA        PWET ABOT ATOP NMGP    X         Y         XSIZ       YSIZ');
card_group02 = card_group02 + '*      I       AREA        PWET ABOT ATOP NMGP    X         Y         XSIZ       YSIZ' + '\n'
for ch in S_list:
    if debugg == 1: print(ch.printCTFchannel());
    card_group02 = card_group02 + ch.printCTFchannel() + '\n'

# -----------------------------------------------------------------------------------------------------------
# calculate total number of gaps
# i.e. number of connections between subchannels
Gap_total=0
unif=[]
for ch in S_list:
    x=ch.getChannelNeighbors()
    myC=ch.getChannelNumber()
    lc = x[0]
    # distringush between horizontal and vertical gaps
    if lc!=0:
        if myC<lc:
            y = str(myC) + 'to' + str(lc)
        else:
            y = str(lc) + 'to' + str(myC)
        unif.append(y)
    lc=x[1]
    if lc!=0:
        if myC<lc:
            y = str(myC) + 'to' + str(lc)
        else:
            y = str(lc) + 'to' + str(myC)
        unif.append(y)
    lc=x[2]
    if lc!=0:
        if myC<lc:
            y = str(myC) + 'to' + str(lc)
        else:
            y = str(lc) + 'to' + str(myC)
        unif.append(y)
    lc=x[3]
    if lc!=0:
        if myC<lc:
            y = str(myC) + 'to' + str(lc)
        else:
            y = str(lc) + 'to' + str(myC)
        unif.append(y)

unif=set(unif)
#x=np.array(unif)
#y=np.extract(x!=0,x)
Gap_total +=len(unif)


# https://stackoverflow.com/questions/17140886/how-to-search-and-replace-text-in-a-file-using-python
fl = open(filein,'r')
filedata = fl.read()
fl.close()

fileupdate = filedata.replace('CARD_GROUP_02',card_group02)
#card_group02 = card_group02 + '' + '\n'

print('*******************************************************************************')
print('* CARD GROUP 3 - Transverse Channel Connection (Gap) Data                     *')
print('*******************************************************************************')
# -----------------------------------------------------------------------------------------------------------
# print out card 3.1
if debugg==1: print('* Card 3.1');
card_group03 = card_group03 + '* Card 3.1' + '\n'
if debugg==1: print('*    NK NDM2 NDM3 NDM4 NDM5 NDM6 NDM7 NDM8 NDM9 NM10 NM11 NM12 NM13 NM14');
card_group03 = card_group03 + '*    NK NDM2 NDM3 NDM4 NDM5 NDM6 NDM7 NDM8 NDM9 NM10 NM11 NM12 NM13 NM14' + '\n'
x = '  {:5n}'.format(Gap_total)
x = x + '  0    0    0    0    0    0    0    0    0    0    0    0    0 '
if debugg==1: print(x);
card_group03 = card_group03 + x + '\n'
# -----------------------------------------------------------------------------------------------------------
# print out card 3.2 and 3.3
if debugg==1: print('* Card 3.2');
card_group03 = card_group03 + '* Card 3.2' + '\n'
if debugg==1: print('*     K     IK    JK   GAPN        LNGTH       WKR          FWL     IGB IGA FACT IG JG IG JG IG JG');
card_group03 = card_group03 + '*     K     IK    JK   GAPN        LNGTH       WKR          FWL     IGB IGA FACT IG JG IG JG IG JG' + '\n'
if debugg==1: print('* Card 3.3');
card_group03 = card_group03 + '* Card 3.3' + '\n'
if debugg==1: print('*     GMLT  ETNR');
card_group03 = card_group03 + '*     GMLT  ETNR' + '\n'

unif=[]
sum=1
for ch in S_list:
    x=ch.getChannelNeighbors()
    myC=ch.getChannelNumber()
    for idx,lc in enumerate(x):
        if lc!=0:
            if myC<lc:
                y = str(myC) + 'to' + str(lc)
                unif.append(y)
                gapNom=r_p - 2.0*r_r
                # check if guide tube is anywhere
                # same type of guide tubes anywhere assumed
                rt = ch.getRodTypeNeighbors()
                if idx==0 and rt[0]!=rt[2]:
                    gapNom = r_p - r_r - r_g
                if idx==1 and rt[0]!=rt[1]:
                    gapNom = r_p - r_r - r_g
                if idx==2 and rt[1]!=rt[3]:
                    gapNom = r_p - r_r - r_g
                if idx==3 and rt[2]!=rt[3]:
                    gapNom = r_p - r_r - r_g
                x='  {:5n}'.format(sum)+'  {:5n}'.format(myC)+'  {:5n}'.format(lc)+'  {:10.8f}'.format(gapNom*0.01)
                # check if edge or corner location
                gapDist=r_p
                gt=ch.getFANumberNeighbors()
                # vertical gap -----------------------------------------------
                if idx==0 and gt[0]!=gt[1] and gt[2]!=gt[3] and gt[0]==gt[2]:
                    gapDist = r_p + r_f - N_r*r_p
                # horizontal gap ---------------------------------------------
                if idx==1 and gt[0]!=gt[2] and gt[1]!=gt[3] and gt[0]==gt[1]:
                    gapDist = r_p + r_f - N_r*r_p
                # corner gap -------------------------------------------------
                if idx==2 and gt[0]!=gt[1] and gt[1]!=gt[3] and gt[2]!=gt[3]:
                    gapDist = r_p + r_f - N_r*r_p
                x=x + '  {:10.8f}'.format(gapDist*0.01)
                WKR=0.5
                FWALL=0.0
                IGAPA=0
                FACTOR=1.0
                x = x + '  {:10.8f}'.format(WKR) + '  {:5.2f}'.format(FWALL) + '  {:3n}'.format(IGAPA)
                x = x + '  {:3n}'.format(IGAPA) + '  {:3n}'.format(FACTOR)
                x = x + ' 0  0  0  0  0  0 '
                if debugg == 1: print(x);
                card_group03 = card_group03 + x + '\n'
                x = '      1   0.0'
                if debugg == 1: print(x);
                card_group03 = card_group03 + x + '\n'
                sum += 1


# -----------------------------------------------------------------------------------------------------------
# print out card 3.3.5
if debugg==1: print('* Card 3.3.5');
card_group03 = card_group03 + '* Card 3.3.5' + '\n'
if debugg==1: print('*    K       X          Y      NORM');
card_group03 = card_group03 + '*    K       X          Y      NORM' + '\n'

sum=1
for ch in S_list:
    x=ch.getChannelNeighbors()
    myC=ch.getChannelNumber()
    nrX=ch.getChannelX()
    nrY=ch.getChannelY()
    for idx,lc in enumerate(x):
        if lc!=0:
            if myC<lc:
                # here additonal gaps (due to corners, edges) are neglected
                x = '  {:5n}'.format(sum) + '  {:10.8f}'.format((nrX*r_p+0.5*r_p)*0.01)
                x = x + '  {:10.8f}'.format((nrY*r_p+0.5*r_p)*0.01)
                if idx==0 or idx==2:
                    x = x + ' x'
                else:
                    x = x + ' y'
                    if debugg == 1: print(x);
                card_group03 = card_group03 + x + '\n'
                sum += 1

fileupdate = fileupdate.replace('CARD_GROUP_03',card_group03)

# -----------------------------------------------------------------------------------------------------------
''
print('*******************************************************************************')
print('* CARD GROUP 4 - Vertical Channel Connection Data                             *')
print('*******************************************************************************')
# -----------------------------------------------------------------------------------------------------------
# print out card 4.2
if debugg==1: print('* Card 4.2');
card_group04 = card_group04 + '* Card 4.2' + '\n'
if debugg==1: print('* ISEC   NCHN  NONO     DXS     IVAR');
card_group04 = card_group04 + '* ISEC   NCHN  NONO     DXS     IVAR' + '\n'
x = '     1   ' + '{:7n}'.format(S_total)
x = x +'  35    0.126124   12'
if debugg==1: print(x);
card_group04 = card_group04 + x + '\n'
# -----------------------------------------------------------------------------------------------------------
# print out card 4.3
if debugg==1: print('* Card 4.3');
card_group04 = card_group04 + '* Card 4.3' + '\n'
if debugg==1: print('* JLEV     VARDX   JLEV     VARDX   JLEV     VARDX   JLEV     VARDX   JLEV     VARDX');
card_group04 = card_group04 + '* JLEV     VARDX   JLEV     VARDX   JLEV     VARDX   JLEV     VARDX   JLEV     VARDX' + '\n'
if debugg==1: print('    2    0.4874805   3    0.0609351   4    0.1219177  13    0.1218701  14    0.1219177');
card_group04 = card_group04 + '    2    0.4874805   3    0.0609351   4    0.1219177  13    0.1218701  14    0.1219177' + '\n'
if debugg==1: print('   22    0.1218701  23    0.1219177  32    0.1218701  33    0.1219177  34    0.1218701');
card_group04 = card_group04 + '   22    0.1218701  23    0.1219177  32    0.1218701  33    0.1219177  34    0.1218701' + '\n'
if debugg==1: print('   35    0.0609351  36    0.3656104 ');
card_group04 = card_group04 + '   35    0.0609351  36    0.3656104 ' + '\n'
# -----------------------------------------------------------------------------------------------------------
# print out card 4.4
if debugg==1: print('* Card 4.4');
card_group04 = card_group04 + '* Card 4.4' + '\n'
if debugg==1: print('*     I   KCHA  KCHA  KCHA  KCHA  KCHA  KCHA   KCHB  KCHB  KCHB  KCHB  KCHB  KCHB');
card_group04 = card_group04 + '*     I   KCHA  KCHA  KCHA  KCHA  KCHA  KCHA   KCHB  KCHB  KCHB  KCHB  KCHB  KCHB' + '\n'
for ch in S_list:
    myC=ch.getChannelNumber()
    x = '  {:5n}'.format(myC)+'  {:5n}'.format(myC)+'  0     0     0     0     0'
    x = x + '  {:5n}'.format(myC)+'  0     0     0     0     0'
    if debugg == 1: print(x);
    card_group04 = card_group04 + x + '\n'
# -----------------------------------------------------------------------------------------------------------
# print out card 4.5
if debugg==1: print('* Card 4.5');
card_group04 = card_group04 + '* Card 4.5' + '\n'
if debugg==1: print('* IWDE');
card_group04 = card_group04 + '* IWDE' + '\n'
x = '  {:5n}'.format(S_total)
if debugg==1: print(x);
card_group04 = card_group04 + x + '\n'
# -----------------------------------------------------------------------------------------------------------
# print out card 4.6
if debugg==1: print('* Card 4.6');
card_group04 = card_group04 + '* Card 4.6' + '\n'
if debugg==1: print('* MSIM  35*S_total');
card_group04 = card_group04 + '* MSIM  35*S_total' + '\n'
x = '  {:7n}'.format(35*S_total);
if debugg==1: print(x);
card_group04 = card_group04 + x + '\n'

fileupdate = fileupdate.replace('CARD_GROUP_04',card_group04)
# -----------------------------------------------------------------------------------------------------------
# print out card 7
# it is assumed that we have 11 grids: 7 grids in the active zone, 2 in the plenum zones and
# 2 pseudo-grids to model fuel assembly bottom and top nozzle
print('*******************************************************************************')
print('* CARD GROUP 7 - Grid Loss Coefficient Data                                   *')
print('*******************************************************************************')
if debugg==1: print('* Card 7.1  S_total/12 * 11 = xxx lines');
card_group07 = card_group07 + '* Card 7.1  S_total/12 * 11 = xxx lines' + '\n'
if debugg==1: print('*    NCD    NGT  IFGQF  IFSDRP  IFESPV  IFTPE  IGTEMP  NFBS  NDUM9-14');
card_group07 = card_group07 + '*    NCD    NGT  IFGQF  IFSDRP  IFESPV  IFTPE  IGTEMP  NFBS  NDUM9-14' + '\n'

cas = S_total/12
if int(cas)*12<S_total:
    cas=int(cas)+1
else:
    cas=int(cas)

# but we want to apply the pressure loss coefficients only for the subchannels inside
# of a fuel assembly, not at gaps and corners
# therefore we now create an array containing only all the relevant subchannels
unif=[]
sum=1
for ch in S_list:
    myC=ch.getChannelNumber()
    x = ch.getNumberOfNeighborFuel()
    if x==1:
        unif.append(myC)

ns=len(unif)
# print('*** ', ns)
cas = ns/12
if int(cas)*12<ns:
    cas=int(cas)+1
else:
    cas=int(cas)


x = '  {:7n}'.format(cas*11)
x = x + '   0      0       0       0      0       0     0  0 0 0 0 0 0'
if debugg==1: print(x);
card_group07 = card_group07 + x + '\n'
if debugg==1: print('* Card 7.2');
card_group07 = card_group07 + '* Card 7.2' + '\n'
if debugg==1: print('** CDL   J  Subchannels, enter up to 12');
card_group07 = card_group07 + '** CDL   J  Subchannels, enter up to 12' + '\n'
if debugg==1: print('** CDL calculated from NESTOR MVG obtained Re-dependent k correlation.');
card_group07 = card_group07 + '** CDL calculated from NESTOR MVG obtained Re-dependent k correlation.' + '\n'
if debugg==1: print('** Assuming Re=500,000');
card_group07 = card_group07 + '** Assuming Re=500,000' + '\n'


grids=['* Grid 1', '* Grid 2', '* Grid 3', '* Grid 4', '* Grid 5', '* Grid 6', '* Grid 7', '* Grid 8', '* Grid 9', '* Grid 10', '* Grid 11']
cdli=['1.6100', '0.6200', '1.0800', '1.0800', '1.0800', '1.0800', '1.0800', '1.0800', '1.0800', '0.8600', '2.6290']
cdlj=['1',      '2',      '4',      '8',      '13',     '17',     '22',     '26',     '30',     '34',     '35']

for idx,gr in enumerate(grids):
    if debugg == 1: print(gr);
    card_group07 = card_group07 + gr + '\n'
    x = cdli[idx] + '  ' + cdlj[idx]
    sum=1
    y=''
    for i in range(len(unif)):
        y = y + '  {:4n}'.format(unif[i])
        if i==len(unif)-1 and sum!=12:
            for j in range(12-sum):
                y = y + '  {:4n}'.format(0)
                sum += 1
        if sum==12:
            if debugg == 1: print(x+y);
            card_group07 = card_group07 + x+y + '\n'
            y=''
            sum=1
        else:
            sum +=1

fileupdate = fileupdate.replace('CARD_GROUP_07',card_group07)
# -----------------------------------------------------------------------------------------------------------
# print out card 8
print('*******************************************************************************')
print('* CARD GROUP 8 - Rod and Unheated Conductor Data                              *')
print('*******************************************************************************')

if debugg == 1: print('* Card 8.1');
card_group08 = card_group08 + '* Card 8.1' + '\n'
if debugg == 1: print('*  NRRD    NSRD   NC NRTB NRAD NLTY NSTA  NXF NCAN RADF   W3 NM12 NM13 NM14');
card_group08 = card_group08 + '*  NRRD    NSRD   NC NRTB NRAD NLTY NSTA  NXF NCAN RADF   W3 NM12 NM13 NM14' + '\n'
x = '  {:7n}'.format(N_total)
x = x + '     0    1    1    0    0    1    1    0    0    0    0    0    0'
if debugg == 1: print(x);
card_group08 = card_group08 + x + '\n'
if debugg == 1: print('* Card 8.2');
card_group08 = card_group08 + '* Card 8.2' + '\n'
if debugg == 1: print('*    N    IFTY     IAXP NRND      DAXMIN   RMULT    HGAP ISECR   HTAMB    TAMB');
card_group08 = card_group08 + '*    N    IFTY     IAXP NRND      DAXMIN   RMULT    HGAP ISECR   HTAMB    TAMB' + '\n'
if debugg == 1: print('* Card 8.3');
card_group08 = card_group08 + '* Card 8.3' + '\n'
if debugg == 1: print('* NSCH  PIE  NSCH  PIE  NSCH  PIE  NSCH  PIE  NSCH   PIE  NSCH   PIE  NSCH   PIE  NSCH   PIE');
card_group08 = card_group08 + '* NSCH  PIE  NSCH  PIE  NSCH  PIE  NSCH  PIE  NSCH   PIE  NSCH   PIE  NSCH   PIE  NSCH   PIE' + '\n'
#
# we assume two geometry type here: one for standard fuel rod (1), the other for guide tube (2)
#
rX, rY = rodK.shape
for j in range(rY):
    for i in range(rX):
        rodNum=rodK[j,i]
        x = '  {:7n}'.format(rodNum)
        rodTyp = rodH[j, i]
        # add rod geometry type
        if rodTyp==1:
            x = x + '  {:2n}'.format(1)
        if rodTyp==0:
            x = x + '  {:2n}'.format(2)
        # add power profile id
        x = x + '  {:7n}'.format(rodNum)
        x = x + '  0       0.00000   1.000   5678.3     1   0.000   0.000'
        if debugg == 1: print(x);
        card_group08 = card_group08 + x + '\n'
        # find all subchannels connected to this rod
        unil=[]
        for ch in S_list:
            myC = ch.getChannelNumber()
            lyL = ch.getRodNeighbors()
            if rodNum in lyL:
                unil.append(myC)
        x=''
        for k in range(len(unil)):
            x = x + '  {:7n}'.format(unil[k])+ ' 0.25 '
        for k in range(8 - len(unil)):
            x = x + '  {:2n}'.format(0) + ' 0.00 '
        if debugg == 1: print(x);
        card_group08 = card_group08 + x + '\n'

# -----------------------------------------------------------------------------------------------------------
# print out card 8.6
if debugg == 1: print('* Card 8.6');
card_group08 = card_group08 + '* Card 8.6' + '\n'
if debugg == 1: print('*   I          NRT1 NST1 NRX1');
card_group08 = card_group08 + '*   I          NRT1 NST1 NRX1' + '\n'
x = '    1    '
x = x + '  {:7n}'.format(N_total)
x = x + ' 0    2'
if debugg == 1: print(x);
card_group08 = card_group08 + x + '\n'
# all rods use the same initialisation table
if debugg == 1: print('* Card 8.7');
card_group08 = card_group08 + '* Card 8.7' + '\n'
if debugg == 1: print('*  IRTB');
card_group08 = card_group08 + '*  IRTB' + '\n'

x = ''
sum=1
rX, rY = rodK.shape
for j in range(rY):
    for i in range(rX):
        rodNum=rodK[j,i]
        x = x + '  {:7n}'.format(rodNum)
        if sum==12:
            if debugg == 1: print(x);
            card_group08 = card_group08 + x + '\n'
            x=''
            sum=1
        else:
            sum = sum + 1
        if j==rX-1 and i==rX-1 and len(x)>0:
            if debugg == 1: print(x);
            card_group08 = card_group08 + x + '\n'

# -----------------------------------------------------------------------------------------------------------
# print out card 8.9
# simple temperature table
if debugg == 1: print('* Card 8.9');
card_group08 = card_group08 + '* Card 8.9' + '\n'
if debugg == 1: print('*     AXIALT      TRINIT');
card_group08 = card_group08 + '*     AXIALT      TRINIT' + '\n'
if debugg == 1: print('      0.0000      292.78');
card_group08 = card_group08 + '      0.0000      292.78' + '\n'
if debugg == 1: print('      4.7500      292.78');
card_group08 = card_group08 + '      4.7500      292.78' + '\n'

fileupdate = fileupdate.replace('CARD_GROUP_08',card_group08)
# -----------------------------------------------------------------------------------------------------------
# print out card 11
#
print('*******************************************************************************')
print('* CARD GROUP 11 - Axial Power Tables and Forcing Functions                    *')
print('*******************************************************************************')

if debugg == 1: print('* Card 11.1');
card_group11 = card_group11 + '* Card 11.1' + '\n'
if debugg == 1: print('* NQA      NAXP MNXN  NQ  NGPF NQR  NDM7 NDM8 NDM9 NM10 NM11 NM12 NM13 NM14');
card_group11 = card_group11 + '* NQA      NAXP MNXN  NQ  NGPF NQR  NDM7 NDM8 NDM9 NM10 NM11 NM12 NM13 NM14' + '\n'
x = '    1 '
x = x + '  {:7n}'.format(N_total)
x = x + ' 36    0    0    1    0    0    0    0    0    0    0    0'
if debugg == 1: print(x);
card_group11 = card_group11 + x + '\n'
if debugg == 1: print('*');
card_group11 = card_group11 + '*' + '\n'
if debugg == 1: print('* Axial Power Forcing Functions');
card_group11 = card_group11 + '* Axial Power Forcing Functions' + '\n'

if debugg == 1: print('* Card 11.2 + 11.3 *****************');
card_group11 = card_group11 + '* Card 11.2 + 11.3 *****************' + '\n'
if debugg == 1: print('*     YQA');
card_group11 = card_group11 + '*     YQA' + '\n'
if debugg == 1: print('      0.0');
card_group11 = card_group11 + '      0.0' + '\n'
if debugg == 1: print('*  I NAXN');
card_group11 = card_group11 + '*  I NAXN' + '\n'
# -----------------------------------------------------------------------------------------------------------
# print out card 11 axial profile
#
# for the time being we use a flat axial power profile for all rods
#
power=[0.0   ,  0.0  , 1.0   , 1.0   , 1.0   , 1.0   , 1.0   , 1.0   , 1.0   , 1.0   , 1.0   , 1.0   , 1.0   , 1.0   , 1.0   , 1.0   , 1.0   , 1.0   , 1.0   , 1.0   , 1.0   , 1.0   , 1.0   , 1.0   , 1.0   , 1.0   , 1.0   , 1.0   , 1.0   , 1.0   , 1.0   , 1.0   , 1.0   , 1.0   , 0.0   , 0.0    ]
pnode=[0.0000, 0.4872, 0.5481, 0.6699, 0.7917, 0.9135, 1.0353, 1.1571, 1.2788, 1.4006, 1.5224, 1.6442, 1.7660, 1.8878, 2.0096, 2.1314, 2.2532, 2.3750, 2.4968, 2.6186, 2.7404, 2.8622, 2.9840, 3.1058, 3.2276, 3.3494, 3.4712, 3.5929, 3.7147, 3.8365, 3.9583, 4.0801, 4.2019, 4.3237, 4.3846, 4.7540 ]

rX, rY = rodK.shape
for j in range(rY):
    for i in range(rX):
        rodNum=rodK[j,i]
        x = '* Card 11.3 : rod {:7n}'.format(rodNum)
        if debugg == 1: print(x);
        card_group11 = card_group11 + x + '\n'
        x = '*  I NAXN'
        if debugg == 1: print(x);
        card_group11 = card_group11 + x + '\n'
        x = '    {:7n} 36'.format(rodNum)
        if debugg == 1: print(x);
        card_group11 = card_group11 + x + '\n'
        x = '* Card 11.4 : rod {:7n}'.format(rodNum)
        if debugg == 1: print(x);
        card_group11 = card_group11 + x + '\n'
        x = '*   Y     AXIAL'
        if debugg == 1: print(x);
        card_group11 = card_group11 + x + '\n'
        for idx, height in enumerate(pnode):
            x = '  {:5.4f}'.format(height)
            x = x + '  {:5.4f}'.format(power[idx])
            if debugg == 1: print(x);
            card_group11 = card_group11 + x + '\n'

# -----------------------------------------------------------------------------------------------------------
# print out card 11 radial power fractions
#
# for the time being we use a flat radial power profile for all rods
# we set this profile equal to the matrix "rodH"
#
if debugg == 1: print('* Radial Power Forcing Functions');
card_group11 = card_group11 + '* Radial Power Forcing Functions' + '\n'
if debugg == 1: print('* Card 11.7');
card_group11 = card_group11 + '* Card 11.7' + '\n'
if debugg == 1: print('*        YQR');
card_group11 = card_group11 + '*        YQR' + '\n'
if debugg == 1: print('         0.0');
card_group11 = card_group11 + '         0.0' + '\n'
if debugg == 1: print('* Card 11.8');
card_group11 = card_group11 + '* Card 11.8' + '\n'
if debugg == 1: print('*        FQR');
card_group11 = card_group11 + '*        FQR' + '\n'

rX, rY = rodK.shape
x=''
sum=1
for j in range(rY):
    for i in range(rX):
        rodNum=rodK[j,i]
        power=rodH[j,i]
        x = x + '  {:7.5f}'.format(power)
        if sum == 12:
            if debugg == 1: print(x);
            card_group11 = card_group11 + x + '\n'
            x = ''
            sum = 1
        else:
            sum = sum + 1
        if j == rX - 1 and i == rX - 1 and len(x)>0:
            if debugg == 1: print(x);
            card_group11 = card_group11 + x + '\n'

fileupdate = fileupdate.replace('CARD_GROUP_11',card_group11)
# -----------------------------------------------------------------------------------------------------------
# print out card 13 radial power fractions
#
print('*******************************************************************************')
print('* CARD GROUP 13 - Boundary Conditions Data                                    *')
print('*******************************************************************************')


if debugg == 1: print('* Card 13.1');
card_group13 = card_group13 + '* Card 13.1' + '\n'
if debugg == 1: print('*   NBND NKBD NFUN NGBD NDM5 NDM6 NDM7 NDM8 NDM9 NM10 NM11 NM12 NM13 NM14');
card_group13 = card_group13 + '*   NBND NKBD NFUN NGBD NDM5 NDM6 NDM7 NDM8 NDM9 NM10 NM11 NM12 NM13 NM14' + '\n'
x = '  {:7n} '.format(S_total*2)
x = x + '0    0    0    0    0    0    0    0    0    0    0    0    0'
if debugg == 1: print(x);
card_group13 = card_group13 + x + '\n'
if debugg == 1: print('* Card 13.4');
card_group13 = card_group13 + '* Card 13.4' + '\n'
if debugg == 1: print('* Inlet b.c. -----------------------------------------------------------');
card_group13 = card_group13 + '* Inlet b.c. -----------------------------------------------------------' + '\n'
if debugg == 1: print('* note: mass flow rate set to 0 here since gtot was specified up top.');
card_group13 = card_group13 + '* note: mass flow rate set to 0 here since gtot was specified up top.' + '\n'
if debugg == 1: print('*  IBD1 IBD2 ISPC N1FN N2FN N3FN   BCVALUE1     BCVALUE2   BCVALUE3  INITGAS');
card_group13 = card_group13 + '*  IBD1 IBD2 ISPC N1FN N2FN N3FN   BCVALUE1     BCVALUE2   BCVALUE3  INITGAS' + '\n'

flowrate=0.0
chantemp=-293.6

for ch in S_list:
    myC=ch.getChannelNumber()
    x = ' {:7n}  1   2   0    0    0  '.format(myC)
    x = x + '    {:7.5f}     {:7.5f} 0.0       1'.format(flowrate,chantemp)
    if debugg == 1: print(x);
    card_group13 = card_group13 + x + '\n'

if debugg == 1: print('* Outlet b.c. ------------------------------------------------------------');
card_group13 = card_group13 + '* Outlet b.c. ------------------------------------------------------------' + '\n'
if debugg == 1: print('*  IBD1 IBD2 ISPC N1FN N2FN N3FN   BCVALUE1     BCVALUE2   BCVALUE3  INITGAS');
card_group13 = card_group13 + '*  IBD1 IBD2 ISPC N1FN N2FN N3FN   BCVALUE1     BCVALUE2   BCVALUE3  INITGAS' + '\n'

flowrate=0.0
chanpres=158.0

for ch in S_list:
    myC=ch.getChannelNumber()
    x = ' {:7n} 37   1   0    0    0  '.format(myC)
    x = x + '    {:7.5f}     {:7.5f}  {:7.5f}       1'.format(0.0,chantemp, chanpres)
    if debugg == 1: print(x);
    card_group13 = card_group13 + x + '\n'

fileupdate = fileupdate.replace('CARD_GROUP_13',card_group13)
# -----------------------------------------------------------------------------------------------------------
# write input file
#
fl = open(fileout,'w')
fl.write(fileupdate)
fl.close()

with h5py.File(fileh5, 'w') as hf:
    hf.create_dataset("channel_IDs",  data=rodS)
    hf.create_dataset("rod_IDs",      data=rodK)
    hf.create_dataset("rod_types",    data=rodH)
    hf.create_dataset("rod_FA_ID",    data=rodU)

