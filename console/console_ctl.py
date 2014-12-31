import time
import math
from PyQt4 import QtCore, QtGui, QtOpenGL
from PyQt4.Qt import pyqtSignal, QString

from console.console_view import Ui_ConsoleView
from console.gl_widget  import GLWidget

try:
    from OpenGL import GL
except ImportError:
    print 'PyOpenGL must be installed to run this application'



class ConsoleCtl(QtGui.QMainWindow, Ui_ConsoleView):
    
    PI = 3.14159265359
    
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
            self.buttonReset.clicked.connect(self.handleResetButton)
            self.glWidget = GLWidget()
            self.glLayout.addWidget(self.glWidget)
    
    def closeEvent(self, event):
        self.serial.stop_service()
        
        while(self.serial.running):
            print'waiting serial shutdown'
            time.sleep(.5)
        
        
    def setupComboPorts(self):
        ports = self.serial.getPorts()
        for port in ports:
            self.listConnect.addItem(port[0])
    
    def handleResetButton(self):
        self.glWidget.setXRotation(0)
        self.glWidget.setYRotation(0)
        self.glWidget.setZRotation(0)
        
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

         # TODO: cleanup output from gimbal so parsing is easier
        data = data.__str__().strip('roll/pitch/yaw').strip()
        
        #NEW TEMPORARY PARSE
        if(data.count(':') <> 2):
            return
        
        result = data.split(':')
        
        print result
        
        if math.isnan(float(result[0])):
            return
        if math.isnan(float(result[1])):
            return
        if math.isnan(float(result[2])):
            return
        
        roll = float(result[0])
        pitch = float(result[1])
        yaw = float(result[2])

        self.labelPitch.setText(pitch.__str__())
        self.labelRoll.setText(roll.__str__())
        self.labelYaw.setText(yaw.__str__())
        
        self.glWidget.setXRotation(pitch)
        self.glWidget.setZRotation(roll)
        #self.glWidget.setYRotation(yaw)

        


        '''
        if data.count(':') < 14:
            return
        result = data.split(':')
        
        accelX = float(result[0])
        accelY = float(result[1])
        accelZ = float(result[2])
        gravityX = float(result[3])
        gravityY = float(result[4])
        gravityZ = float(result[5])
        magX = int(result[6])
        magY = int(result[7])
        magZ = int(result[8])
        quatX = float(result[9])
        quatY = float(result[10])
        quatZ = float(result[11])
        pitch = float(result[12])
        roll = float(result[13])
        yaw = float(result[14])

 
        self.labelAccelX.setText(accelX.__str__())
        self.labelAccelY.setText(accelY.__str__())
        self.labelAccelZ.setText(accelZ.__str__())
        self.labelGravityX.setText(gravityX.__str__())
        self.labelGravityY.setText(gravityY.__str__())
        self.labelGravityZ.setText(gravityZ.__str__())
        self.labelMagX.setText(magX.__str__())
        self.labelMagY.setText(magY.__str__())
        self.labelMagZ.setText(magZ.__str__())
        self.labelQuatX.setText(quatX.__str__())
        self.labelQuatY.setText(quatY.__str__())
        self.labelQuatZ.setText(quatZ.__str__())
        self.labelPitch.setText(pitch.__str__())
        self.labelRoll.setText(roll.__str__())
        self.labelYaw.setText(yaw.__str__())
        '''
        
        
