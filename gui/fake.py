from trayjenkins.event import Event
from trayjenkins.jobs import IModel
from pyjenkins.job import Job, JobStatus

class JobsModel(IModel):

    def __init__(self):
        self._jobsUpdatedEvent = Event()
        self._jobs = []
        self._jobs_rota = [[Job('spam', JobStatus.OK),
                          Job('eggs', JobStatus.OK)],
                         [Job('spam', JobStatus.FAILING),
                          Job('eggs', JobStatus.DISABLED)],
                        ]
        self._next_jobs = 0

    def updateJobs(self):
        """
        @rtype: None
        """
        jobs = self._jobs_rota[self._next_jobs]
        if self._jobs != jobs:
            self._jobs = jobs
            self._jobsUpdatedEvent.fire(jobs)

        self._next_jobs = self._next_jobs + 1
        if self._next_jobs is len(self._jobs_rota):
            self._next_jobs = 0
            
    def jobsUpdatedEvent(self):
        """
        Listeners receive Event.fire([pyjenkins.job.Job])
        @rtype: trayjenkins.event.IEvent
        """
        return self._jobsUpdatedEvent
