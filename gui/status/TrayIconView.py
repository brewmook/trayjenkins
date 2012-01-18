import trayjenkins
from PySide import QtGui
from pyjenkins.Event import Event
from trayjenkins.status.interfaces import IView

class TrayIconView(IView):

    def __init__(self, parentWidget, delayInSecons):
        """
        @type parentWidget: QtGui.QWidget
        """
        self._statusRefreshEvent= Event()
        self._delayInSeconds= delayInSecons

        self._trayIcon= QtGui.QSystemTrayIcon(parentWidget)
        self._trayIcon.show()

        self._icons= {}
        self._icons[trayjenkins.status.FAILING]= QtGui.QIcon('images/status/failing.png')
        self._icons[trayjenkins.status.OK]=      QtGui.QIcon('images/status/ok.png')
        self._icons[trayjenkins.status.UNKNOWN]= QtGui.QIcon('images/status/unknown.png')

        self.setStatus(trayjenkins.status.UNKNOWN)

    def statusRefreshEvent(self):
        """
        Event arguments: <none>
        @rtype: pyjenkins.interfaces.IEvent
        """
        return self._statusRefreshEvent

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
