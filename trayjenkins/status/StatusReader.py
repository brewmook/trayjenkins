from trayjenkins.status.interfaces import IStatusReader
from pyjenkins.Job import JobStatus

class StatusReader(IStatusReader):

    def __init__(self, jenkins):
        """
        @type jenkins: pyjenkins.interfaces.IJenkins
        """
        self._jenkins = jenkins

    def status(self):

        result= JobStatus.OK
        jobs= self._jenkins.listJobs()

        if jobs is None:
            result= JobStatus.UNKNOWN
        else:
            for job in jobs:
                if job.status is JobStatus.FAILING:
                    result= JobStatus.FAILING
                    break

        return result