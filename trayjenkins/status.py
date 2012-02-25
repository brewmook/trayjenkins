from trayjenkins.event import Event
from pyjenkins.job import JobStatus

class IModel(object):

    def statusChangedEvent(self):
        """
        Event arguments: (status:str, message:str)
        @rtype: trayjenkins.event.IEvent
        """

class IView(object):

    def setStatus(self, status, message):
        """
        @type status: str
        @type message: str
        """

class IStatusReader(object):

    def status(self, jobs):
        """
        @type jobs: [pyjenkins.job.Job]
        @return String from pyjenkins.job.JobStatus
        @rtype: str
        """

class IMessageComposer(object):

    def message(self, jobs):
        """
        @type jobs: [pyjenkins.job.Job]
        @return Brief message describing the job statuses.
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

    def onModelStatusChanged(self, status, message):

        self._view.setStatus(status, message)

class DefaultMessageComposer(IMessageComposer):

    def message(self, jobs):
        """
        @type jobs: [pyjenkins.job.Job]
        @return Brief message describing the job statuses.
        @rtype: str
        """
        result = ''
        if jobs is not None:
            if len(jobs) == 0:
                result = 'No jobs'
            else:
                failing = [job.name for job in jobs if job.status == JobStatus.FAILING]
                if failing:
                    result = 'FAILING:\n' + '\n'.join(failing)
                else:
                    result = 'All active jobs pass'

        return result

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
                 messageComposer=DefaultMessageComposer(),
                 statusReader=StatusReader(),
                 statusChangedEvent=Event()):
        """
        @type statusReader: trayjenkins.jobs.IModel
        @type statusReader: trayjenkins.status.IStatusReader
        """
        self._messageComposer = messageComposer
        self._statusReader = statusReader
        self._statusChangedEvent = statusChangedEvent
        self._lastStatus = JobStatus.UNKNOWN
        self._lastMessage = None
        
        jobsModel.jobsUpdatedEvent().register(self.onJobsUpdated)

    def onJobsUpdated(self, jobs):

        status = self._statusReader.status(jobs)
        message = self._messageComposer.message(jobs)
        if self._lastStatus != status or self._lastMessage != message:
            self._statusChangedEvent.fire(status, message)
        self._lastStatus = status
        self._lastMessage = message

    def statusChangedEvent(self):
        """
        Event arguments: status:str
        @rtype: trayjenkins.event.IEvent
        """
        return self._statusChangedEvent
