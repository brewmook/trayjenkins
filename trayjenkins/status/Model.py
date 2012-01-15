import trayjenkins
from trayjenkins.status.interfaces import IModel

class Model(IModel):

    def __init__(self, jenkins):
        """
        @type jenkins: pyjenkins.interfaces.IJenkins
        """
        self._jenkins = jenkins

    def status(self):

        result= trayjenkins.status.FAILING
        failingJobs= self._jenkins.listFailingJobs()

        if failingJobs is None:
            result= trayjenkins.status.UNKNOWN
        elif not failingJobs:
            result= trayjenkins.status.OK

        return result