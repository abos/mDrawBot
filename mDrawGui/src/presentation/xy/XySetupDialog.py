__author__ = 'abos'

from PyQt4.QtCore import *
from PyQt4 import QtCore, QtGui


class RobotSetupUI(QtGui.QWidget):
    def __init__(self,uidialog,robot):
        super(RobotSetupUI, self).__init__()
        self.ui = uidialog()
        self.ui.setupUi(self)
        self.robot = robot
        self.setWindowTitle('XY Setup')
        self.updateUI()
        self.ui.motoA_CK.mousePressEvent = self.setMotorAck
        self.ui.motoA_CCK.mousePressEvent = self.setMotorAcck
        self.ui.motoB_CK.mousePressEvent = self.setMotorBck
        self.ui.motoB_CCK.mousePressEvent = self.setMotorBcck
        self.ui.btnOk.clicked.connect(self.applySetup)
        self.show()
        self.updating = True
        self.moveThread = WorkInThread(self.updateEndStopThread)
        self.moveThread.setDaemon(False)
        self.moveThread.start()

    def updateEndStopThread(self):
        while self.updating:
            time.sleep(0.2)
            self.robot.M11()

    def closeEvent(self, event):
        self.updating = False

    def updateUI(self):
        self.ui.lineWidth.setText(str(self.robot.width))
        self.ui.lineHeight.setText(str(self.robot.height))
        if self.robot.motoADir == 0:
            self.ui.motoA_CK.setStyleSheet(motorSelectedStyle)
            self.ui.motoA_CCK.setStyleSheet("")
        else:
            self.ui.motoA_CK.setStyleSheet("")
            self.ui.motoA_CCK.setStyleSheet(motorSelectedStyle)
        if self.robot.motoBDir == 0:
            self.ui.motoB_CK.setStyleSheet(motorSelectedStyle)
            self.ui.motoB_CCK.setStyleSheet("")
        else:
            self.ui.motoB_CK.setStyleSheet("")
            self.ui.motoB_CCK.setStyleSheet(motorSelectedStyle)

    def applySetup(self):
        self.robot.width = float(str(self.ui.lineWidth.text()))
        self.robot.height = float(str(self.ui.lineHeight.text()))
        self.robot.M5()
        self.hide()
        self.robot.initRobotCanvas()

    def setMotorAck(self,event):
        self.robot.motoADir = 0
        self.updateUI()

    def setMotorAcck(self,event):
        self.robot.motoADir = 1
        self.updateUI()

    def setMotorBck(self,event):
        self.robot.motoBDir = 0
        self.updateUI()

    def setMotorBcck(self,event):
        self.robot.motoBDir = 1
        self.updateUI()

