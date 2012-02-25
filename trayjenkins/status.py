from trayjenkins.event import Event
from pyjenkins.job import JobStatus

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

class Presenter(object):

    def __init__(self, model, view):
        """
        @type model: trayjenkins.status.IModel
        @type view:  trayjenkins.status.IView
        """
        self._model= model
        self._view= view
        model.statusChangedEvent().register(self.onModelStatusChanged)

    def onModelStatusChanged(self, status):

        self._view.setStatus(status)

class StatusReader(IStatusReader):

    def status(self, jobs):
        """
        @type jobs: [pyjenkins.job.Job]
        @return String from pyjenkins.job.JobStatus
        @rtype: str
        """
        result= JobStatus.OK

        if jobs is None:
            result= JobStatus.UNKNOWN
        else:
            for job in jobs:
                if job.status is JobStatus.FAILING:
                    result= JobStatus.FAILING
                    break

        return result

class Model(IModel):

    def __init__(self, jobsModel,
                 statusReader=StatusReader(),
                 statusChangedEvent=Event()):
        """
        @type statusReader: trayjenkins.jobs.IModel
        @type statusReader: trayjenkins.status.IStatusReader
        """
        self._statusReader = statusReader
        self._statusChangedEvent = statusChangedEvent
        self._status = JobStatus.UNKNOWN
        
        jobsModel.jobsUpdatedEvent().register(self.onJobsUpdated)

    def onJobsUpdated(self, jobs):

        newStatus = self._statusReader.status(jobs)
        if newStatus is not self._status:
            self._statusChangedEvent.fire(newStatus)
            self._status = newStatus

    def statusChangedEvent(self):
        """
        Event arguments: status:str
        @rtype: trayjenkins.event.IEvent
        """
        return self._statusChangedEvent
