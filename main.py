#!/usr/bin/env python

__author__ = "Jeremy Malloch"
__copyright__ = "Copyleft 2016"
__credits__ = ["Jeremy Malloch"]
__license__ = "GPL"
__version__ = "3"
__maintainer__ = "Jeremy Malloch"
__email__ = "jmalloch@uwaterloo.ca"
__status__ = "Prototype"

import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

#Take in from command line the refresh rate of data coming in so it will
#be used to match the refresh rate of the animation (in milliseconds)
sys.argv[1] = refreshRate

#Take in from command line the length of time of the window to view in milliseconds
sys.argv[2] = frameLength

#Global variable for the number of samples that will be displayed at any time
numSamples = frameLength*refreshRate

#Global variable for the number of data channels coming (number of plots is 
#double this, since there is the filtered and unfiltered output)
inChannels = 2

#Initialize the Pandas Dataframe that will store all the data
df = pd.DataFrame(np.random.randn(10, 4))

#Initialize the x-axis by using the refresh rate and window view length
xAxis = np.linspace(0.0, num=(numSamples+1), endpoint=False)

#Initilize lists of the subplots that
unFilteredPlots = []
FilteredPlots = []

for channels in range(inChannels):
    unFilteredPlots.append(plt.figure())
    FilteredPlots.append(plt.figure())
    
unfiltered1 = fig.add_subplot(2,2,1)




frame1 = animation.TimedAnimation(fig, interval=200, repeat_delay=None, repeat=True, event_source=None, *args, **kwargs)
frame2 = animation.TimedAnimation(fig, interval=200, repeat_delay=None, repeat=True, event_source=None, *args, **kwargs)
