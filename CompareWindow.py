
# Importing PyQt5 library to construct widgets for Graphic User Interface (GUI) application
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
                             QWidget, QLabel,QMainWindow, QTableWidgetItem, QTableWidget, QMenu, QMessageBox)

from functools import partial
import shlex

from PyQt5.QtCore import Qt, pyqtSignal


class ComparisonUI(QMainWindow):
    """
        Creates the comparison window that will be opened when the user clicks the compare button.

        Purpose: Used to create plots using multiple trend reports from different imported spreadsheets
        The user will type in names of the data tables and their corresponding row numbers which they wish
        to plot from.
    """

    MultiBoxSignal = pyqtSignal(list, list, str)

    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setWindowTitle("Perspective - MultiGraph Window")

        # initialize Compare User Interface
        self.CompareUI()

    def CompareUI(self):
        print("initialize widgets")

        # Creates the mainwidget to hold/display all other widgets on
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        # Creating descriptor labels
        self.TableHeader = QLabel("Tables")
        self.RowHeader = QLabel("Row Selection")

        ###MUST FOLLOW FORMAT EXACTLY### Table name must be a string, no symbols
        # string is the automatic default no matter what no plans to make a conversion for integers
        self.Instructions = QLabel(
            'Input Format is as Follows... "Table Name", "row, numbers, seperated, with, commas" ')

        """
        These aren't a QtableWidget these are QlineEdits that ask the user to input which table and which rows they
        want to pull data from. Quotations are neccessary. 

        *Quotations allow function shelex.split() to split on quotations and then store in a list

        """
        self.TableRowEntry1 = QLineEdit(' "Table", "Rows Numbers" ')
        self.TableRowEntry2 = QLineEdit(' "Table", "Rows Numbers" ')
        self.TableRowEntry3 = QLineEdit(' "Table", "Rows Numbers" ')
        self.TableRowEntry4 = QLineEdit(' "Table", "Rows Numbers" ')
        self.TableRowEntry5 = QLineEdit(' "Table", "Rows Numbers" ')

        ##Create buttons for box and scatter plot
        self.BoxPlot = QPushButton("Box Plot")
        self.ScatterPlot = QPushButton("Scatter Plot")

        """
        This is prob not going to work Overload???

        does the on enter need to be for every btn????
        """
        self.TableRowEntry1.returnPressed.connect(self.BoxPlot.click)
        self.TableRowEntry2.returnPressed.connect(self.BoxPlot.click)
        self.TableRowEntry3.returnPressed.connect(self.BoxPlot.click)
        self.TableRowEntry4.returnPressed.connect(self.BoxPlot.click)
        self.TableRowEntry5.returnPressed.connect(self.BoxPlot.click)

        # <editor-fold desc="Error msg feedback">

        ###WORK IN PROGRESS: Error msgs and error handling###
        self.ErrorMsg = QMessageBox()
        self.ErrorMsg.setText("Nothing for now")
        self.ErrorMsg.setInformativeText("This is additional information")
        self.ErrorMsg.setWindowTitle("Error Message")
        self.ErrorMsg.setDetailedText("The details are as follows:")

        # </editor-fold>

        # Initial values (TEST VALUES)
        self.Label = QLabel("Empty right now")
        self.text = "initial string"

        """
            Currently these values are just the strings from default setting of the QlineEdit
            .text() grabs whatever text is inside the QLineEdits, which right now is ' "Table", "Rows Numbers" '
        """
        self.Entry1 = self.TableRowEntry1.text()
        self.Entry2 = self.TableRowEntry2.text()
        self.Entry3 = self.TableRowEntry3.text()
        self.Entry4 = self.TableRowEntry4.text()
        self.Entry5 = self.TableRowEntry5.text()

        """
            Checks to see if the text in the QlineEdit has changed and if it has it passes the arguments a string, and a
            number representing which QlineEdit was modified, 1-5 descending order.
            partial allows for the passing of multiple arguments through, what is normally only one

        """
        self.TableRowEntry1.textChanged[str].connect(partial(self.onChanged, entryNum=1))
        self.TableRowEntry2.textChanged[str].connect(partial(self.onChanged, entryNum=2))
        self.TableRowEntry3.textChanged[str].connect(partial(self.onChanged, entryNum=3))
        self.TableRowEntry4.textChanged[str].connect(partial(self.onChanged, entryNum=4))
        self.TableRowEntry5.textChanged[str].connect(partial(self.onChanged, entryNum=5))

        print("About to call plotting functions")
        ###Takes the Entrys that have been made connects it my my methods Box/ScatterPlotCall###
        self.BoxPlot.clicked.connect(self.BoxPlotCall)
        self.ScatterPlot.clicked.connect(self.ScatterPlotCall)

        ###LAYOUT###
        # <editor-fold desc="Layout">
        self.vboxMain = QVBoxLayout(self.main_widget)
        self.VboxCOMP1 = QVBoxLayout()

        self.vboxMain.addLayout(self.VboxCOMP1)

        self.Header = QHBoxLayout()
        self.Header.addWidget(self.TableHeader)
        self.Header.addWidget(self.RowHeader)

        self.subHeader = QHBoxLayout()
        self.subHeader.addStretch()
        self.subHeader.addWidget(self.Instructions)

        self.hboxCOMP1 = QHBoxLayout()
        # self.hboxCOMP1.addStretch()
        self.hboxCOMP1.addWidget(self.TableRowEntry1)
        self.hboxCOMP1.addStretch()

        self.hboxCOMP2 = QHBoxLayout()
        # self.hboxCOMP2.addStretch()
        self.hboxCOMP2.addWidget(self.TableRowEntry2)
        self.hboxCOMP2.addStretch()

        self.hboxCOMP3 = QHBoxLayout()
        # self.hboxCOMP3.addStretch()
        self.hboxCOMP3.addWidget(self.TableRowEntry3)
        self.hboxCOMP3.addStretch()

        self.hboxCOMP4 = QHBoxLayout()
        # self.hboxCOMP3.addStretch()
        self.hboxCOMP4.addWidget(self.TableRowEntry4)
        self.hboxCOMP4.addStretch()

        self.hboxCOMP5 = QHBoxLayout()
        # self.hboxCOMP3.addStretch()
        self.hboxCOMP5.addWidget(self.TableRowEntry5)
        self.hboxCOMP5.addStretch()

        self.hboxPlotBtns = QHBoxLayout()
        self.hboxPlotBtns.addWidget(self.BoxPlot)
        self.hboxPlotBtns.addWidget(self.ScatterPlot)
        self.hboxPlotBtns.addStretch()

        self.hboxRAND = QHBoxLayout()
        self.hboxRAND.addWidget(self.Label)

        ### ADD TO PAGE ###
        self.VboxCOMP1.addLayout(self.Header)
        self.VboxCOMP1.addLayout(self.subHeader)
        self.VboxCOMP1.addLayout(self.hboxCOMP1)
        self.VboxCOMP1.addLayout(self.hboxCOMP2)
        self.VboxCOMP1.addLayout(self.hboxCOMP3)
        self.VboxCOMP1.addLayout(self.hboxCOMP4)
        self.VboxCOMP1.addLayout(self.hboxCOMP5)
        self.VboxCOMP1.addLayout(self.hboxPlotBtns)
        # self.VboxCOMP1.addLayout(self.hboxRAND)
        # </editor-fold>

    def onChanged(self, text, entryNum):
        """
            Purpose: checks to see which QlineEdit was modfied using the QlineEdit number
            takes the text in the LineEdit and defines it as the User's entry text
        """

        if entryNum == 1:
            self.text = text
            userIN = str(self.text)
            self.Entry1 = userIN
        elif entryNum == 2:
            self.text = text
            userIN = str(self.text)
            self.Entry2 = userIN
        elif entryNum == 3:
            self.text = text
            userIN = str(self.text)
            self.Entry3 = userIN
        elif entryNum == 4:
            self.text = text
            userIN = str(self.text)
            self.Entry4 = userIN
        elif entryNum == 5:
            self.text = text
            userIN = str(self.text)
            self.Entry5 = userIN

        else:
            print("something was passed")
            pass

        # List with all possible entries looking at a maximum of 5???
        # possibly problematic in case future iterations want to include more entries
        ###Create a list containg all entries the user has input###
        self.ALLentries = [self.Entry1, self.Entry2, self.Entry3, self.Entry4, self.Entry5]

    def CheckEntries(self):
        """
            Purpose
            Check to see which entries have been modified returns True if user input is detected
            The check is run by comparing the current state (string) to the default string which is...
            "Table", "Rows Numbers"
            QUOTATIONS ARE NECCESSARY in order to parse user input later on with shelex() method

        """
        if self.Entry1 == ' "Table", "Rows Numbers" ':
            self.userInput = False
        else:
            self.userInput = True

        if self.Entry2 == ' "Table", "Rows Numbers" ':
            self.userInput2 = False
        else:
            self.userInput2 = True

        if self.Entry3 == ' "Table", "Rows Numbers" ':
            self.userInput3 = False
        else:
            self.userInput3 = True

        if self.Entry4 == ' "Table", "Rows Numbers" ':
            self.userInput4 = False
        else:
            self.userInput4 = True

        if self.Entry5 == ' "Table", "Rows Numbers" ':
            self.userInput5 = False
        else:
            self.userInput5 = True

    def BoxPlotCall(self):

        # runs method CheckEntries to see which LineEdits were actually modfied, returns booleans to expediate the next proccess
        self.CheckEntries()

        # List of truth values see which lineEdits the user has changed

        # most likely put this in my checkEntries method
        UserInputList = [self.userInput, self.userInput2, self.userInput3, self.userInput4, self.userInput5]

        # List to save index for the tables whos QlineEdits have changed
        MutableList = []

        """
            Enumerate goes through a list and creates an order pair with the item and its index.
            For example the list [apple, grape, berry], once enumerated, becomes [(0, apple),(1, grape),(2, berry)]
        """

        UserInputList = list(enumerate(UserInputList))
        print("enumerated userinput list")
        print(UserInputList)

        ###For loop runs through our list of booleans and checks to see which ones are True ('modifed from user inputting something')
        for index, item in enumerate(UserInputList, start=0):
            print("item is .... {}".format(item))
            # print([item[1] for i in UserInputList])

            # checks the ordered pair and look at the second item in the pair to check the boolean
            if item[1] == True:
                print(item)
                # appends the index for that item to a list to be referenced later on
                MutableList.append(index)

                ###Print Statements for debugging###
                print("printing index ... {}".format(index))
                print("printing mutablelist ... ")
                print(MutableList)
            else:
                pass

        # Want to call for all tables that have been changed
        # We have the numbers now we want to attach those to our variable and call it as such

        print("Parsing is about to begin")

        ParsedList = []  # initiate a list to store all parsed strings from the QlineEdits
        self.RowNumList = []  # initiate a list to store Row numbers
        self.TableList = []  # initiate a list to store Table Names

        """
            For loop parses string and stores parsed strings into two seperate lists
            one list for row numbers and the other for the table names
        """
        i = 0
        for i in range(len(MutableList)):
            print("mutable list is as follows...")
            print(MutableList)
            print("Inisde parse loop, i value is {}".format(i))
            print(self.ALLentries[MutableList[i]])
            """
                shelex.split() is a unique parser in that it seperates based on quotations (" ")
                This used to seperate the Table Names, and Row Numbers since both are surrounded by quotations
            """
            ParsedString = shlex.split(self.ALLentries[MutableList[i]])
            print("parsed string is ..... {}".format(ParsedString))
            print(type(ParsedString))

            # attach parsed string to our list
            ParsedList.append(ParsedString)
            print(ParsedList)

            print("second element of string ... {}".format(ParsedList[i][1]))

            ###Selecting the row numbers###_____________________________________________________________________________

            # further split the nested list using the fact each item is sepereated with a comma
            RowVals = ParsedList[i][1].split(',')
            print("ROWS TO BE SELECTED are as follows...")
            print(RowVals)
            print("right before mapping")

            # convert the strings into integers
            RowVals = list(map(int, RowVals))

            print("Row Values after mapping has taken place")
            print(RowVals)
            self.RowNumList.append(RowVals)
            print(self.RowNumList)

            # DEBUGGING STATEMENTS TO CHECK OUTPUT
            # print(self.RowNumList)
            # print(type(self.RowNumList[0]))


            ###Selecting the Table Number###____________________________________________________________________________
            # Methodology is similar to RowVal collection above. Follows almost same proccess

            print("Right before appending things to Table List")
            TableEntry = ParsedList[i][0].split(',')

            print("Table list is as follows")
            print(TableEntry)
            print(type(TableEntry[0]))
            print("first element of table entry is .... {}".format(TableEntry[0]))

            """
                Error Handling depending on user input if the table name is a number vs a string we have to
                approach the problem differently. First checks to see if the string can be converted to an integer else
                it just continues on as a string.

                POSSIBLE BUG: if it can be converted to integer might skip all below code and just end. ErrorHandling W.I.P.
            """

            TableVal = (TableEntry[0])
            self.TableList.append(TableVal)
            print("current counter is ............... {}".format(i))

        # string value so we know when we call plot to do a boxplot
        self.PlotCompareVal = "box"

        ###output check###
        print("Parsedstring list is here .......... {}".format(ParsedList))
        print("Row numbers list is as follows.... {}".format(self.RowNumList))

        print("Table List is as follows....{}".format(self.TableList))
        print(self.TableList)

        # This is the data for which Table Names and which Rows need to be plotted
        print(type(self.RowNumList))
        print(type(self.TableList))

        ###SIGNAL EMMITTION W.I.P.
        self.MultiBoxSignal.emit(self.TableList, self.RowNumList, self.PlotCompareVal)

    def ScatterPlotCall(self):
        print("scatter plot called")
        ### W.I.P###