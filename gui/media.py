import os
from PySide import QtGui


class MediaFiles(object):

    def __init__(self, executable_path):
        self._executable_path = executable_path

    def disabled_icon(self):
        return QtGui.QIcon(self._locate('media/status/disabled.png'))

    def failing_icon(self):
        return QtGui.QIcon(self._locate('media/status/failing.png'))

    def ignored_icon(self):
        return QtGui.QIcon(self._locate('media/status/ignored.png'))

    def ok_icon(self):
        return QtGui.QIcon(self._locate('media/status/ok.png'))

    def unknown_icon(self):
        return QtGui.QIcon(self._locate('media/status/unknown.png'))

    def ok_sound_path(self):
        return self._locate('media/status/ok.wav')

    def failing_sound_path(self):
        return self._locate('media/status/failing.wav')

    def _locate(self, resource):
        return os.path.join(self._executable_path, resource)
