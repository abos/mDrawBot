import logging
from math import ceil
import time

__author__ = 'abos'

logger = logging.getLogger(__name__)


class XyRobotLogic:
    """
    implements main logic to control robot
    """

    def prepareMove(self, target, robotModel, absolute=False):
        if not absolute:
            target = (target.x(), -target.y())
            target = (target[0] + robotModel.robotCent[0] - robotModel.origin[0],
                      -target[1] - robotModel.origin[1] + robotModel.robotCent[1] - robotModel.height)
        else:
            # position set by user
            target = (target.x(), target.y())

        dx = target[0] - robotModel.x
        dy = target[1] - robotModel.y

        # distance = sqrt(dx * dx + dy * dy)

        maxD = max(abs(dx), abs(dy)) * 0.5
        maxStep = ceil(maxD)

        #        self.deltaStep = (dx / maxStep, dy / maxStep)
        #        self.maxStep = maxStep

        x = target[0]
        y = -target[1]

        logger.debug("prepareMove: x/y <%s, %s>, maxStep <%s>", x, y, maxStep)

        if x < 0 or x > self.width or y < 0 or y > self.height:
            logger.debug("prepareMove: desired position is outside area")
            return None

        return x, y


    def moveOverList(self, remoteRobot):
        if self.moveList == None: return

        moveLen = len(self.moveList)
        moveCnt = 0

        for move in self.moveList:
            # loop for all points
            for i in range(len(move)):
                p = move[i]

                x = (p[0] - self.origin[0])
                y = (p[1] - self.origin[1] - self.height)

                print "goto", x, -y

                try:
                    if not self.printing:
                        return

                    while self.pausing:
                        time.sleep(0.5)

                    auxDelay = 0

                    if self.laserMode:
                        if i > 0:
                            auxDelay = self.laserBurnDelay * 1000
                        elif i == 0:
                            self.M4(self.laserPower, 0.0)  # turn laser power down when perform transition
                            self.q.get()

                    remoteRobot.moveTo(x, -y, auxdelay=auxDelay)

                    self.x = x
                    self.y = y

                    self.q.get()

                    if self.laserMode and i == 0:
                        self.M4(self.laserPower)  # turn laser power back to set value
                        self.q.get()
                    if not self.laserMode and i == 0:
                        self.M1(self.penDownPos)
                        self.q.get()
                        time.sleep(0.2)
                except:
                    pass
            if not self.laserMode:
                self.M1(self.penUpPos)
                self.q.get()
                time.sleep(0.2)

            moveCnt += 1
            self.robotSig.emit("pg %d" % (int(moveCnt * 100 / moveLen)))
        self.printing = False
        self.robotSig.emit("done")
