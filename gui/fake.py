from pyjenkins.job import Job, JobStatus


class Jenkins(object):

    def __init__(self):
        self._jobs_rota = [[Job('spam', JobStatus.OK),
                            Job('eggs', JobStatus.OK)],
                           [Job('spam', JobStatus.FAILING),
                            Job('eggs', JobStatus.DISABLED)],
                           ]
        self._next_jobs = 0

    def list_jobs(self):
        """
        @rtype: None
        """
        result = self._jobs_rota[self._next_jobs]

        self._next_jobs = self._next_jobs + 1
        if self._next_jobs is len(self._jobs_rota):
            self._next_jobs = 0

        return result
