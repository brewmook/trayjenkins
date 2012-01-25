from PySide import QtCore

class JobsUpdateThread(QtCore.QThread):

    def __init__(self, jobsModel):
        """
        @type jobsModel: trayjenkins.jobs.interfaces.IModel
        """
        QtCore.QThread.__init__(self)
        self.jobsModel = jobsModel

    def run(self):

        while True:
            self.jobsModel.updateJobs()
            self.sleep(15)
