import logging
from control.EventHook import EventHook
from control.robot.xy.XyRobotModel import XyRobotModel

__author__ = 'abos'

logger = logging.getLogger(__name__)


class RemoteXyRobot:
    """
    Class to control remote robot. No algorithmic logic is involved in this class. This is
     slim communication adapter.
    """

    def __init__(self, remoteAdapter):
        self.remoteAdapter = remoteAdapter
        self.remoteAdapter.register(self)

        self.robotModel = XyRobotModel()
        self.onChangeRobot = EventHook()


    def registerOnChangeRobot(self, listener):
        logger.info("registerOnChangeRobot")

        self.onChangeRobot += listener


    def goHome(self):
        """
        send robot home
        :return:
        """
        logger.info("goHome")

        if self.robotModel.state != IDLE:
            logger.debug("goHome: robot not idle, ignore command ")
            return

        self.remoteAdapter.sendCmd("G28\n")

        self.robotModel.x = 0
        self.robotModel.y = 0


    # def moveTo(self, pos, absolute=False):
    #     logger.info("moveTo")
    #
    #     # if self.moving:
    #     #            self.moving = False
    #     #            self.moveThread.join()
    #
    #     pos = self.prepareMove(pos, absolute)
    #
    #     if pos == None:
    #         return
    #
    #     self.G1(pos[0], pos[1])
    #     self.moving = True
    #     self.moveThread = WorkInThread(self.moveStep)
    #     self.moveThread.setDaemon(True)
    #     self.moveThread.start()


    def moveTo(self, x, y, feedrate=0, auxdelay=None):
        logger.info("moveTo")

        if self.robotState != IDLE: return

        cmd = "G1 X%.2f Y%.2f" % (x, y)

        if auxdelay != None:
            cmd += " A%d" % (auxdelay)

        cmd += '\n'

        self.robotModel.state = BUSYING
        self.remoteAdapter.sendCmd(cmd)


    def movePen(self, pos):
        logger.info("M1")

        if self.robotState != IDLE: return

        cmd = "M1 %d" % (pos)
        cmd += '\n'

        self.robotModel.state = BUSYING
        self.remoteAdapter.sendCmd(cmd)


    def M3(self, auxdelay):  # aux delay
        if self.robotState != IDLE: return
        cmd = "M3 %d\n" % (auxdelay)

        self.robotModel.state = BUSYING
        self.remoteAdapter.sendCmd(cmd)


    def setupLaserPower(self, laserPower, rate=1):
        if self.robotState != IDLE: return
        cmd = "M4 %d\n" % (int(laserPower * rate))

        self.robotModel.laserPower = laserPower

        self.robotModel.state = BUSYING
        self.remoteAdapter.sendCmd(cmd)


    def M5(self):
        if self.robotState != IDLE: return
        cmd = "M5 A%d B%d H%d W%d\n" % (self.motoADir, self.motoBDir, self.height, self.width)

        self.robotModel.state = BUSYING
        self.remoteAdapter.sendCmd(cmd)


    def readRobotConfig(self):  # read robot arm setup and init pos
        cmd = "M10\n"
        self.remoteAdapter.sendCmd(cmd)


    def M11(self):  # read end stop value form xy
        cmd = "M11\n"
        self.remoteAdapter.sendCmd(cmd)


    def messageReceived(self, msg):
        """
        callback method that will be executed when remote adapter receives a message
        :param msg:
        :return:
        """
        logger.info("messageReceived")

        if "M10" in msg:
            logger.debug("messageReceived: handle M10")
            tmp = msg.split()

            if tmp[1] != "XY": return

            self.robotModel.width = float(tmp[2])
            self.robotModel.height = float(tmp[3])

            if tmp[6] == "A0":
                self.motoADir = 0
            else:
                self.motoADir = 1
            if tmp[7] == "B0":
                self.motoBDir = 0
            else:
                self.motoBDir = 1

            self.robotModel.state = IDLE

            self.onChangeRobot.fire()
        elif "M11" in msg:
            logger.debug("messageReceived: handle M11")

            t = msg.split()

# self.robotSetup.ui.label_8.setText("X-:%s X+:%s Y-:%s Y+:%s " % (t[1], t[2], t[3], t[4]))
