import os

class MediaFiles(object):

    def __init__(self, executablePath):
        self._executablePath = executablePath

    def disabledImagePath(self):
        return self._locate('media/status/disabled.png')

    def okImagePath(self):
        return self._locate('media/status/ok.png')

    def failingImagePath(self):
        return self._locate('media/status/failing.png')

    def unknownImagePath(self):
        return self._locate('media/status/unknown.png')

    def okSoundPath(self):
        return self._locate('media/status/ok.wav')

    def failingSoundPath(self):
        return self._locate('media/status/failing.wav')

    def _locate(self, resource):
        return os.path.join(self._executablePath, resource)
