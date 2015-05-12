import logging
from math import ceil
import time
from presentation.WorkInThread import WorkInThread

__author__ = 'abos'

logger = logging.getLogger(__name__)


class XyUiController:
    """
    Simulation of robot movement
    """

    def __init__(self, robotModel, sceneUpdateSig):
        self.moving = False
        self.moveThread = None
        self.robotModel = robotModel
        self.sceneUpdateSig = sceneUpdateSig

    def simulateMovement(self, dx, dy, absolute=False):
        """

        :param dx: relative destination
        :param dy: relative destination
        :param absolute:
        :return:
        """
        logger.info("simulateMovement")

        if self.moving and self.moveThread:
            logger.debug("simulateMovement: robot already moving, wait for stop")
            self.moving = False
            self.moveThread.join()

        # pos = self.prepareMove(pos,absolute)

        # if pos == None:
        #     return

        xDistance = abs(dx - self.robotModel.x)
        yDistance = abs(dy - self.robotModel.y)

        maxD = max(xDistance, yDistance) * 0.5
        maxStep = ceil(maxD)
        deltaStep = (xDistance / maxStep, yDistance / maxStep)
        logger.debug("maxD <%s>, maxStep <%s>, deltaStep <%s>, ", maxD, maxStep, deltaStep)

        self.moving = True

        self.moveThread = WorkInThread(self._moveStep, dx, dy, deltaStep)
        self.moveThread.setDaemon(True)
        self.moveThread.start()

    def _moveStep(self, dx, dy, deltaStep):
        while True:
            # approach to dx
            if abs(self.robotModel.x - dx) <= deltaStep[0]:
                self.robotModel.x = dx
            elif self.robotModel.x < dx:
                self.robotModel.x += deltaStep[0]
            elif self.robotModel.x > dx:
                self.robotModel.x -= deltaStep[0]

            # approach to dy
            if abs(self.robotModel.y - dy) <= deltaStep[1]:
                self.robotModel.y = dy
            elif self.robotModel.y < dy:
                self.robotModel.y += deltaStep[1]
            elif self.robotModel.y > dy:
                self.robotModel.y -= deltaStep[1]

            self.sceneUpdateSig.emit()
            time.sleep(0.02)

            if self.robotModel.x == dx and self.robotModel.y == dy:
                logger.debug("_moveStep: stopped at <%s, %s>", dx, dy)
                break

            if not self.moving:
                logger.debug("_moveStep: interrupted at <%s, %s>", dx, dy)
                break

        self.moving = False
