import trayjenkins
from trayjenkins.status.interfaces import IModel

class Model(IModel):

    def __init__(self, jenkins, ignoreJobs=[]):
        """
        @type jenkins: pyjenkins.interfaces.IJenkins
        @type ignoreJobs: [str]
        """
        self._jenkins = jenkins
        self._ignoreJobs = ignoreJobs

    def status(self):

        result= trayjenkins.status.FAILING
        failingJobs= self._jenkins.listFailingJobs()

        if failingJobs is None:
            result= trayjenkins.status.UNKNOWN
        else:
            failingJobs= [job for job in failingJobs if job not in self._ignoreJobs]
            if not failingJobs:
                result= trayjenkins.status.OK

        return result