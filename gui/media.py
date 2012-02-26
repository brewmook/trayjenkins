import os
from PySide import QtGui

class MediaFiles(object):

    def __init__(self, executablePath):
        self._executablePath = executablePath

    def disabledIcon(self):
        return QtGui.QIcon(self._locate('media/status/disabled.png'))

    def failingIcon(self):
        return QtGui.QIcon(self._locate('media/status/failing.png'))

    def ignoredIcon(self):
        return QtGui.QIcon(self._locate('media/status/ignored.png'))

    def okIcon(self):
        return QtGui.QIcon(self._locate('media/status/ok.png'))

    def unknownIcon(self):
        return QtGui.QIcon(self._locate('media/status/unknown.png'))

    def okSoundPath(self):
        return self._locate('media/status/ok.wav')

    def failingSoundPath(self):
        return self._locate('media/status/failing.wav')

    def _locate(self, resource):
        return os.path.join(self._executablePath, resource)
