import logging
from PyQt4 import QtCore, QtGui

from PyQt4.QtCore import *

from control.robot.xy.RemoteXyRobot import RemoteXyRobot
from control.robot.xy.XyRobotModel import XyRobotModel
from presentation.AbstractRobotGui import AbstractRobotGui
from presentation.xy import XySetup
from presentation.xy.XySetupDialog import RobotSetupUI
from presentation.xy.XyUiController import XyUiController

logger = logging.getLogger(__name__)

#IDLE = 0
#BUSYING = 1
#motorSelectedStyle = "border: 1px solid rgb(67,67,67);\r\nborder-radius: 4px;\r\n"


class XYBot(QtGui.QGraphicsObject, AbstractRobotGui):
    """
    UI definition for XY robot. No simulation logic involved in this class.
    """

    def __init__(self, sceneUpdateSig, scene, ui, parent=None):
        super(XYBot, self).__init__()

        self.sceneUpdateSig = sceneUpdateSig

        self.robotModel = XyRobotModel()
        self.remoteRobot = RemoteXyRobot(self.robotModel)

        # UI objects
        self.scene = scene
        self.ui = ui

        self.uiController = XyUiController(self.robotModel, self.sceneUpdateSig)

        self.robotSetup = None

        # origin of robot
        # self.robotCent = None
        # initial params
        # self.width = 380
        # self.height = 310
        self.scaler = 1.0
        # self.x = 0
        # self.y = 0
        self.txtPtr = []
        # self.motoADir = 0
        #        self.motoBDir = 0
        #        self.laserBurnDelay = 0

        # origin of robot coordinate system (top left)
        self.origin = None

        #        self.xyorigin = None
        #        self.q = Queue.Queue()
        self.pRect = None
        #        self.moveList = None
        #        self.printing = False
        #        self.pausing = False
        #        self.laserMode = False
        #        self.lastx = 9999
        #        self.lasty = 9999
        self.ui.label.setText("X(mm)")
        self.ui.label_2.setText("Y(mm)")

    def boundingRect(self):
        return QRectF(0, 0, 100, 100)

    def initRobotCanvas(self):
        logger.info("initRobotCanvas");

        # calc origin of robot coordinate system / top left corner
        self.origin = ((self.scene.width() - self.robotModel.width) / 2,
                       (self.scene.height() - self.robotModel.height) / 2)

        if self.pRect is not None:
            self.scene.removeItem(self.pRect)
            for p in self.txtPtr:
                self.scene.removeItem(p)
            self.txtPtr = []

        pen = QtGui.QPen(QtGui.QColor(124, 124, 124))
        self.pRect = self.scene.addRect(self.origin[0], self.origin[1],
                                        self.robotModel.width,
                                        self.robotModel.height,
                                        pen)

        # add label to origin
        pTxt = self.scene.addText("O")
        cent = QPointF(self.origin[0] - 10, self.origin[1] + self.robotModel.height)
        pTxt.setPos(cent)
        pTxt.setDefaultTextColor(QtGui.QColor(124, 124, 124))
        self.txtPtr.append(pTxt)

        # add label to y axis
        pTxt = self.scene.addText("Y")
        cent = QPointF(self.origin[0] - 10, self.origin[1] - 10)
        pTxt.setPos(cent)
        pTxt.setDefaultTextColor(QtGui.QColor(124, 124, 124))
        self.txtPtr.append(pTxt)

        # add label to x axis
        pTxt = self.scene.addText("X")
        cent = QPointF(self.origin[0] + self.robotModel.width,
                       self.origin[1] + self.robotModel.height)
        pTxt.setPos(cent)
        pTxt.setDefaultTextColor(QtGui.QColor(124, 124, 124))
        self.txtPtr.append(pTxt)

        # fill info box
        self.ui.labelScale.setText(str(self.scaler))

    def robotGoHome(self):
        self.remoteRobot.goHome()
        self.sceneUpdateSig.emit()

    def moveTo(self, position):
        """

        :param position: absolute position in canvas
        :return:
        """
        logger.info("moveTo <%s> from relative <%s, %s>", position, self.robotModel.x, self.robotModel.y)

        relativeX = position.x() - self.origin[0]
        relativeY = self.robotModel.height - (position.y() - self.origin[1])

        logger.debug("moveTo relative <%s, %s>", relativeX, relativeY)

        self.remoteRobot.moveTo(relativeX, relativeY)
        self.uiController.simulateMovement(relativeX, relativeY)


    # def parseEcho(self,msg):
    # if "M10" in msg:
    # tmp = msg.split()
    # if tmp[1]!="XY": return
    #
    # self.width = float(tmp[2])
    # self.height = float(tmp[3])
    #
    # if tmp[6]=="A0":
    # self.motoADir = 0
    # else:
    #             self.motoADir = 1
    #         if tmp[7]=="B0":
    #             self.motoBDir = 0
    #         else:
    #             self.motoBDir = 1
    #         self.initRobotCanvas()
    #         self.robotState = IDLE
    #     elif "M11" in msg:
    #         t = msg.split()
    #         self.robotSetup.ui.label_8.setText("X-:%s X+:%s Y-:%s Y+:%s " %(t[1],t[2],t[3],t[4]))


    def paint(self, painter, option, widget=None):
        logger.info("paint")

        painter.setBrush(QtCore.Qt.darkGray)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # -- calc position of robot
        x = self.origin[0] + self.robotModel.x
        y = self.origin[1] + self.robotModel.height - self.robotModel.y

        painter.drawText(x - 30, y + 10,
                         "(%.2f, %.2f)" % (self.robotModel.x, self.robotModel.y))

        # -- draw cross hairs
        pen = QtGui.QPen(QtGui.QColor(124, 124, 124))
        painter.setBrush(QtCore.Qt.darkGray)
        painter.setPen(pen)
        painter.drawLine(self.origin[0], y, self.origin[0] + self.robotModel.width, y)
        painter.drawLine(x, self.origin[1], x, self.origin[0] + self.robotModel.height)

        # -- draw position of robot
        pen = QtGui.QPen(QtGui.QColor(0, 169, 231))
        painter.setBrush(QtGui.QColor(0, 169, 231))
        painter.setPen(pen)
        painter.drawEllipse(-5 + x, -5 + y, 10, 10)

        # -- fill upper right info boxes
        self.ui.labelXpos.setText("%.2f" % self.robotModel.x)
        self.ui.labelYpos.setText("%.2f" % self.robotModel.y)

    #
    # def moveOverList(self):
    #     if self.moveList == None: return
    #     moveLen = len(self.moveList)
    #     moveCnt = 0
    #     for move in self.moveList:
    #         #loop for all points
    #         for i in range(len(move)):
    #             p = move[i]
    #             x=(p[0]-self.origin[0])
    #             y=(p[1]-self.origin[1]-self.height)
    #             print "goto",x,-y
    #             try:
    #                 if self.printing == False:
    #                     return
    #                 elif self.pausing == True:
    #                     while self.pausing==True:
    #                         time.sleep(0.5)
    #                 auxDelay = 0
    #                 if self.laserMode:
    #                     if i>0:
    #                         auxDelay = self.laserBurnDelay*1000
    #                     elif i==0:
    #                         self.M4(self.laserPower,0.0) # turn laser power down when perform transition
    #                         self.q.get()
    #                 self.G1(x,-y,auxdelay = auxDelay)
    #                 self.x = x
    #                 self.y = y
    #                 self.q.get()
    #                 if self.laserMode and i==0:
    #                     self.M4(self.laserPower) # turn laser power back to set value
    #                     self.q.get()
    #                 if not self.laserMode and i==0:
    #                     self.M1(self.penDownPos)
    #                     self.q.get()
    #                     time.sleep(0.2)
    #             except:
    #                 pass
    #         if not self.laserMode:
    #             self.M1(self.penUpPos)
    #             self.q.get()
    #             time.sleep(0.2)
    #         moveCnt+=1
    #         self.robotSig.emit("pg %d" %(int(moveCnt*100/moveLen)))
    #     self.printing = False
    #     self.robotSig.emit("done")

    # def printPic(self):
    #     logger.info("printPic");
    #
    #     #update pen servo position
    #     #update pen servo position
    #     mStr = str(self.ui.linePenUp.text())
    #     self.penUpPos = int(mStr.split()[1])
    #     mStr = str(self.ui.linePenDown.text())
    #     self.penDownPos = int(mStr.split()[1])
    #
    #     while not self.q.empty():
    #         self.q.get()
    #
    #     return
    #     self.printing = True
    #     self.pausing = False
    #     self.moveListThread = WorkInThread(self.moveOverList)
    #     self.moveListThread.setDaemon(True)
    #     self.moveListThread.start()
    #
    # def stopPrinting(self):
    #     self.printing = False
    #     self.pausing = False
    #
    # def pausePrinting(self, v):
    #     self.pausing = v

    def showSetup(self):
        self.robotSetup = RobotSetupUI(XySetup.Ui_Form, self)
