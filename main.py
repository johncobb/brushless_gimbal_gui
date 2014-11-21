import Queue
import time
import Tkinter
import threading
import random
import Queue
from cpserial import CpSerial
from Tkinter import *

def buttonExit():
    # schedule the exit for 10ms
    root.after(100, exitApp())

    
def exitApp():
    serialThread.shutdown_thread()
    while(serialThread.isAlive()):
        continue
    
    exit()

def serialDataReceived(data):
    print 'Callback function modemDataReceived ', data
    #return
    
    strvar_status.set(data.strip('\r\n'))
    
    if data.count(':') < 2:
        return
    
    strvar_labelX.set(data.split(':')[1])
    strvar_labelY.set(data.split(':')[2])
    
    # (hack) not the best way to edit a text box
    #entry.delete(0, len(entry.get()))
    #entry.insert(0, data)
    

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
CANVAS_HEIGHT = 100
FRAME_HEIGHT = 300
    
if __name__ == '__main__':
    

    
    root = Tkinter.Tk()
    root.resizable(width=FALSE, height=FALSE)
    root.minsize(width=600, height=400)
    root.geometry("600x400")
    
    # StringVar requires root to be declare
    strvar_labelX = StringVar()
    strvar_labelX.set('--.---')
    strvar_labelY = StringVar()
    strvar_labelY.set('--.---')
    strvar_status = StringVar()
    strvar_status.set('')
    
   
    canvas = Canvas(root, width=SCREEN_WIDTH, height=CANVAS_HEIGHT)
    canvas.grid(row=0, column=0)
    
    
    line = canvas.create_line(0,50,SCREEN_WIDTH,50,fill='blue',tag='horizon')
    
    frame = Frame(root, width=SCREEN_WIDTH, height=FRAME_HEIGHT)
    frame.grid(row=1,column=0)
    
    labelX = Label(frame, width=5, justify=LEFT, padx=2)
    labelValX = Label(frame, width=5, justify=LEFT, padx=2, textvariable=strvar_labelX)
    labelY = Label(frame, width=5, justify=LEFT, padx=2)
    labelValY = Label(frame, width=5, justify=LEFT, padx=2, textvariable=strvar_labelY)
    labelStatus = Label(frame, width=5, justify=LEFT, padx=2)
    labelValStatus = Label(frame, width=20, justify=LEFT, padx=2, textvariable=strvar_status)
    
    labelX['text'] = 'Acc X:'
    labelY['text'] = 'Acc Y:'
    labelStatus['text'] = 'Status'
    
    labelX.grid(row=0, column=0)
    labelValX.grid(row=0, column=1)
    labelY.grid(row=0, column=2)
    labelValY.grid(row=0, column=3)
    labelStatus.grid(row=1, column=0)
    labelValStatus.grid(row=1, column=1, columnspan=3)
    

    buttonExit = Button(frame, text='Exit', command=buttonExit, justify=LEFT)
    buttonExit.grid(row=2,column=0)
    
    
    
    #entry = Entry(frame, bd=2)
    #entry.grid(row=3,column=0)

    serialThread = CpSerial(serialDataReceived)
    serialThread.start()
    root.mainloop()
    
    
 