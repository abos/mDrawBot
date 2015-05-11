import logging
from control.EventHook import EventHook
from control.robot.xy.XyRobotModel import XyRobotModel, IDLE, BUSYING

__author__ = 'abos'

logger = logging.getLogger(__name__)


class RemoteXyRobot:
    """
    Class to control remote robot. No algorithmic logic is involved in this class. This is
    a slim communication adapter only..
    """

    def __init__(self, robotModel):
        self.remoteAdapter = None
        self.robotModel = robotModel
        self.onChangeRobot = EventHook()


    def setRemoteAdapter(self, remoteAdapter):
        self.remoteAdapter = remoteAdapter
        self.remoteAdapter.register(self)


    def registerOnChangeRobot(self, listener):
        logger.info("registerOnChangeRobot")

        self.onChangeRobot += listener


    def _sendCmd(self, cmd):
        if not self.remoteAdapter:
            logger.debug("_sendCmd: no remote configured")
            return

        if self.robotModel.state != IDLE:
            logger.debug("_sendCmd: robot not idle, ignore command ")
            return

        self.remoteAdapter.sendCmd(cmd)

    def goHome(self):
        """
        send robot home
        :return:
        """
        logger.info("goHome")

        self.robotModel.state = BUSYING
        self._sendCmd("G28\n")

        self.robotModel.x = 0
        self.robotModel.y = 0


    def moveTo(self, x, y, feedrate=0, auxdelay=None):
        logger.info("moveTo")

        cmd = "G1 X%.2f Y%.2f" % (x, y)

        if auxdelay != None:
            cmd += " A%d" % (auxdelay)

        cmd += '\n'
        self._sendCmd(cmd)


    def movePen(self, pos):
        logger.info("movePen")

        cmd = "M1 %d" % (pos)
        cmd += '\n'
        self._sendCmd(cmd)


    def M3(self, auxdelay):  # aux delay
        cmd = "M3 %d\n" % (auxdelay)
        self._sendCmd(cmd)


    def setupLaserPower(self, laserPower, rate=1):
        logger.info("setupLaserPower")
        cmd = "M4 %d\n" % (int(laserPower * rate))
        self.robotModel.laserPower = laserPower
        self._sendCmd(cmd)


    def M5(self):
        cmd = "M5 A%d B%d H%d W%d\n" % (self.motoADir, self.motoBDir, self.height, self.width)
        self._sendCmd(cmd)


    def readRobotConfig(self):  # read robot arm setup and init pos
        cmd = "M10\n"
        self._sendCmd(cmd)


    def M11(self):  # read end stop value form xy
        cmd = "M11\n"
        self._sendCmd(cmd)


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
