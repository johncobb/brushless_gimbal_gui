from PyQt4 import QtGui, QtCore
import sys
import time
import serial
from serial.tools import list_ports
from cpdefs import CpDefs

class CpSerialThread(QtCore.QThread):
    
    received = pyqtSignal(QString)
    
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self)
        self.ser = serial.Serial(CpDefs.SerialPort, baudrate=CpDefs.SerialBaudrate, parity='N', stopbits=1, bytesize=8, xonxoff=0, rtscts=0)
        self.exiting = False
        self.sig_stop = False
        self.running = False
        
    def __del__(self):
        self.sig_stop = True
        self.exiting = True
        self.wait()
    
    def getPorts(self): 
        return list(list_ports.comm_ports())
    
    def set_port(self, port):
        # stop the service
        if(self.running):
            self.stop_service()
            # wait for service to stop
            while(self.running):
                time.sleep(.1)
            
        self.ser = serial.Serial(port, baudrate=CpDefs.SerialBaudrate, parity='N', stopbits=1, bytesize=8, xonxoff=0, rtscts=0)
        #self.start_service()
        
    def start_service(self):
        
        self.running = True
        print 'starting service...'
        
        tmp_buffer = ''
        
        if(self.ser.isOpen()):
            self.ser.close()
        
        self.ser.open()
        
        while self.sig_stop == False:
            #print 'modem has data!!!'
            tmp_char = self.ser.read(1)
            if(tmp_char == '\r'):

                #print 'received ', tmp_buffer
                self.emit(QtCore.SIGNAL('func_x(QString)'), tmp_buffer.strip('\r\n'))
                tmp_buffer= ""
            else:
                tmp_buffer += tmp_char
            
            time.sleep(.005)
            
        self.running = False
        
        '''
        i = 0
        while self.sig_stop == False:
            time.sleep(1)
            print 'emitting...'
            self.emit(QtCore.SIGNAL('func_x(QString)'), str(i))
            i = i + 1
        '''
        print 'service stopped!'

    def stop_service(self):
        self.sig_stop = True
        
        if(self.ser.isOpen()):
            self.ser.close()
        print 'stopping service...'
        
        
    def run(self):
        self.start_service()
                
class MainApp(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        
        #Setup UI
        self.layout = QtGui.QHBoxLayout(self)
        self.label = QtGui.QLabel("Counter")
        self.button = QtGui.QPushButton('Exit')
        self.connect(self.button, QtCore.SIGNAL('clicked()'), self.buttonPressed)
        self.setupUi()
        # Setup Thread
        self.thread = CpSerialThread()
        self.connect(self.thread, QtCore.SIGNAL('func_x(QString)'), self.fnc_callback)
        self.thread.start()
        

    def setupUi(self):
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.button)
    
    def buttonPressed(self):
        self.thread.stop_service()
        
    def fnc_callback(self, count):
        self.label.setText(count)
        print count        
        
if __name__ == '__main__':
    
    app = QtGui.QApplication(sys.argv)
    form = MainApp()
    form.show()
    sys.exit(app.exec_())