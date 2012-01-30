class IModel(object):

    def statusChangedEvent(self):
        """
        Event arguments: status:str
        @rtype: trayjenkins.event.IEvent
        """

class IView(object):

    def setStatus(self, status):
        """
        @type status: str
        """

class IStatusReader(object):

    def status(self, jobs):
        """
        @type jobs: [pyjenkins.job.Job]
        @return String from pyjenkins.job.JobStatus
        @rtype: str
        """
