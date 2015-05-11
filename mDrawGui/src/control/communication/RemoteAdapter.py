import logging

__author__ = 'abos'

logger = logging.getLogger(__name__)


class RemoteAdapter:
    def __init__(self):
        self.listener = None

    def register(self, listener):
        logger.info("register")
        self.listener = listener

    def sendCmd(self, cmd=""):
        logger.info("sendCmd: cmd: <%s>", cmd)

        if not cmd:
            cmd = str(self.ui.lineSend.text()) + '\n'

        self.comm.send(cmd)
