import matplotlib
from matplotlib import pyplot as plt

matplotlib.use("Qt5Agg")

plt.style.use(['ggplot'])

# Backend door for matplotlib importation required to use Pyqt with matpltlib libray
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationBar
from matplotlib.figure import Figure
from matplotlib import rcParams

import numpy as np



class FigureAssembly(object):
    """
        Purpose: create the base figure for data to be plotted on.
        1. Inheritance/initalization
        2. defining figure and axes
        3. Plotting method
    """

    ### 1).Inheritance/initialization ###
    def __init__(self):
        super(FigureAssembly, self).__init__()

        # 2). Figure/axes defined
        self.figure = plt.figure()  # creates a blank figure to plot data on
        """
        'self.figure.add_subplot(111)'
        defines the number and position of subplots first two numbers are total number of plots on grid.
        For example 2x2 indicates total of 4 plots. Last number indicates the acutal plot number. For example 223 means
        there are four plots and we are looking at the third plot of the 4
        """
        self.axes = self.figure.add_subplot(111)

        # define axes headers
        self.axes.set_xlabel('x label')
        self.axes.set_ylabel('y label')

    # 3). Plotting Method
    """
        Purpose: differentiate which type of graph should be plotted depending on user input
        Takes arguments(List, List, str)
    """

    def plotData(self, xdata, ydata, PlotVal, show):
        # Debugging Statements
        print("plotting")
        #print("elements data type of list x is {}".format(type(xdata[1])))
        #print("elements data type of list y is {}".format(type(ydata[1])))
        #print("PlotVal data type is {}".format(type(PlotVal)))

        ###Superficial Touches###

        self.axes.grid()  # add a grid to plot

        # Plots boxplots
        if PlotVal == "box":
            print("inside PlotVal = box")
            self.x = xdata

            print("x data is here .......{}".format(self.x))

            print("data type of static x is {}".format(type(self.x[1])))
            # try:
            #     print("data type of static x is {}".format(type(self.x[1])))
            # except:
            #     self.Debugger.PrintException()

            self.axes.boxplot(self.x)
            self.axes.grid()
        # Plots ScatterPlots
        elif PlotVal == "scatter":

            self.x = xdata
            self.y = ydata
            print("about to assign n")

            n = len(self.y)
            print(n)
            print(self.x)
            print(self.y)

            # Creates 1 to n many points along our x-axis for each piece of data we will plot
            self.NumTicks = np.arange(n)
            print(self.NumTicks)

            # sets ticks 1-n as x-axis
            self.axes.set_xticks(self.NumTicks)
            print("ticks have been created ")

            # sets our table headers as the x-axis labels for our datapoints, and rotates to look better
            self.axes.set_xticklabels(self.y, rotation=60)
            print("strings have been set as labels")

            # creates scatter plot
            self.axes.scatter(self.NumTicks, self.x)
            self.axes.grid()
            # self.axes.plt.tight_layout()

        if show == True:
            plt.show()
        else:
            pass
        print("graph appears")