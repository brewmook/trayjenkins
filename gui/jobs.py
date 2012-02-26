from PySide import QtCore, QtGui
from trayjenkins.jobs import IView
from pyjenkins.job import JobStatus

class ListView(QtGui.QGroupBox, IView):

    def __init__(self, mediaFiles):
        """
        @type mediaFiles: gui.media.MediaFiles
        """
        QtGui.QGroupBox.__init__(self, "Jobs")

        self._jobs = QtGui.QListWidget()
        self._icons = {
            JobStatus.DISABLED: mediaFiles.disabledIcon(),
            JobStatus.FAILING:  mediaFiles.failingIcon(),
            JobStatus.OK:       mediaFiles.okIcon(),
            JobStatus.UNKNOWN:  mediaFiles.unknownIcon(),
            }

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self._jobs)
        self.setLayout(layout)

    def setJobs(self, jobs):
        """
        @type jobs: [pyjenkins.job.Job]
        """
        self._jobs.clear()
        for job in jobs:
            self._jobs.addItem(QtGui.QListWidgetItem(self._icons[job.status],
                                                     job.name))

class UpdateTimer(QtCore.QObject):

    def __init__(self, jobsModel, seconds, parent=None):
        """
        @type jobsModel: trayjenkins.jobs.IModel
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
