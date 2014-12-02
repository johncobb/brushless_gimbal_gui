

from PyQt4 import QtGui
from PyQt4.Qt import pyqtSignal, QString
from console.console_view import Ui_ConsoleView



class ConsoleCtl(QtGui.QMainWindow, Ui_ConsoleView):
    
    openPort = pyqtSignal(QString)
    
    def __init__(self, serial):
            QtGui.QMainWindow.__init__(self)
            self.setupUi(self)
            self.serial = serial
            self.serial.received.connect(self.handleData)
            self.setupComboPorts()
            self.buttonConnect.clicked.connect(self.handleButton)
            
    def setupComboPorts(self):
        ports = self.serial.getPorts()
        for port in ports:
            self.comboPorts.addItem(port[0])
            
            
    def handleButton(self):
        self.serial.openPort(self.comboPorts.currentText())
            
    def handleData(self, text):
        pass
        #self.textLog.append(text) 