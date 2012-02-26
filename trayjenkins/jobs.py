from pyjenkins.backend.http import Http
from pyjenkins.jenkins import Jenkins, JenkinsFactory
from pyjenkins.server import Server
from trayjenkins.event import Event

class IModel(object):

    def updateJobs(self):
        """
        @rtype: None
        """

    def jobsUpdatedEvent(self):
        """
        Listeners receive Event.fire([pyjenkins.job.Job])
        @rtype: trayjenkins.event.IEvent
        """

class IView(object):
    
    def setJobs(self, jobs):
        """
        @type jobs: [pyjenkins.job.Job]
        """

class IFilter(object):

    def filter(self, jobs):
        """
        @type jobs: [pyjenkins.job.Job]
        @rtype: [pyjenkins.job.Job]
        """

class Presenter(object):

    def __init__(self, model, view):
        """
        @type model: trayjenkins.jobs.IModel
        @type view:  trayjenkins.jobs.IView
        """
        self._model= model
        self._view= view
        model.jobsUpdatedEvent().register(self.onModelJobsChanged)

    def onModelJobsChanged(self, jobs):
        
        self._view.setJobs(jobs)


class Model(IModel):

    def __init__(self, server,
                 jenkinsFactory=JenkinsFactory(),
                 event=Event()):
        """
        @type server: pyjenkins.server.Server
        @type jenkinsFactory: pyjenkins.interfaces.IJenkinsFactory
        @type event: trayjenkins.event.IEvent
        """
        self._jenkins = jenkinsFactory.create(server)
        self._jobsUpdatedEvent = event
        self.jobs = None

    def updateJobs(self):
        """
        @rtype: None
        """
        jobs = self._jenkins.listJobs()
        if self.jobs != jobs:
            self.jobs = jobs
            self._jobsUpdatedEvent.fire(jobs)

    def jobsUpdatedEvent(self):
        """
        Listeners receive Event.fire([pyjenkins.job.Job])
        @rtype: trayjenkins.event.IEvent
        """
        return self._jobsUpdatedEvent

class NoFilter(IFilter):

    def filter(self, jobs):

        return jobs

class IgnoreJobsFilter(IFilter):

    def __init__(self):

        self._ignores = set()

    def filter(self, jobs):

        return [job for job in jobs if job.name not in self._ignores]

    def ignore(self, jobName):

        self._ignores.add(jobName)

    def unignore(self, jobName):

        self._ignores.discard(jobName)

    def ignoring(self, jobName):

        return jobName in self._ignores
