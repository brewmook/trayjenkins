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

    def enable_job(self, job_name):

        job = self._find_job(job_name)
        if job:
            job.status = JobStatus.OK
        return True

    def disable_job(self, job_name):

        job = self._find_job(job_name)
        if job:
            job.status = JobStatus.DISABLED
        return False

    def _find_job(self, job_name):

        result = None
        jobs = [job for job in self._jobs_rota[self._next_jobs] if job.name == job_name]
        if jobs != []:
            result = jobs[0]
        return result
