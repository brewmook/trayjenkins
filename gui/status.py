from PySide import QtGui
from PySide.phonon import Phonon
from pyjenkins.job import JobStatus
from trayjenkins.status import IView

class TrayIconView(object):

    def __init__(self, trayIcon):
        """
        @type trayIcon: QtGui.QSystemTrayIcon
        """
        self._trayIcon= trayIcon

    def setIcon(self, trayIcon, tooltip, messageTitle, messageText, messageIcon):
        """
        @type trayIcon: QtGui.QIcon
        @type tooltip: str
        @type messageTitle: unicode
        @type messageText: unicode
        @type messageIcon: QtGui.QSystemTrayIcon.MessageIcon
        """
        self._trayIcon.setIcon(trayIcon)
        self._trayIcon.setToolTip(tooltip)
        self._trayIcon.showMessage(messageTitle, messageText, messageIcon)


class TrayIconViewAdapter(IView):

    def __init__(self, view, mediaFiles):
        """
        @type view: gui.status.TrayIconView
        @type mediaFiles: gui.media.MediaFiles
        """
        self._view = view
        self._media = mediaFiles

    def setStatus(self, status, message):
        """
        @type status: str
        @type message: str
        """
        messageIcon = QtGui.QSystemTrayIcon.Information
        if status is JobStatus.FAILING:
            trayIcon = self._media.failing_icon()
            messageIcon = QtGui.QSystemTrayIcon.Warning
        elif status is JobStatus.OK:
            trayIcon = self._media.ok_icon()
        else:
            trayIcon = self._media.unknown_icon()

        if status is None:
            tooltip = 'None'
        else:
            tooltip = status.capitalize()

        if message is None:
            message = ''

        self._view.setIcon(trayIcon,
                           tooltip,
                           unicode('Jenkins status change'),
                           unicode(message),
                           messageIcon)


class SoundView(IView):

    def __init__(self, parent, mediaFiles):
        """
        @type parent: QtGui.QWidget
        @type mediaFiles: gui.media.MediaFiles
        """
        self.mediaObject = Phonon.MediaObject(parent)
        self.audioOutput = Phonon.AudioOutput(Phonon.NotificationCategory, parent)
        Phonon.createPath(self.mediaObject, self.audioOutput)

        self._sounds = {
            JobStatus.FAILING: Phonon.MediaSource(mediaFiles.failing_sound_path()),
            JobStatus.OK:      Phonon.MediaSource(mediaFiles.ok_sound_path()),
            }

    def setStatus(self, status, message):
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
        @type views: [trayjenkins.status.IView]
        """
        self._views = views

    def setStatus(self, status, message):
        """
        @type status: str
        """
        for view in self._views:
            view.setStatus(status, message)
