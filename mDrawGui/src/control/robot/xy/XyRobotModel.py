__author__ = 'abos'

IDLE = 0
BUSYING = 1

class XyRobotModel:
    """
    Saves a robot state
    """

    def __init__(self):
        self.state = IDLE
        self.moving = False
        self.robotCent = None
        #initial params
        self.width = 380
        self.height = 310

        self.scaler = 1.0

        self.x = 0
        self.y = 0

        self.txtPtr=[]

        self.motoADir = 0
        self.motoBDir = 0

        self.laserBurnDelay = 0
        self.origin = None
        self.xyorigin = None
        #self.q = Queue.Queue()
        self.pRect = None
        #self.moveList = None
        self.printing = False
        self.pausing = False
        self.laserMode = False
        #self.lastx = 9999
        #self.lasty = 9999

