#!/usr/bin/env python

__author__ = "Jeremy Malloch"
__status__ = "Prototype"

import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import seaborn as sns
from time import gmtime, strftime
import csv
import string

#Kinda obvious who wrote the program based on the style haha
plt.style.use('seaborn-colorblind')

#Take in from command line the refresh rate of data coming in so it will
#be used to match the refresh rate of the animation (in milliseconds)
#Take in from command line the length of time of the window to view in milliseconds
try:
    refreshRate, frameLength = int(sys.argv[1]), int(sys.argv[2])
except ValueError:
    print("Refresh rate or frame length is not a valid number")

#Global variable for the number of samples that will be displayed at any time
numSamples = frameLength/refreshRate

#Global variable for the number of data channels coming (number of plots is 
#double this, since there is the filtered and unfiltered output)
inChannels = 2

#Initialize the x-axis by using the refresh rate and window view length
xAxis = [-1.0*refreshRate*x for x in range(numSamples)]

class Current_Data(object):
	"""Holds the most recent data that is currently displayed"""

	def __init__(self, numSamples_, inChannels_):
		Columns = [('UnFilt_'+str(x)) for x in range(1,inChannels_+1)]
		for x in range(1,inChannels_+1):
			Columns.append('Filt_+str(x)')
		self.numSamples = numSamples_
		self.inChannels = inChannels_
		self.df = pd.DataFrame(np.zeros((numSamples_, inChannels_*2)), columns=Columns)
		#Log the results in a CSV file with current day and time as file name
		self.fileName = strftime("%Y-%m-%d %H:%M:%S", gmtime())
		self.df.to_csv(self.fileName)
		with open('foo.csv', 'a') as self.f:
             self.writer = csv.writer(f)

	def update(self, newRow):
		self.writer.writerows(newRow)
		self.df.index = df.index + 1
		self.df.loc[0] = newRow
		self.df.drop(index[-1])

	def unFiltData(self, channel_number):
		'''
		Method that returns a list of the unfiltered data corresponding to
		the channel number passed as a parameter
		'''
		return self.df[('UnFilt_'+str(channel_number))]

	def FiltData(self, channel_number):
		'''
		Method that returns a list of the filtered data corresponding to
		the channel number passed as a parameter
		'''
		return self.df[('Filt_'+str(channel_number))]

#Initilize lists of the subplots that
unFilteredPlots = []
FilteredPlots = []

#Initialize Current_Data Object
Data = Current_Data(numSamples, inChannels)

#Initializing the plot
fig = plt.figure()

#Initialize all the subplots
for channels in range(inChannels):
	#Set up the unfiltered plot for an in channel
    unFiltTemp = fig.add_subplot(inChannels,2,1 + 2*channels)
    unFiltTemp.plot(xAxis, Data.unFiltData(channels))
    unFilteredPlots.append(unFiltTemp)
    #Set up the filtered plot for an in channel
    FiltTemp = plt.figure(inChannels,2,(2*channels+1))
    FiltTemp.plot(xAxis, Data.FiltData(channels))
    FilteredPlots.append(FiltTemp)



class Window(object):
	'''
	Class that generates the figure to plot
	'''
    def __init__(self, fig_):
    	self.fig = fig_
    	self.xAxis = [-1.0*refreshRate*x for x in range(numSamples)]
    	self.unFilteredPlots = [(self.fig.add_subplot(inChannels,2,1 + 2*channels)) for channels in range(inChannels)]
    	self.FilteredPlots = [(self.fig.add_subplot(inChannels,2,1 + 2*channels+1)) for channels in range(inChannels)]
    	#Add label of each column (Unfiltered vs filtered)
    	self.unFilteredPlots[0].set_title('Unfiltered Data')
		self.FilteredPlots[0].set_title('Filtered Data')

    def __call__(self, i):
        # This way the plot can continuously run and we just keep
        # watching new realizations of the process
        if i == 0:
            return self.init()
        for subplot in self.unFilteredPlots:
        	unFiltTemp.plot(self.xAxis, Data.unFiltData(channels))
        for subplot in self.FilteredPlots:
        	FiltTemp.plot(self.xAxis, Data.FiltData(channels))

        return self.fig

#Label the x-axis 
plt.xlabel('time (ms)')

frame1 = animation.TimedAnimation(fig, interval=refreshRate)
plt.show()