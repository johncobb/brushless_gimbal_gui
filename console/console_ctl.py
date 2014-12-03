import time
from PyQt4 import QtGui
from PyQt4 import QtCore 
from PyQt4.Qt import pyqtSignal, QString
from console.console_view import Ui_ConsoleView



class ConsoleCtl(QtGui.QMainWindow, Ui_ConsoleView):
    
    openPort = pyqtSignal(QString)
    
    def __init__(self, serial):
            QtGui.QMainWindow.__init__(self)
            self.setupUi(self)
            self.serial = serial
            self.serial.received.connect(self.handleData)
            self.serial.portStateChanged.connect(self.handlePortStateChanged)
            self.serial.portErrorOccured.connect(self.handlePortError)
            self.setupComboPorts()
            self.buttonConnect.clicked.connect(self.handleButton)
    
    def closeEvent(self, event):
        self.serial.stop_service()
        
        while(self.serial.running):
            print'waiting serial shutdown'
            time.sleep(.5)
        
        
    def setupComboPorts(self):
        ports = self.serial.getPorts()
        for port in ports:
            self.listConnect.addItem(port[0])
            
    def handleButton(self):

        # if we're open then we disconnect and setup ui for connecting
        if(self.serial.ser.isOpen()):
            self.buttonConnect.setText("Connect")
            self.listConnect.setEnabled(True)
            self.serial.closePort()

        else:
            self.buttonConnect.setText("Disconnect")
            self.listConnect.setEnabled(False)
            self.serial.changePort(self.listConnect.currentText().__str__())

            
    def handleData(self, data):
        #print data
        self.parseData(data)

        
    def handlePortStateChanged(self, msg):
        self.labelStatus.setText(msg)
        
    def handlePortError(self, msg):
        self.buttonConnect.setText("Connect")
        self.listConnect.setEnabled(True)
        self.textStatus.append(msg)
        
        
    def parseData(self, data):
        #self.labelStatus.setText(data)
        self.textStatus.append(data)
        print data
        
        if data.count(':') < 2:
            return
        
        self.labelX.setText(data.split(':')[1])
        self.labelY.setText(data.split(':')[2])