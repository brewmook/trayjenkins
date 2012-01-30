from PySide import QtCore

class JobsUpdateTimer(QtCore.QObject):

    def __init__(self, jobsModel, seconds, parent=None):
        """
        @type jobsModel: trayjenkins.jobs.interfaces.IModel
        @type seconds: int
        @type parent: PySide.QtCore.QObject
        """
        QtCore.QObject.__init__(self, parent)

        self.jobsTimerId = self.startTimer(seconds * 1000)
        self.jobsModel = jobsModel
        self.jobsModel.updateJobs()

    def timerEvent(self, event):

        if event.timerId() == self.jobsTimerId:
            self.jobsModel.updateJobs()
