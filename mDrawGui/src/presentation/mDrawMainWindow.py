from PyQt4.QtCore import *

# noinspection PyUnresolvedReferences
import time
import images_rc
import logging

from control.communication.serial import SerialCom
from presentation.RobotGui import *
from presentation.WorkInThread import WorkInThread
from presentation.xy import XYRobotGui

__author__ = 'abos'

logger = logging.getLogger(__name__)


class mDrawMainWindow(QtGui.QWidget):
    sceneUpdateSig = pyqtSignal()
    robotSig = pyqtSignal(str)

    def __init__(self):
        super(mDrawMainWindow, self).__init__()
        logger.info("init")

        self.scene = None
        self.ui = None
        self.robotGui = None

        self.initUI()
        logger.info("init finished")


    def initUI(self):
        logger.info("initUI")

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.refreshCom()

        # init scene
        rect = QRectF(self.ui.graphicsView.rect())
        self.scene = QtGui.QGraphicsScene(rect)
#        item = QtGui.QGraphicsEllipseItem(75, 10, 60, 40)
        self.ui.graphicsView.setScene(self.scene)
        self.ui.progressBar.setVisible(False)
        self.ui.labelPic.setVisible(False)

        # mouse movement
        self.ui.graphicsView.mousePressEvent = self.graphMouseClick
        self.ui.graphicsView.mouseMoveEvent = self.graphMouseMove
        self.ui.graphicsView.mouseReleaseEvent = self.graphMouseRelease

        #fix the 1 pix margin of graphic view
        rcontent = self.ui.graphicsView.contentsRect();
        self.ui.graphicsView.setSceneRect(0, 0, rcontent.width(), rcontent.height());

        self.initGraphView()
        self.setWindowTitle('mDraw')
        self.show()

        # connect scene.update to sceneUpdateSig
        self.sceneUpdateSig.connect(self.scene.update)

        # start refresh thread
        self.refreshThread = WorkInThread(self.sceneRefresh)
        self.refreshThread.setDaemon(True)
        self.refreshThread.start()


    def initGraphView(self):
        logger.info("initGraphView")

        # create new robot UI
        self.robotGui = XYRobotGui.XYBot(self.scene, self.ui)

        scene = self.ui.graphicsView.scene()
        # remove graph reference first
        # self.ptrPicRect = None
        # self.pic = None
        scene.clear()

        rc = scene.sceneRect()
        cent = QPointF(rc.width() / 2, rc.height() / 2 + 100)
        #        self.robotCent = cent
        #        self.robot.robotCent =(cent.x(),cent.y())

        logger.debug("initGraphView: robot center <%s>", cent)
        #print "rc",cent

        scene.addItem(self.robotGui)

        self.robotGui.initRobotCanvas()

    #        self.robot.setPos(cent)

    def sceneRefresh(self):
        logger.info("sceneRefresh")

        while True:
            self.sceneUpdateSig.emit()
            time.sleep(0.2)

        logger.debug("sceneRefresh: finished")


    def refreshCom(self):
        logger.info("refreshCom")

        self.commList = {}
        self.ui.portCombo.clear()
        serPorts = SerialCom.serialList()

        for s in serPorts:
            self.commList[s] = "COM"
            self.ui.portCombo.addItem(s)
            #self.socket.refresh()

    def graphMouseRelease(self, event):
        logger.info("graphMouseRelease")

        self.robotGui.moveTo(event.pos())

        # else:
        #     if self.mouseOverPic:
        #         w = self.picWidth
        #         h = self.picHeight
        #         pos = event.pos()
        #         px, py = pos.x(), pos.y()
        #         x = px - self.rectBias[0]
        #         y = py - self.rectBias[1]
        #         self.tempPicRect.setRect(x, y, w, h)
        #         self.scene.removeItem(self.tempPicRect)
        #         self.tempPicRect = None
        #         self.picX0 = x
        #         self.picY0 = y
        #         self.updatePic()
        #     elif self.mouseResizePic:
        #         x = self.picX0
        #         y = self.picY0
        #         pos = event.pos()
        #         rect = self.tempPicRect.rect()
        #         w = rect.width()
        #         h = rect.height()
        #         self.tempPicRect.setRect(x, y, w, h)
        #         self.scene.removeItem(self.tempPicRect)
        #         self.tempPicRect = None
        #         self.picWidth = w
        #         self.picHeight = h
        #         self.updatePic()


    def graphMouseMove(self, event):
        logger.info("graphMouseMove")

        # if self.tempPicRect != None:
        #     if self.mouseOverPic:
        #         w = self.picWidth
        #         h = self.picHeight
        #         pos = event.pos()
        #         px, py = pos.x(), pos.y()
        #         self.tempPicRect.setRect(px - self.rectBias[0], py - self.rectBias[1], w, h)
        #     elif self.mouseResizePic:
        #         x = self.picX0
        #         y = self.picY0
        #         ratio = self.picHeight / self.picWidth
        #         pos = event.pos()
        #         px, py = pos.x(), pos.y()
        #         w = px - x
        #         if w < 10:
        #             w = 10
        #         #h = py-y
        #         h = w * ratio  # fix svg w/h ratio
        #         #self.ui.labelPic.setText(" w: %d mm\n h: %d mm" %(w,h))
        #         self.ui.lineSvgWidth.setText("%.2f" % w)
        #         self.ui.lineSvgHeight.setText("%.2f" % h)
        #         # let label follow mouse positions
        #         self.ui.labelPic.move(QPoint(x + w + 20, y + h + 20))
        #         self.tempPicRect.setRect(x, y, w, h)
        # else:  # restore mouse icon
        #     pos = event.pos()
        #     x = self.picX0
        #     y = self.picY0
        #     w = self.picWidth
        #     h = self.picHeight
        #     px, py = pos.x(), pos.y()
        #     if px > x and px < (x + w) and py > y and py < (y + h):
        #         if self.mouseOverPic == False:
        #             QtGui.QApplication.setOverrideCursor(QtGui.QCursor(Qt.SizeAllCursor))
        #             self.mouseOverPic = True
        #     elif px > (x + w) and px < (x + w + 5) and py > (y + h) and py < (y + h + 5):
        #         if self.mouseResizePic == False:
        #             QtGui.QApplication.setOverrideCursor(QtGui.QCursor(Qt.SizeFDiagCursor))
        #             self.mouseResizePic = True
        #     else:
        #         if self.mouseOverPic == True or self.mouseResizePic == True:
        #             QtGui.QApplication.restoreOverrideCursor()
        #             QtGui.QApplication.restoreOverrideCursor()
        #             self.mouseOverPic = False
        #             self.mouseResizePic = False


    def graphMouseClick(self, event):
        logger.info("graphMouseClick")

        # if self.ptrPicRect == None: return
        # pos = event.pos()
        # x = self.picX0
        # y = self.picY0
        # w = self.picWidth
        # h = self.picHeight
        # px, py = pos.x(), pos.y()
        # if self.mouseOverPic or self.mouseResizePic:
        #     pen = QtGui.QPen(QtGui.QColor(0, 169, 231), 3, QtCore.Qt.DashDotLine)
        #     self.tempPicRect = self.scene.addRect(x, y, w, h, pen)
        #     self.rectBias = (px - x, py - y)
