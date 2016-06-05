#!/usr/bin/env python

__author__ = "Jeremy Malloch"
__status__ = "Prototype"

import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import seaborn as sns

#Kinda obvious who wrote the program based on the style haha
plt.style.use('seaborn-colorblind')

#Take in from command line the refresh rate of data coming in so it will
#be used to match the refresh rate of the animation (in milliseconds)
#Take in from command line the length of time of the window to view in milliseconds
try:
    refreshRate, frameLength = int(sys.argv[1]), int(sys.argv[2])
except ValueError:
    print("Refresh rate or framel length is not a valid number")

#Global variable for the number of samples that will be displayed at any time
numSamples = frameLength/refreshRate

#Global variable for the number of data channels coming (number of plots is 
#double this, since there is the filtered and unfiltered output)
inChannels = 2

#Initialize the Pandas Dataframe that will store all the data
#Currently has randomized data in it just to test functionality
df = pd.DataFrame(np.random.randn(10, 4))

#Initialize the x-axis by using the refresh rate and window view length
xAxis = np.linspace(0.0, 10000, num=(numSamples+1), endpoint=False)

#Initilize lists of the subplots that
unFilteredPlots = []
FilteredPlots = []

for channels in range(inChannels):
    unFilteredPlots.append(plt.figure())
    FilteredPlots.append(plt.figure())
    


#Label the x-axis 
plt.xlabel('time (ms)')

#frame1 = animation.TimedAnimation(fig, interval=200, repeat_delay=None, repeat=True, event_source=None, *args, **kwargs)
plt.show()