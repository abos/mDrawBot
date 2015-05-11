import logging

__author__ = 'abos'

logger = logging.getLogger(__name__)


class AbstractRobotGui:
    def __init__(self):
        pass

    def robotGoHome(self):
        raise NotImplementedError

    def showSetup(self):
        raise NotImplementedError

    def moveTo(self, position):
        raise NotImplementedError
