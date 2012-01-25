from trayjenkins.status.interfaces import IStatusReader
from pyjenkins.job import JobStatus

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
