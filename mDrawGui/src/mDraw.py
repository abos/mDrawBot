from PyQt4 import QtGui
import logging
import sys
from presentation.mDrawMainWindow import mDrawMainWindow

__author__ = 'abos'

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    logger.info("start application")

    app = QtGui.QApplication(sys.argv)
    ex = mDrawMainWindow()
    sys.exit(app.exec_())
