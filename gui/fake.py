from trayjenkins.event import Event
from trayjenkins.jobs import IModel
from pyjenkins.job import Job, JobStatus

class JobsModel(IModel):

    def __init__(self):
        self._jobs_updated_event = Event()
        self._jobs = []
        self._jobs_rota = [[Job('spam', JobStatus.OK),
                          Job('eggs', JobStatus.OK)],
                         [Job('spam', JobStatus.FAILING),
                          Job('eggs', JobStatus.DISABLED)],
                        ]
        self._next_jobs = 0

    def update_jobs(self):
        """
        @rtype: None
        """
        jobs = self._jobs_rota[self._next_jobs]
        if self._jobs != jobs:
            self._jobs = jobs
            self._jobs_updated_event.fire(jobs)

        self._next_jobs = self._next_jobs + 1
        if self._next_jobs is len(self._jobs_rota):
            self._next_jobs = 0
            
    def jobs_updated_event(self):
        """
        Listeners receive Event.fire([pyjenkins.job.Job])
        @rtype: trayjenkins.event.IEvent
        """
        return self._jobs_updated_event
