from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QTableWidgetItem, QTableWidget, QMenu)
from PyQt5.QtCore import Qt, QAbstractTableModel, pyqtSignal

import TableUI

import numpy as np



class CreateTable(QTableWidget):
    dataSignal = pyqtSignal(list, np.ndarray, str)  # Signal Emitted to send x,y data for plotting
    reNameSignal = pyqtSignal(str, str)  # signal to send the previous name of the table and the assigned new name
    DictionarySignal = pyqtSignal()  # supposedly the signal to run dictionary re-creation

    # Maybe add boolean to dictionary signal


    def __init__(self, Data, row, col, colHeaders):
        super(CreateTable, self).__init__()

        print("Start initialization: Table Creation is underway")

        # initiate a name to give to the table before the user assigns it a name.
        self.name = "temporary name"

        self.setSelectionBehavior(self.SelectRows)

        self.ColHeader = colHeaders
        self.setRowCount(row)
        self.setColumnCount(col)
        self.data = Data
        self.setHorizontalHeaderLabels(colHeaders)

        print("Right Before for loop to assign data to QTableWidget")

        n = len(Data)
        m = len(colHeaders)

        for i in range(n):
            DataValues = self.data.iloc[i, :]
            print("values are {}".format(DataValues))
            # m = len(values)
            #ConvertedVals = pd.to_numeric(DataValues)

            ValList = DataValues.values.tolist()
            print(ValList)

            for j in range(0, m):
                self.item = QTableWidgetItem(str(round(ValList[j], 6)))
                # print("{}, {}".format(i, j))
                self.setItem(i, j, self.item)

    def contextMenuEvent(self, event):

        menu = QMenu(self)
        graphAction = menu.addAction("Graph")  # Boxplt

        scatterAction = menu.addAction("Scatter Plot")
        checkAttributesAction = menu.addAction("Table Attributes")
        ###checkAttributes open a settings-esque window


        ReNameAction = menu.addAction("Rename")
        printNameAction = menu.addAction("Name?")
        printAction = menu.addAction("Print Row")
        quitAction = menu.addAction("Close Table")

        action = menu.exec_(self.mapToGlobal(event.pos()))

        if action == quitAction:
            self.deleteLater()
        elif action == printAction:
            self.selected = self.selectedItems()
            n = len(self.selected)
            print("n is {}".format(n))
            for i in range(n):
                self.selected[i] = str(self.selected[i].text())
            for i in range(n):
                self.selected[i] = float(self.selected[i])
            print(self.selected)

        ###Attribute Naming related actions###
        elif action == ReNameAction:
            self.openPop = TableUI.TablePopup()
            self.openPop.show()
            self.openPop.TableString.connect(self.RenameTable)

        elif action == printNameAction:
            print(self.name)

        ###GRAPHING COMMANDS###
        elif action == graphAction:
            self.selected = self.selectedItems()
            n = len(self.selected)
            for i in range(n):
                self.selected[i] = str(self.selected[i].text())
            for i in range(n):
                self.selected[i] = float(self.selected[i])
            print("right before plotter called")

            # self.Graph = Plotter(self.selected, self.ColHeader)
            print(type(self.selected), type(self.ColHeader))

            # self.plotbtn.clicked.connect(partial(self.initiatePlot, xdata, ydata))
            self.PlotVal = "box"
            self.dataSignal.emit(self.selected, self.ColHeader, self.PlotVal)

        elif action == scatterAction:
            self.selected = self.selectedItems()
            n = len(self.selected)
            for i in range(n):
                self.selected[i] = str(self.selected[i].text())
            for i in range(n):
                self.selected[i] = float(self.selected[i])
            print("right before plotter called")

            # self.Graph = Plotter(self.selected, self.ColHeader)
            print(type(self.selected), type(self.ColHeader))

            self.PlotVal = "scatter"
            self.dataSignal.emit(self.selected, self.ColHeader, self.PlotVal)

        else:
            print("u clicked something other than quit")

    def RenameTable(self, TableName):
        currentName = self.name
        print("inside RenameTable")
        self.name = TableName
        print(self.name)

        self.reNameSignal.emit(currentName, self.name)

        #self.DictionarySignal.emit()  # COULD BE PROBLEMATIC_____________________________
        # for i in range(len(self.TableNameDB)):
        #     if self.TableNameDB[i] == currentName:
        #         self.TableNameDB[i] = TableName

    def NameChange(self, string):
        print("name change initiate")
        self.name = string
        print("table name is {}".format(self.name))