from trayjenkins.event import Event
from trayjenkins.jobs import IModel
from pyjenkins.job import Job, JobStatus

class JobsModel(IModel):

    def __init__(self):
        self._jobsUpdatedEvent = Event()
        self.jobs = []
        self.jobsRota = [[Job('spam', JobStatus.OK),
                          Job('eggs', JobStatus.OK)],
                         [Job('spam', JobStatus.FAILING),
                          Job('eggs', JobStatus.OK)],
                        ]
        self.nextJobs = 0

    def updateJobs(self):
        """
        @rtype: None
        """
        jobs = self.jobsRota[self.nextJobs]
        if self.jobs != jobs:
            self.jobs = jobs
            self._jobsUpdatedEvent.fire(jobs)

        self.nextJobs = self.nextJobs + 1
        if self.nextJobs is len(self.jobsRota):
            self.nextJobs = 0
            
    def jobsUpdatedEvent(self):
        """
        Listeners receive Event.fire([pyjenkins.job.Job])
        @rtype: trayjenkins.event.IEvent
        """
        return self._jobsUpdatedEvent
