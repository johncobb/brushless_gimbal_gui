import sys
import math
from PyQt4 import QtCore, QtGui, QtOpenGL

try:
    from OpenGL import GL
    from OpenGL import GLU
    
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
            "PyOpenGL must be installed to run this example.")


class GLWidget(QtOpenGL.QGLWidget):
    xRotationChanged = QtCore.pyqtSignal(int)
    yRotationChanged = QtCore.pyqtSignal(int)
    zRotationChanged = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)

        self.object = 0
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0

        self.lastPos = QtCore.QPoint()

        self.trolltechGreen = QtGui.QColor.fromCmykF(0.40, 0.0, 1.0, 0.0)
        self.trolltechPurple = QtGui.QColor.fromCmykF(0.39, 0.39, 0.0, 0.0)

    def minimumSizeHint(self):
        return QtCore.QSize(50, 50)

    def sizeHint(self):
        return QtCore.QSize(400, 400)

    def setXRotation(self, angle):
        #angle = self.normalizeAngle(angle)
        if angle != self.xRot:
            self.xRot = angle
            self.xRotationChanged.emit(angle)
            self.updateGL()
            
        #print 'x angle:', angle

    def setYRotation(self, angle):
        # set the Pitch Axis
        if angle != self.yRot:
            self.yRot = angle
            self.yRotationChanged.emit(angle)
            self.updateGL()

    def setZRotation(self, angle):
        # set the Roll Axis
        if angle != self.zRot:
            self.zRot = angle
            self.zRotationChanged.emit(angle)
            self.updateGL()

    def initializeGL(self):
        self.qglClearColor(self.trolltechPurple.dark())
        self.object = self.makeObject()
        GL.glShadeModel(GL.GL_FLAT)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_CULL_FACE)

    def paintGL(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glLoadIdentity()
        
        self.drawGuides()

        GL.glTranslated(0.0, 0.0, -1.0)
        GL.glRotated(self.xRot, 1.0, 0.0, 0.0)
        GL.glRotated(self.yRot, 0.0, 1.0, 0.0)
        GL.glRotated(self.zRot, 0.0, 0.0, 1.0)
        GL.glCallList(self.object)
        

    def drawGuides(self):
        GL.glBegin(GL.GL_LINES)
        #x line
        GL.glColor3f(1, 0, 0)
        GL.glVertex3f(-3, -2, 0)
        GL.glVertex3f(-1, -2, 0)
        
        #y line
        GL.glColor3f(0, 0, 1)
        GL.glVertex3f(-3, -2, 0)
        GL.glVertex3f(-3, 0, 0)
        
        #z line
        GL.glColor3f(0, 1, 0)
        GL.glVertex3f(-3, -2, 0)
        GL.glVertex3f(-3, -2, -2)
        GL.glEnd()
        
    def resizeGL(self, width, height):
        side = min(width, height)
        if side < 0:
            return

        GL.glViewport((width - side) / 2, (height - side) / 2, side, side)

        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        #GL.glOrtho(-0.5, +0.5, +0.5, -0.5, 4.0, 15.0)
        #GL.glOrtho(-30.0, 30.0, -30.0, 30.0, -30.0, 30.0)
        #GL.glOrtho(-7.5, 7.5, -7.5, 7.5, -7.5, 7.5)
        GL.glOrtho(-3.5, 3.5, -3.5, 3.5, -3.5, 3.5)
        

        GL.glMatrixMode(GL.GL_MODELVIEW)
        

        

    def mousePressEvent(self, event):
        self.lastPos = event.pos()

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() & QtCore.Qt.LeftButton:
            self.setXRotation(self.xRot + 1 * dy)
            self.setYRotation(self.yRot + 1 * dx)
        elif event.buttons() & QtCore.Qt.RightButton:
            self.setXRotation(self.xRot + 1 * dy)
            self.setZRotation(self.zRot + 1 * dx)

        self.lastPos = event.pos()

    def makeObject(self):
        genList = GL.glGenLists(1)
        GL.glNewList(genList, GL.GL_COMPILE)


        
        GL.glBegin(GL.GL_QUADS)

        GL.glColor3f(0.0,1.0,0.0)
        GL.glVertex3f( 1.0, 1.0,-1.0)
        GL.glVertex3f(-1.0, 1.0,-1.0)
        GL.glVertex3f(-1.0, 1.0, 1.0)
        GL.glVertex3f( 1.0, 1.0, 1.0) 
 
        GL.glColor3f(1.0,0.0,0.0)
        GL.glVertex3f( 1.0,-1.0, 1.0)
        GL.glVertex3f(-1.0,-1.0, 1.0)
        GL.glVertex3f(-1.0,-1.0,-1.0)
        GL.glVertex3f( 1.0,-1.0,-1.0) 
 
        GL.glColor3f(0.0,1.0,0.0)
        GL.glVertex3f( 1.0, 1.0, 1.0)
        GL.glVertex3f(-1.0, 1.0, 1.0)
        GL.glVertex3f(-1.0,-1.0, 1.0)
        GL.glVertex3f( 1.0,-1.0, 1.0)
 
        GL.glColor3f(1.0,1.0,0.0)
        GL.glVertex3f( 1.0,-1.0,-1.0)
        GL.glVertex3f(-1.0,-1.0,-1.0)
        GL.glVertex3f(-1.0, 1.0,-1.0)
        GL.glVertex3f( 1.0, 1.0,-1.0)
 
        GL.glColor3f(0.0,0.0,1.0)
        GL.glVertex3f(-1.0, 1.0, 1.0) 
        GL.glVertex3f(-1.0, 1.0,-1.0)
        GL.glVertex3f(-1.0,-1.0,-1.0) 
        GL.glVertex3f(-1.0,-1.0, 1.0) 
 
        GL.glColor3f(1.0,0.0,1.0)
        GL.glVertex3f( 1.0, 1.0,-1.0) 
        GL.glVertex3f( 1.0, 1.0, 1.0)
        GL.glVertex3f( 1.0,-1.0, 1.0)
        GL.glVertex3f( 1.0,-1.0,-1.0)
        
        
        GL.glEnd()
        GL.glEndList()

        return genList