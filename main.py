import sys
import time
from PyQt4 import QtCore
from PyQt4.QtCore import *
from PyQt4 import QtGui
from cpserial import CpSerialThread
from console.console_ctl import ConsoleCtl

     
if __name__ == "__main__":
    
    app = QtGui.QApplication(sys.argv)
    serialThread = CpSerialThread()
    serialThread.start()
    
    console = ConsoleCtl(serialThread)
    console.show()
    
      
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
