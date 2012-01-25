from PySide import QtGui
from trayjenkins.jobs.interfaces import IView
from pyjenkins.job import JobStatus

class JobsListView(QtGui.QGroupBox, IView):

    def __init__(self):
        QtGui.QGroupBox.__init__(self, "Jobs")

        self._jobs = QtGui.QListWidget()
        self._icons = {JobStatus.FAILING: QtGui.QIcon('images/status/failing.png'),
                       JobStatus.OK:      QtGui.QIcon('images/status/ok.png'),
                       JobStatus.UNKNOWN: QtGui.QIcon('images/status/unknown.png')}

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
