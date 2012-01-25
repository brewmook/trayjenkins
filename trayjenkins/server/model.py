from pyjenkins.backend.http import Http
from pyjenkins.event import Event
from pyjenkins.jenkins import Jenkins, JenkinsFactory
from pyjenkins.server import Server
from trayjenkins.server.interfaces import IModel

class Model(IModel):

    def __init__(self, server,
                 jenkinsFactory=JenkinsFactory(),
                 event=Event()):
        """
        @type server: pyjenkins.server.Server
        @type jenkinsFactory: pyjenkins.interfaces.IJenkinsFactory
        @type event: pyjenkins.interfaces.IEvent
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
        @rtype: pyjenkins.interfaces.IEvent
        """
        return self._jobsUpdatedEvent
