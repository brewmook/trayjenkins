from PySide import QtGui
from pyjenkins.Job import JobStatus
from trayjenkins.status.interfaces import IView

class TrayIconView(IView):

    def __init__(self, parentWidget, delayInSecons, menu):
        """
        @type parentWidget: QtGui.QWidget
        @type delayInSecons: int
        @type menu: QtGui.QMenu
        """
        self._delayInSeconds= delayInSecons

        self._trayIcon= QtGui.QSystemTrayIcon(parentWidget)
        self._trayIcon.setContextMenu(menu)

        self._icons= {JobStatus.FAILING: QtGui.QIcon('images/status/failing.png'),
                      JobStatus.OK:      QtGui.QIcon('images/status/ok.png'),
                      JobStatus.UNKNOWN: QtGui.QIcon('images/status/unknown.png')}

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
                                   QtGui.QSystemTrayIcon.Information,# icon,
                                   self._delayInSeconds * 1000)
