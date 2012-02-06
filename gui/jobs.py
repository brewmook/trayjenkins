from PySide import QtCore, QtGui
from trayjenkins.jobs.interfaces import IView
from pyjenkins.job import JobStatus

class JobsListView(QtGui.QGroupBox, IView):

    def __init__(self, mediaFiles):
        """
        @type mediaFiles: gui.media.MediaFiles
        """
        QtGui.QGroupBox.__init__(self, "Jobs")

        self._jobs = QtGui.QListWidget()
        self._icons = {
            JobStatus.FAILING: QtGui.QIcon(mediaFiles.failingImagePath()),
            JobStatus.OK:      QtGui.QIcon(mediaFiles.okImagePath()),
            JobStatus.UNKNOWN: QtGui.QIcon(mediaFiles.unknownImagePath()),
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
