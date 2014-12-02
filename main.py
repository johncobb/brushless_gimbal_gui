import sys
import time
from PyQt4 import QtCore
from PyQt4.QtCore import *
from PyQt4 import QtGui
from cpserial import CpSerialThread

from serial.tools import list_ports
from gimbal_ui import Ui_FormMain


def load_form():
    
    ports = list(list_ports.comports())
    
    for port in ports:
        print port
        f.listConnect.addItem(port[0])
    
    '''
    for i in range(10):
        f.listConnect.addItem('item %s' % (i+1))
    '''

def fnc_connect_clicked():
    
    print f.listConnect.currentText()
    print f.thread.running
    
    if f.thread.running == True:
        f.thread.stop_service()
        f.buttonConnect.setText('Connect')
    else:
        f.thread.set_port(str(f.listConnect.currentText()))
        f.buttonConnect.setText('Disconnect')
        f.thread.start()

        
    #f.thread.stop_service()
    print 'clicked'
    pass

def fnc_callback(data):
    f.labelStatus.setText(data)
    f.textStatus.append(data)
    print data
    
    if data.count(':') < 2:
        return
    
    f.labelX.setText(data.split(':')[1])
    f.labelY.setText(data.split(':')[2])
    
    
        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    f = Ui_FormMain()
    #new code
    f.thread = CpSerialThread()
    f.connect(f.thread, QtCore.SIGNAL('func_x(QString)'), fnc_callback)
    f.connect(f.buttonConnect, QtCore.SIGNAL('clicked()'), fnc_connect_clicked)
    #f.thread.start()
    #f.scrollStatus.setWidget(f.labelStatus)
    load_form()
    f.show()
    
    
    sys.exit(app.exec_())




            
                


'''
#command
pyuic4 filename.ui > filename.py
# Copy to constructor due to editor bug

class Ui_FormMain(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        
    def setupUi(self, FormMain):
'''
