import sys
import time
import serial
from PyQt4 import QtGui
from PyQt4 import QtCore 
from PyQt4.Qt import pyqtSignal, QString
from serial.tools import list_ports
from cpdefs import CpDefs

class CpSerialThread(QtCore.QThread):
    
    
    received = pyqtSignal(QString)
    portStateChanged = pyqtSignal(QString)
    portErrorOccured = pyqtSignal(QString)
    
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self)
        self.exiting = False
        self.sig_stop = False
        self.sig_portchange = False
        self.sig_portclose = False
        self.port_name = ''
        self.ser = serial.Serial()
        self.initPort()
        self.running = False
        
    def __del__(self):
        self.sig_stop = True
        self.exiting = True
        self.wait()
        
    def initPort(self):
        self.ser.port = CpDefs.SerialPort
        self.ser.baudrate = CpDefs.SerialBaudrate
        self.ser.parity = 'N'
        self.ser.stopbits = 1
        self.ser.bytesize = 8
        self.ser.xonxoff = 0
        self.ser.rtscts = 0
        
    
    def getPorts(self): 
        return list(list_ports.comports())
    
    def changePort(self, port):
        self.port_name = port
        self.sig_portchange = True
        print 'change port'
        
    def closePort(self):
        self.sig_portclose = True
        
    def handle_close_port(self):
        # reset the flag
        self.sig_portclose = False
        try:
            if(self.ser.isOpen()):
                self.ser.close()
                self.portStateChanged.emit('port closed') 
        except serial.SerialException, se:
            print se
            self.portErrorOccured.emit(str(se)) 
        except serial.SerialTimeoutException, sto:
            print sto
            self.portErrorOccured.emit(str(sto)) 
        except Exception, e:
            print e
            self.portErrorOccured.emit(str(e))
        
        
    def handle_set_port(self):
        
        # reset the flag
        self.sig_portchange = False

        try:
            # sanity check here
            if(self.ser.isOpen()):
                self.ser.close()
                # allow port to settle
                time.sleep(.1)
            
            # change the port and reopen
            self.ser.port = self.port_name
            self.ser.open()
            
            self.portStateChanged.emit(self.port_name)
        except serial.SerialException, se:
            print se
            self.portErrorOccured.emit(str(se)) 
        except serial.SerialTimeoutException, sto:
            print sto
            self.portErrorOccured.emit(str(sto)) 
        except Exception, e:
            print e
            self.portErrorOccured.emit(str(e)) 


    def start_service(self):
        
        self.running = True
        print 'starting service...'
        
        tmp_buffer = ''
        
        while self.sig_stop == False:

            # handle changing of port
            if(self.sig_portchange):
                print 'change port'
                self.handle_set_port()
                tmp_buffer = ''
            
            # handle closing of port
            if(self.sig_portclose):
                print 'close port'
                self.handle_close_port()
                tmp_buffer = ''
                
            # wait for user to signal to open port
            if (self.ser.isOpen() == False):
                time.sleep(.5)
                continue
            
            # handle incoming data
            while (self.ser.inWaiting() > 0):
                #print 'modem has data!!!'
                tmp_char = self.ser.read(1)
                if(tmp_char == '\r'):
                    # signal data received
                    self.received.emit(tmp_buffer.strip('\r\n'))
                    tmp_buffer= ''
                else:
                    tmp_buffer += tmp_char
            
            time.sleep(.005)
            
        self.running = False
        
        print 'service stopped!'

    def stop_service(self):
        self.sig_stop = True
        
        if(self.ser.isOpen()):
            self.ser.close()
        print 'stopping service...'
        
        
    def run(self):
        self.start_service()