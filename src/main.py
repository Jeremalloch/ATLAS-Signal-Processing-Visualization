import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import seaborn as sns
from time import gmtime, strftime
import csv
import string

__author__ = "Jeremy Malloch"
__status__ = "Prototype"

# Open the CSV file
# with open(str(fileName), 'a') as f:
#     writer = csv.writer(f)

# Kinda obvious who wrote the program based on the style haha
plt.style.use('seaborn-colorblind')

# Take in from command line the refresh rate of data coming in so it will
# be used to match the refresh rate of the animation (in milliseconds)
# Take in from command line the length of time of the window to view in milliseconds
# try:
#    refreshRate, frameLength = int(sys.argv[1]), int(sys.argv[2])
# except ValueError:
#    print("Refresh rate or frame length is not a valid number")

# Hardcode the value of frameLength and refresh rate
refreshRate = 200
frameLength = 2000

# Global variable for the number of samples that will be displayed at any time
numSamples = frameLength // refreshRate

# Global variable for the number of data channels coming (number of plots is
# double this, since there is the filtered and unfiltered output)
inChannels = 3

# Initialize the x-axis by using the refresh rate and window view length
xAxis = [-1.0 * refreshRate * x for x in range(numSamples)]


class Realtime_plot:
	"""
    Holds the most recent data that is currently displayed
    """

	def __init__(self, plt):
		Columns = [('UnFilt_' + str(x)) for x in range(1, inChannels + 1)]
		for x in range(1, inChannels + 1):
			Columns.append('Filt_' + str(x))
		# TODO Initilize an empty dataframe so that a string of zeroes won't be written to the csv file
		# self.df = pd.DataFrame(np.zeros((numSamples, inChannels * 2)), columns=Columns)
		self.df = pd.DataFrame(np.random.rand(numSamples, (inChannels * 2)), columns=Columns)
		# TODO look into putting the CSV file into the object
		# Log the results in a CSV file with current day and time as file name
		# self.fileName = strftime("%Y-%m-%d %H:%M:%S", gmtime()) + '.csv'
		# TODO Look into sys.path() so that CSV file is saved in same location as program
		# self.df.to_csv(fileName)
		self.fig, self.PlotArray = plt.subplots(inChannels, 2, sharex='col', sharey='row') #Initialize the subplots
		self.xAxis = [-1.0 * refreshRate * x for x in range(numSamples + 1)]
		self.PlotArray[0, 0].set_title('Filtered Data')    #Add a label above the column of filtered plots
		self.PlotArray[0, 1].set_title('Unfiltered Data')    #Add a label above the column of unfiltered plots


	def update(self):
		"""
	    Update the dataframe object, removing the oldest row entry, and
		adding the newRow iterable to the top of the DataFrame
		"""
		# self.writer.writerows(newRow)
		self.df.loc[-1] = self.updateData()    # Adding the new row
		self.df.index = self.df.index + 1   # Shifting the row index up by one
		self.df.sort_index()  # Sorting the dataframe by index
		self.df.drop(self.df.index[10], inplace=True)   # Drop the oldest data from the dataframe
		self.plot_()    #Update the plot

	def updateData(self):
		"""
		Returns a list of updated data from the input
		:return: list of type float
		"""
		# As stopgap until raspberry pi data collection code is collected, random x values are generated
		return np.random.rand(inChannels)

	def getData(self, ):
		"""
		Returns a pandas series object for the y values for one plot
		:return: Pandas series of floats
		"""

	def getPlot(self, Row, Column):
		"""
		Returns the subplot located at the row and column referenced
		:param Row: int
		:param Column: int
		:return: matplotlib.axes._subplots.AxesSubplot object
		"""
		return self.PlotArray[Row, Column]

	def updatePlot(self):
		"""
		Updates the plot upon new data being added to the current data
		data frame
		:return: matplotlib.figure.Figure
		"""
		for num, subplot in enumerate(self.PlotArray):  #Update the unfiltered data plots
			self.PlotArray[0][num].plot(self.xAxis, self.unFiltData(num))
		for num, subplot in enumerate(self.PlotArray):  #Update the filtered data plots
			self.PlotArray[1][num].plot(self.xAxis, self.FiltData(channels))

		return self.fig


	def test(self):
		"""
		Test function that calls update rows, fills in rows with for
		loop to test function of update function
		"""
		for x in range(1, 15):
			self.update([x, x, x, x])
		return self.df

class Data_source:
	"""
	Abstractation of the input data, coming from a raspberry pi
	Currently just consists of a random number generator
	"""
	def __init__(self, input_channels_):
		self.input_channels = input_channels_

	def update(self):
		return np.random.rand(self.input_channels)


# Initializing the plot
fig = plt.figure(figsize = (12, 2 * inChannels))  #Vary the plotting window size based on number of input channels
ax = plt
# Initialize the window object
display = Realtime_plot(plt)
# Label the x-axis
plt.xlabel('time (ms)')

frame = animation.FuncAnimation(fig, Realtime_plot.update, fargs=(*dataSource.update), interval=refreshRate, blit=True)


plt.show() #display the plto