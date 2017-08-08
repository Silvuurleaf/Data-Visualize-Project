# imports/libraries
# <editor-fold desc="Imports and Libraries">
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QLineEdit, QPushButton, QSlider, QApplication, QVBoxLayout, QHBoxLayout,
                             QApplication, QWidget, QLabel, QCheckBox, QRadioButton,QMainWindow,
                             QFileDialog, QMenu, QMessageBox, QAction, QToolBar, QDialog, QTableWidget, QTableWidgetItem)
from PyQt5.QtCore import Qt, pyqtSignal

import matplotlib

matplotlib.use("Qt5Agg")
from matplotlib import pyplot as plt
plt.style.use(['ggplot'])
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

import csv
import pandas as pd

import linecache

#Custom Modules
import CreateFigure
import CompareWindow
import TableUI
import PTable
import Debugger



# </editor-fold>


class MainWindow(QMainWindow):
    """"
            Purpose: Mainwindow screen stores majority of application widgets.
            Responsible for displaying datatable and user interaction of upload, and datamanipulation

    """

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Perspective")

        # Initializes the user interface window
        self.initializeUI()

        # calls our class CompareWindow and creates a window that runs in the background
        self.compareWin = CompareWindow.ComparisonUI()

        # Adjust the max size the window can be
        self.compareWin.resize(350, 200)
        self.compareWin.setMaximumSize(500, 250)

        #calls the class TablePopWin to create the window to ask the user to name the table
        self.TablePopWin = TableUI.TablePopup()

        #creates an instance of our debugger to be used if need be.
        self.Debugger = Debugger.ErrorFind()

    def initializeUI(self):

        # initiate list for table objects and dictionary to pair names with objects
        self.TableDB = []
        self.TableNameDB = []
        self.TableDictionary = {}


        ###set the main widget responsible for making widgets appear on scren
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        # CREATION OF WIDGETS GENERAL BUTTONS____________________________________________________________________________
        # <editor-fold desc="Widgets Creation CheckPoint">

        ###first file###
        # buttons associated with the first browse button
        """
            Buttons related to the first file being uploaded
        """
        self.FileNmLabel = QLabel('FileName')
        self.FileNameEdit = QLineEdit('"Filename"')
        self.FileNameEdit.setMaximumSize(200, 20)
        self.BrowseBtn = QPushButton('Browse')
        self.BrowseBtn.setMaximumSize(80, 20)

        self.OpacityLabel = QLabel('Opacity')
        self.OpacitySlider = QSlider(Qt.Horizontal)
        self.OpacitySlider.setMinimum(0)
        self.OpacitySlider.setMaximum(100)
        self.OpacitySlider.setValue(100)
        self.OpacitySlider.setTickInterval(10)
        self.OpacitySlider.setTickPosition(QSlider.TicksBelow)
        self.OpacitySlider.setMaximumSize(200, 20)

        self.ShowChkbx = QCheckBox('show')

        ###Overlay Plot###
        # checkbox to give user ability to overlay data
        self.Overlay = QCheckBox('Overlay Plots')

        self.comparison = QPushButton('Compare')
        self.comparison.setMaximumSize(80, 20)

        # </editor-fold>__________________________________________________________________________END OF WIDGET CREATION




        # Button Functionality___________________________________________________________________________________________
        # <editor-fold desc="Button Functionality">

        # connect the browse button to method ImportFile
        self.BrowseBtn.clicked.connect(self.ImportFile)

        # whenver the value of the slider is changed connect to the method OpacityVal
        self.OpacitySlider.valueChanged.connect(self.OpacityVal)

        # connect comparison button to method OpenCompare
        self.comparison.clicked.connect(self.OpenCompare)

        # </editor-fold>_____________________________________________________________________END OF BUTTON FUNCTIONALITY




        # Widget Layout_________________________________________________________________________________________________
        # <editor-fold desc="Layout">


        self.hMAIN = QHBoxLayout(self.main_widget)

        ###First File Labels###
        self.hbox2 = QHBoxLayout()
        self.hbox2.addWidget(self.FileNmLabel)
        self.hbox2.addStretch()
        self.hbox2.addWidget(self.OpacityLabel)

        ###First File Widgets###
        self.hbox3 = QHBoxLayout()
        self.hbox3.addWidget(self.FileNameEdit)
        self.hbox3.addWidget(self.BrowseBtn)
        self.hbox3.addWidget(self.OpacitySlider)
        self.hbox3.addWidget(self.ShowChkbx)

        ###OverLay###
        self.hbox5 = QHBoxLayout()
        self.hbox5.addWidget(self.Overlay)
        self.hbox5.addWidget(self.comparison)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.hbox2)
        self.vbox.addLayout(self.hbox3)
        self.vbox.addLayout(self.hbox5)

        self.vboxRIGHT = QVBoxLayout()

        ###SOme of these layouts are not utilized anymore
        self.HboxGraph = QHBoxLayout()
        # self.HboxGraph.addWidget(self.canvas)

        # self.vboxGraph = QVBoxLayout()
        # self.vboxGraph.addWidget(self.canvas)

        self.vboxNavBar = QVBoxLayout()
        # self.vboxNavBar.addWidget(self.NavBar)

        self.vboxData = QVBoxLayout()

        # self.vboxRIGHT.addLayout(self.vboxGraph)
        self.vboxRIGHT.addLayout(self.vbox)
        self.vboxRIGHT.addLayout(self.HboxGraph)
        self.vboxRIGHT.addLayout(self.vboxNavBar)
        self.vboxRIGHT.addLayout(self.vboxData)

        self.hMAIN.addLayout(self.vbox)
        self.hMAIN.addLayout(self.vboxRIGHT)

        # </editor-fold>

        self.show()

    def ImportFile(self):
        ###Actual importation and manipulation of Data CSV Files

        ### on click opens a dialog window asks user to pick a file from the directory and then stores the file's path.
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "(*.csv)")
        if fileName:
            print(fileName)
            self.FileNameEdit.setText(fileName)
            Data = pd.read_csv(open(fileName))
            # print(Data)

            ### removes all the statistics information from the file and reports just the raw data

            # <editor-fold desc="Data Reformatting Proccess">

            self.BaseStats = Data.drop('Nominal Value', axis=1)
            self.BaseStats.drop('median', axis=1, inplace=True)
            self.BaseStats.drop('Tolerance', axis=1, inplace=True)
            self.BaseStats.drop('mean', axis=1, inplace=True)
            self.BaseStats.drop('min', axis=1, inplace=True)
            self.BaseStats.drop('max', axis=1, inplace=True)
            self.BaseStats.drop('range', axis=1, inplace=True)
            self.BaseStats.drop('Deviation', axis=1, inplace=True)
            self.BaseStats.drop('variance', axis=1, inplace=True)
            self.BaseStats.drop('Standard Deviation', axis=1, inplace=True)
            self.BaseStats.drop('LowerBound', axis=1, inplace=True)
            self.BaseStats.drop('UpperBound', axis=1, inplace=True)
            self.BaseStats.drop('Unnamed: 0', axis=1, inplace=True)

            # print("Data has been dropped")
            # </editor-fold>

            # grabs the index as the row headers, and grabs the column index ti be the new column headers
            rowHeaders = self.BaseStats.index
            colHeaders = self.BaseStats.columns.values

            col = len(colHeaders)
            row = len(rowHeaders)

            print("table is about to be made")

            ######### PASS DATABASES THROUGH HERE!?????????!?!?!?
            # Create an instance of the table passing the data, number of rows and cols
            self.Table = PTable.CreateTable(self.BaseStats, row, col, colHeaders)

            print("Table has been made")

            ###OPEN POPUP WINDOW AND ASK FOR USER TO GIVE TABLE A NAME
            self.TablePopWin.show()
            #self.TableDB.append(self.Table)  # list stores objects of all tables made

            # First popup window when table is created signal is sent
            self.TablePopWin.TableString.connect(self.NameAssignment)
            #self.TableNameDB.append(self.Table.name)  # list stores all names of table objects

            # connecting signal created after user renames a table from the context menu
            self.Table.reNameSignal.connect(self.ReNameAdjustments)

            # connects the emitted data signal to plot initiator
            self.Table.dataSignal.connect(self.initiatePlot)


            ### TEMPORARILY DISABLED FOR TESTING PURPOSES###
            try:
                 self.compareWin.MultiBoxSignal.connect(self.initiateMultiPlot)
            except Exception as e:
                 print(e)

            # embeds the datatable into our window
            self.vboxData.addWidget(self.Table)

    def OpenCompare(self):
        print("opening compare window")
        self.compareWin.show()

    def NameAssignment(self, TableName):
        oldName = self.Table.name
        print("inside Name Assignment")
        self.Table.name = TableName

        print("adjusting table name database")
        print(self.TableNameDB)
        for i in range(len(self.TableNameDB)):
            if self.TableNameDB[i] == oldName:
                self.TableNameDB[i] = TableName
        print(self.TableNameDB)

        print(self.Table.name)

        print("Before")
        print("List of table objects........... {}".format(self.TableDB))
        print("List of table names..............{}".format(self.TableNameDB))
        print("Dictionary.......................{}".format(self.TableDictionary))

        self.DataBaseCreation()

        print("List of table objects........... {}".format(self.TableDB))
        print("List of table names..............{}".format(self.TableNameDB))
        print("Dictionary.......................{}".format(self.TableDictionary))

        # self.DictionCreation() #COULD IS PROBLEMATIC_____________________________________________________________

    def ReNameAdjustments(self, oldName, newName):
        print("rename has been called from the context menu on the QtableWidget")
        print("table name database before for loop")
        print(self.TableNameDB)
        for i in range(len(self.TableNameDB)):
            if self.TableNameDB[i] == oldName:
                self.TableNameDB[i] = newName
        print(self.TableNameDB)

        print("Before")
        print("List of table objects........... {}".format(self.TableDB))
        print("List of table names..............{}".format(self.TableNameDB))
        print("Dictionary.......................{}".format(self.TableDictionary))

        self.DataBaseCreation()

        print("List of table objects........... {}".format(self.TableDB))
        print("List of table names..............{}".format(self.TableNameDB))
        print("Dictionary.......................{}".format(self.TableDictionary))

    def DataBaseCreation(self):
        print("starting database collection of table names, objects")

        self.TableDB.append(self.Table)
        self.TableNameDB.append(self.Table.name)  # list stores all names of table objects
        self.TableDictionary = dict(zip(self.TableNameDB, self.TableDB))

    def initiatePlot(self, x, y, PlotVal):
        print("emit signal")
        print(x)
        print(y)
        try:
            f = CreateFigure.FigureAssembly()
        except Exception as e:
            print(e)

        f.plotData(x, y, PlotVal, True)

    def initiateMultiPlot(self, tableV, rowV, PlotV):
        """
            1. Match TableName values with the key values in our TableDB
            2. When we find a  match look at that key's corresponding Table Object, and iterate
            through that objects rows and select the rows specified by rowV
            3.Call plot for those values

        """
        f = CreateFigure.FigureAssembly()
        print("")
        for i in tableV:
            """
                tableV: is list of strings that represent assigned tablenames [Table1, Table2, Table3]
                rowV: is a list, containing lists representing rows from corresponding Tables the user wishes to plot.
                    for example [[1,2],[3,4],[1]] means rows 1,2 from table1, rows 3,4 from table2... so on
                PlotV: is a string that is ethier "box" or "whisker" to tell what method to plot. Default right now 
                is to do a simple boxplot
            """
            print("Creating table instance")

            #Table Dictionary is setup so the names of the Tables (tableV) are the keys of the dictionary
            # and the actual table objects are referenced by these keys
            self.TableOBJ = self.TableDictionary[i]
            print("Data Type for the table object is..................{}".format(type(self.TableOBJ)))
            self.Elements = []
            try:
                for row in rowV:

                    for i in row:
                        print("rowV value is... {}".format(rowV))
                        print("current row list{}".format(row))
                        print("i value is {}".format(i))
                        print("itterating")

                        for j in range(self.TableOBJ.columnCount()):
                            print("i value is ...{}".format(i))
                            print("j value is .... {}".format(j))

                            #idea 1 trying to select rows
                            print("i value is ...{}".format(i))
                            print("j value is .... {}".format(j))
                            EntireRow = self.TableOBJ.selectRow(i)
                            print(EntireRow)

                            #selecteditems

                            #idea 2 iterate through entire table
                            item = self.TableOBJ.itemAt(i,j)
                            print(self.TableOBJ.itemAt(1,1).text())
                            print(self.TableOBJ.itemAt(3,3).text())
                            print("printing item...... {}".format(item))
                            element = item.text()
                            print(element)
                            self.Elements.append(element)

                        #elements = [self.TableOBJ.item(i, j).text() for j in range(self.TableOBJ.columnCount()) if
                        #            self.TableOBJ.item(i, j).text() != ""]
                        #print(elements)

            except Exception as e:
                print(e)

            print(self.Elements)


            # for j in rowV:
            #       for k in j:
            #         print("selecting rows")
            #         print(self.TableOBJ.selectRow(k))
            #
            #         x = self.TableOBJ.selectRow(k)
            #         print("x data is here before plot command is issued................... {}".format(x))
            #         y = self.TableOBJ.ColHeader
            #         f.plotData(x,y,PlotV, False)


        #f.plt.show()
                    # need a list of table names to compare against???
                    # everytime we make a new table add it's name to a list
                    # select table with the same name as == tableV[i]



    def OpacityVal(self):
        OpacitySignal = pyqtSignal(int)
        print("Opacity value is being changed")


def main():
    # main loop
    app = QApplication(sys.argv)

    # instance
    window = MainWindow()
    window.show()
    # appWindow = MainWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()



#         # <editor-fold desc="Error msg feedback">
#
#         ###WORK IN PROGRESS: Error msgs and error handling###
#         self.ErrorMsg = QMessageBox()
#         self.ErrorMsg.setText("Nothing for now")
#         self.ErrorMsg.setInformativeText("This is additional information")
#         self.ErrorMsg.setWindowTitle("Error Message")
#         self.ErrorMsg.setDetailedText("The details are as follows:")
#
#         # </editor-fold>