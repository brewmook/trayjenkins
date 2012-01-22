from trayjenkins.status.interfaces import IStatusReader
from pyjenkins.Job import JobStatus

class StatusReader(IStatusReader):

    def status(self, jenkins):
        """
        @type jenkins: pyjenkins.interfaces.IJenkins
        """
        result= JobStatus.OK
        jobs= jenkins.listJobs()

        if jobs is None:
            result= JobStatus.UNKNOWN
        else:
            for job in jobs:
                if job.status is JobStatus.FAILING:
                    result= JobStatus.FAILING
                    break

        return result