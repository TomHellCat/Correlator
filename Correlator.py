from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow,QDesktopWidget, QMessageBox, QHBoxLayout, QLabel, QFormLayout, QVBoxLayout, QScrollArea, QApplication, QAbstractItemView, QWidget, QAction, QTableWidget,QTableWidgetItem, QFileDialog, QGridLayout, QGroupBox
from PyQt5.QtCore import *
from PyQt5.QtGui import QColor, QBrush
import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model
from sklearn.utils import shuffle
import os
import ctypes
myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Correlator")
        MainWindow.resize(800, 600)
        MainWindow.setWindowTitle("Correlator")
        MainWindow.setWindowIcon(QtGui.QIcon('correlator.png'))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.v = QVBoxLayout(self.centralwidget)
        self.scroll = QScrollArea()
        self.v.addWidget(self.scroll)
        #self.scroll.resize(800, 600)
        self.widget = QWidget()
        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.hGBox = QGroupBox()
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 0, 0))
        self.tableWidget.setObjectName("tableWidget")
        self.widget.setLayout(self.vbox)
        self.l = QLabel()
        self.l.setText('')
        self.l.setGeometry(QtCore.QRect(300, 40, 400, 50))
        self.B = QtWidgets.QPushButton()
        self.B.setText("Find Correlation")
        self.hbox.addWidget(self.l)
        self.hGBox.setLayout(self.hbox)

        
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(310, 240, 171, 51))
        self.pushButton.setObjectName("pushButton")
        self.vbox.addWidget(self.pushButton)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew_File = QtWidgets.QAction(MainWindow)
        self.actionNew_File.setShortcutContext(QtCore.Qt.WidgetWithChildrenShortcut)
        self.actionNew_File.setShortcutVisibleInContextMenu(False)
        self.actionNew_File.setObjectName("actionNew_File")
        self.menuFile.addAction(self.actionNew_File)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Correlator", "Correlator"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.pushButton.setText(_translate("MainWindow", "Open A File"))
        self.pushButton.clicked.connect(self.open_file_dialog)
        self.B.clicked.connect(self.get_data)
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionNew_File.setText(_translate("MainWindow", "New File"))
        self.actionNew_File.setStatusTip(_translate("MainWindow", "Open a new File"))
        self.actionNew_File.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>Something</p><p><br/></p><p><br/></p></body></html>"))
        self.actionNew_File.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionNew_File.triggered.connect(self.openNewFile)
        self.pushButton.setMinimumWidth(250)
        self.pushButton.resize(250,50)
        self.pushButton.setMinimumHeight(50)
        self.vbox.setAlignment(self.pushButton,QtCore.Qt.AlignHCenter)
        self.pushButton.setMinimumWidth(200)
        self.pushButton.resize(200,50)
        self.pushButton.setMinimumHeight(50)
        self.pushButton.setStyleSheet("color: solid black;\n"
                             "font:bold 12px;\n")
                                      
                                      
        
        
        

    def open_file_dialog(self,x=False):
        filename = QtWidgets.QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","Csv Files (*.csv)")    
        if(len(filename[0]) > 0):
            self.vbox.addWidget(self.hGBox)
            self.vbox.addWidget(self.tableWidget)
            self.add(filename[0])
            if(x==False):
                self.pushButton.setParent(None)
                self.pushButton.deleteLater()
            self.lst = []
        
    def cell_was_clicked(self, row, column):
        item = self.tableWidget.item(row, column)
        c = True
        if(row == 0):
            i = self.tableWidget.item(1, column)
            try:
                float(i.text())
                c = True
            except ValueError:
                c = False
            
        if(c == True):
            if(row == 0):
                self.lst.append(item)
                print(item.text())  
                if len(self.lst) == 1 and row == 0:
                    item.setBackground(QBrush(QColor("green")))
                elif len(self.lst) > 1 and row == 0:
                    item.setBackground(QBrush(QColor("lightBlue")))
                    
            if(len(self.lst) == 1):
                self.l.setText('Select the labels that you think has correlation with the selected label')
                self.l.setGeometry(QtCore.QRect(300, 40, 400, 50))
                self.l.setMinimumHeight(40)
                self.removeLabels()
            elif(len(self.lst) > 1):
                self.B.setMinimumHeight(40)
                self.B.setGeometry(QtCore.QRect(500, 40, 100, 50))
                self.B.setStyleSheet("color: solid black;\n"
                             "font:bold 12px;\n")
                self.hbox.addWidget(self.B)
        else:
            #error = QtWidgets.QErrorMessage()
            #error.showMessage('Cannot work on non numerical values')
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Cannot work on non-numerical data')
            msg.setWindowTitle("Error")
            msg.exec_()

    def add(self, path):
        self.tableWidget.setGeometry(QtCore.QRect(20, 120, 751, 1200))#(20, 120, 751, 431)
        self.l.setText('Select the label that you want to examine')
        self.l.setMinimumHeight(40)
        self.l.setGeometry(QtCore.QRect(500, 40, 300, 50))
        self.l.setStyleSheet("color: solid black;\n"
                             "font:bold 14px;\n")
                             
        self.data = pd.read_csv(path, sep=None, iterator=True)
        inf = self.data._engine.data.dialect.delimiter
        self.data = pd.read_csv(path, sep=inf)
        r = self.data.shape[0]
        c = self.data.shape[1]
        self.tableWidget.setRowCount(r+1)
        self.tableWidget.setColumnCount(c)
        self.tableWidget.setMinimumHeight(900)
        self.tableWidget.cellClicked.connect(self.cell_was_clicked)
        lst = self.data.columns.values
        for i in range(len(lst)):
            self.tableWidget.setItem(0,i, QTableWidgetItem(str(lst[i])))   
        for i in range(r):            
            l = self.data.loc[i,:].tolist() 
            for j in range(c):
                self.tableWidget.setItem(i+1,j, QTableWidgetItem(str(l[j])))
        self.labelList = []
        self.Dic = {}
        

    def get_data(self):
        pred = self.lst[0].text()
        print(type(pred))
        att = []
        for i in range(1, len(self.lst)):
            att.append(self.lst[i].text())
        d = self.data[att]
        print(type(d))
        self.correlation(pred, d)
        for i in range(len(self.lst)):
            self.lst[i].setBackground(QBrush(QColor("white")))
        self.lst = []
        self.l.setMinimumHeight(40)
        self.l.setText("Select the label that you want to examine")
        self.hbox.removeWidget(self.B)
        self.B.setGeometry(QtCore.QRect(20, 120, 0,0))
        
    

    def correlation(self, pred, att):
        cor = 0
        cor_att = ""
        y = np.array(self.data[pred])
        for i in att:
            X = np.array(self.data[[i]])
            x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X,y, test_size=0.1)
            linear = linear_model.LinearRegression()

            linear.fit(x_train, y_train)
            acc = linear.score(x_test, y_test)
            if(cor < acc):
                cor = acc
                cor_att = i
            
            self.Dic[acc] = i
            print("Att: ", i ,"Accuracy: ", acc)
        self.labelList.append(QLabel('Correlation with selected Labels'))
        for i in sorted(self.Dic.items(),reverse=True):
            self.labelList.append(QLabel(str(i[1])+ ': '+ str(i[0])))
        for i in range(len(self.labelList)):
            self.vbox.addWidget(self.labelList[i])
            self.labelList[i].setStyleSheet("color: solid black;\n"
                             "font-size: 12px;\n")
            
        print("Attribute with max correlation: ", cor_att ,"\n",
          "Accuracy: ", cor)
        self.tableWidget.setMinimumHeight(400)
        self.labelList[0].setStyleSheet("color: solid black;\n"
                             "font:bold 14px;\n")
        
    def removeLabels(self):
        for i in range(len(self.labelList)):
            self.vbox.removeWidget(self.labelList[i])
            self.labelList[i].setParent(None)
            self.labelList[i].deleteLater()
        self.labelList = []
        self.Dic = {}

    def openNewFile(self):
        self.removeLabels()
        #self.open_file_dialog(True)
        self.lst = []
        filename = QtWidgets.QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","Csv Files (*.csv)")    
        if(len(filename[0]) > 0):
            path = filename[0]
            self.data = pd.read_csv(path, sep=None, iterator=True)
            inf = self.data._engine.data.dialect.delimiter
            self.data = pd.read_csv(path, sep=inf)
            r = self.data.shape[0]
            c = self.data.shape[1]
            self.tableWidget.setRowCount(r+1)
            self.tableWidget.setColumnCount(c)
            lst = self.data.columns.values
            for i in range(len(lst)):
                self.tableWidget.setItem(0,i, QTableWidgetItem(str(lst[i])))   
            for i in range(r):            
                l = self.data.loc[i,:].tolist() 
                for j in range(c):
                    self.tableWidget.setItem(i+1,j, QTableWidgetItem(str(l[j])))
            self.hbox.removeWidget(self.B)
            self.B.setGeometry(QtCore.QRect(20, 120, 0,0))

            
        

    
        

    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    #ui.something()
    MainWindow.show()
    sys.exit(app.exec_())
