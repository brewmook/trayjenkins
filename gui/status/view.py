from PySide import QtGui
from PySide.phonon import Phonon
from pyjenkins.job import JobStatus
from trayjenkins.status.interfaces import IView

class TrayIconView(IView):

    def __init__(self, parentWidget, menu):
        """
        @type parentWidget: QtGui.QWidget
        @type menu: QtGui.QMenu
        """
        self._trayIcon= QtGui.QSystemTrayIcon(parentWidget)
        self._trayIcon.setContextMenu(menu)

        self._icons= {JobStatus.FAILING: QtGui.QIcon('media/status/failing.png'),
                      JobStatus.OK:      QtGui.QIcon('media/status/ok.png'),
                      JobStatus.UNKNOWN: QtGui.QIcon('media/status/unknown.png')}
        self._sounds = {JobStatus.FAILING: QtGui.QSound('media/status/failing.wav'),
                        JobStatus.OK:      QtGui.QSound('media/status/ok.wav')}

        self.setStatus(JobStatus.UNKNOWN)

        self._trayIcon.show()

    def setStatus(self, status):
        """
        @type status: str
        """
        self._trayIcon.setIcon(self._icons[status])
        self._trayIcon.setToolTip(status.capitalize())
        
        self._trayIcon.showMessage(unicode("Jenkins status change"),
                                   unicode("Status: %s" % status.capitalize()),
                                   QtGui.QSystemTrayIcon.Information)

class SoundView(IView):

    def __init__(self, parent):

        self.mediaObject = Phonon.MediaObject(parent)
        self.audioOutput = Phonon.AudioOutput(Phonon.NotificationCategory, parent)
        Phonon.createPath(self.mediaObject, self.audioOutput)

        self._sounds = {JobStatus.FAILING: Phonon.MediaSource('media/status/failing.wav'),
                        JobStatus.OK:      Phonon.MediaSource('media/status/ok.wav')}

    def setStatus(self, status):
        """
        @type status: str
        """
        sound = self._sounds.get(status, None)
        if sound is not None:
            self.mediaObject.stop()
            self.mediaObject.clearQueue()
            self.mediaObject.setCurrentSource(sound)
            self.mediaObject.play()

class MultiView(IView):

    def __init__(self, views=[]):
        """
        @type views: [trayjenkins.status.interfaces.IView]
        """
        self._views = views

    def setStatus(self, status):
        """
        @type status: str
        """
        for view in self._views:
            view.setStatus(status)
