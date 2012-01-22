from trayjenkins.status.StatusReader import StatusReader
from trayjenkins.status.interfaces import IModel
from pyjenkins.Job import JobStatus
from pyjenkins.Event import Event

class Model(IModel):

    def __init__(self, jenkins, statusReader=StatusReader()):
        """
        @type jenkins: pyjenkins.interfaces.IJenkins
        @type statusReader: trayjenkins.status.interfaces.IStatusReader
        """
        self._jenkins = jenkins
        self._statusReader = statusReader
        self._statusChangedEvent = Event()
        self._status = JobStatus.UNKNOWN

    def updateStatus(self):

        newStatus = self._statusReader.status(self._jenkins)
        if newStatus is not self._status:
            self._statusChangedEvent.fire(newStatus)
            self._status = newStatus

    def statusChangedEvent(self):
        """
        Event arguments: status:str
        @rtype: pyjenkins.interfaces.IEvent
        """
        return self._statusChangedEvent