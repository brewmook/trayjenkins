from PySide import QtCore, QtGui
from trayjenkins.jobs import IView
from pyjenkins.job import JobStatus

class ListWithContextMenu(QtGui.QListWidget):

    def __init__(self, actions, parent=0):
        """
        @type actions: {str => PySide.QtGui.QAction}
        """
        super(ListWithContextMenu, self).__init__(parent)
        self._actions = actions

    def contextMenuEvent(self, event):
        """
        @type event: PySide.QtGui.QContextMenuEvent
        """
        if self.itemAt(event.pos()) is not None:
            menu = self._buildContextMenu()
            menu.popup(self.mapToGlobal(event.pos()))

    def _buildContextMenu(self):

        menu = QtGui.QMenu(self)
        for action in self._actions:
            menu.addAction(self._actions[action])
        return menu


class ListView(QtGui.QGroupBox, IView):

    def __init__(self, mediaFiles, ignoreJobsFilter):
        """
        @type mediaFiles: gui.media.MediaFiles
        """
        QtGui.QGroupBox.__init__(self, "Jobs")

        self._actions = { 'Ignore': QtGui.QAction('Ignore', self, triggered=self.ignoreJob),
                          'Cancel ignore': QtGui.QAction('Cancel ignore', self, triggered=self.unignoreJob) }

        self._jobs = ListWithContextMenu(self._actions, self)
        self._ignoreJobsFilter = ignoreJobsFilter
        self._icons = {
            JobStatus.DISABLED: mediaFiles.disabledIcon(),
            JobStatus.FAILING:  mediaFiles.failingIcon(),
            JobStatus.OK:       mediaFiles.okIcon(),
            JobStatus.UNKNOWN:  mediaFiles.unknownIcon(),
            }
        self._ignoredIcon = mediaFiles.ignoredIcon()

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self._jobs)
        self.setLayout(layout)

    def ignoreJob(self):

        item = self._jobs.currentItem()
        if item is not None:
            self._ignoreJobsFilter.ignore(item.text())
        
    def unignoreJob(self):

        item = self._jobs.currentItem()
        if item is not None:
            self._ignoreJobsFilter.unignore(item.text())
        
    def setJobs(self, jobs):
        """
        @type jobs: [pyjenkins.job.Job]
        """
        self._jobs.clear()
        for job in jobs:
            if self._ignoreJobsFilter.ignoring(job.name):
                icon = self._ignoredIcon
            else:
                icon = self._icons[job.status]
            self._jobs.addItem(QtGui.QListWidgetItem(icon, job.name))

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
