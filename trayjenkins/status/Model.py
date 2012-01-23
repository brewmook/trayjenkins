from trayjenkins.status.interfaces import IModel
from pyjenkins.job import JobStatus
from pyjenkins.event import Event

class Model(IModel):

    def __init__(self, statusReader):
        """
        @type statusReader: trayjenkins.status.interfaces.IStatusReader
        """
        self._statusReader = statusReader
        self._statusChangedEvent = Event()
        self._status = JobStatus.UNKNOWN

    def updateStatus(self):

        newStatus = self._statusReader.status()
        if newStatus is not self._status:
            self._statusChangedEvent.fire(newStatus)
            self._status = newStatus

    def statusChangedEvent(self):
        """
        Event arguments: status:str
        @rtype: pyjenkins.interfaces.IEvent
        """
        return self._statusChangedEvent
