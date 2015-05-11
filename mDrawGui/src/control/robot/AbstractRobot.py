from PyQt4 import QtGui
from abc import ABCMeta, abstractmethod

DEBUG_NORMAL = 0
DEBUG_DEBUG = -2
DEBUG_ERR = -3
IDLE = 0
BUSYING = 1

class AbstractRobot(QtGui.QGraphicsItem):
    __metaclass__ = ABCMeta

    @abstractmethod
    def hello(self):
        pass