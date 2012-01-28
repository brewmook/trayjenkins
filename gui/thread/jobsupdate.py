from PySide import QtCore

class JobsUpdateThread(QtCore.QThread):

    def __init__(self, jobsModel, seconds):
        """
        @type jobsModel: trayjenkins.jobs.interfaces.IModel
        @type seconds: int
        """
        QtCore.QThread.__init__(self)
        self.jobsModel = jobsModel
        self.seconds = seconds

    def run(self):

        while True:
            self.jobsModel.updateJobs()
            self.sleep(self.seconds)
