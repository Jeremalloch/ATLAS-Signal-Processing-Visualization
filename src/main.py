import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import seaborn as sns
from time import gmtime, strftime
import csv
import string
from collections import deque

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

# Hardcode the value of frameLength and refresh rate (where dataFrequency is the time interval between data samples)
dataInterval = 200
frameLength = 2000

# Animation rate is the frame rate for updating the animation.  Since we have ~6 plots, having too high an animation
# rate will be unpractical, so instead we'll use 24 fps if the dataFrequency rate is lower than 1/24 (the
if dataInterval < 1/24:
    displayInterval = 1/24
else:
    displayInterval = dataInterval

# Global variable for the number of samples that will be displayed at any time
numSamples = frameLength // dataInterval

# Global variable for the number of data channels coming (number of plots is
# double this, since there is the filtered and unfiltered output)
inChannels = 3

class Data_Container:
    """
    Holds the most recent data that is currently displayed
    """
    def __init__(self, inChannels_, frameLength_, dataInterval_):
        self.dataInterval = dataInterval_
        self.inChannels = inChannels_
        self.frameLength = frameLength_
        self.numSamples = self.frameLength // self.dataInterval
        self.unFilterData = [deque(np.zeros(self.numSamples), maxlen=self.numSamples) for x in range(inChannels)]
        self.FilteredData = [deque(np.zeros(self.numSamples), maxlen=self.numSamples) for x in range(inChannels)]
        Columns = [('UnFilt_' + str(x)) for x in range(1, inChannels + 1)]
        for x in range(1, inChannels + 1):
            Columns.append('Filt_' + str(x))
        # Initialize the CSV file using the columns as labels, then store the writer as an internal attribute
        # TODO look into putting the CSV file into the object
        # Log the results in a CSV file with current day and time as file name
        self.fileName = strftime("%Y-%m-%d %H:%M:%S", gmtime()) + '.csv'

    def pullData(self):
        """
        Pulls data from the Rpi.  Currently just uses numpy randomizer to generate random data
        :return: list of new data points
        """
        return np.random.rand(self.inChannels)

    def update(self):
        """
        Updates the Data_Container object with most recent data, deque objects automatically pop the oldest data
         off the back if the deque object grows longer than the frame
        """
        newData = self.pullData()
        self.writeToCSV(newData)
        for num, channel in enumerate(self.data):
            channel.appendleft(newData[num])

    def writeToCSV(self, newData):
        """
        Write the new row to a CSV file to keep track of the program performance
        newData: iterable of float
        """
        pass

    def getUnfilteredData(self, *args):
        """
        Returns a list of deque objects (basically dynamic arrays optimized for this application) to be sent through
        the filtering algorithm.  (Basically a 2D array is being returned)
        """
        if len(args) == 0:
            return self.unFilterData
        return self.unFilterData[int(args[0])]

    def getFiltereredData(self, *args):
        """
        Returns a list of deque objects to then be plotted (basically a 2D array)
        :return:
        """
        if len(args) == 0:
            return self.FilteredData
        return self.FilteredData[int(args[0])]

    def giveFilteredData(self, dataIterable):
        """
        Takes a row of filtered data in from the filtering algorithm (in an iterable form)
        """
        for num, point in enumerate(dataIterable):
           self.FilteredData[num].appendleft(point)

class Realtime_plot:
    """
    Creates a Data_Container object, then takes data from that and updates the animation plot
    """

    def __init__(self, plt, inChannels_, frameLength_, dataInterval_):
        self.data = Data_Container(inChannels_, frameLength_, dataInterval_)
        self.inChannels = inChannels_
        self.fig, self.PlotArray = plt.subplots(inChannels, 2, sharex='col', sharey='row', figsize = (12, 2 * inChannels))
        self.lineArray = []
        for x in range(self.inChannels):
            self.lineArray.append(self.PlotArray[x,0].plot(self.data.getUnfilteredData(x)))
            self.lineArray.append(self.PlotArray[x,1].plot(self.data.getUnfilteredData(x)))
        self.xAxis = [-1*dataInterval * x for x in range(numSamples)]
        self.PlotArray[0, 0].set_title('Filtered Data')    #Add a label above the column of filtered plots
        self.PlotArray[0, 1].set_title('Unfiltered Data')    #Add a label above the column of unfiltered plots
        self.fig.text(0.3, 0.04, 'Time (ms)', ha='center', va='center') #Set an x-axis label for the first column
        self.fig.text(0.725, 0.04, 'Time (ms)', ha='center', va='center') #Set an x-axis label for the first column

    def getPlot(self, Row, Column):
        """
        Returns the subplot located at the row and column referenced
        :param Row: int
        :param Column: int
        :return: matplotlib.axes._subplots.AxesSubplot object
        """
        return self.PlotArray[Row, Column]

    def getFig(self):
        """
        Returns the matplotlib figure object
        :return: matplotlib.figure.Figure
        """
        return self.fig

    def updatePlot(self):
        """
        Updates the plot upon new data being added to the current data
        data frame
        :return: matplotlib.figure.Figure
        """
        for num, row in enumerate(self.data.FilteredData):  # Update the unfiltered data plots
            self.lineArray[num][0].set_ydata(self.data.getUnfilteredData(num))
            self.lineArray[num + self.inChannels - 1][0].set_ydata(self.data.getFiltereredData(num))
        return self.lineArray

# Initialize the window object
display = Realtime_plot(plt, inChannels, frameLength, dataInterval)

fig = display.getFig()

# display.updatePlot()

frame = animation.FuncAnimation(fig, display.updatePlot(), interval=displayInterval, blit=True)
