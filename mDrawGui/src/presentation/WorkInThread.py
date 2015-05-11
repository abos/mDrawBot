import threading

__author__ = 'abos'


class WorkInThread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)


    def run(self):
        self._target(*self._args)
