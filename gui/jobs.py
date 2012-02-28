from PySide import QtCore, QtGui
from trayjenkins.jobs import IView
from pyjenkins.job import JobStatus
from gui.qmock import QtGuiFactory

class ContextMenuActions(object):

    def __init__(self, parent, ignore_trigger, cancel_ignore_trigger):

        self._ignore = QtGui.QAction('Ignore', parent, triggered=ignore_trigger)
        self._cancel_ignore = QtGui.QAction('Cancel ignore', parent, triggered=cancel_ignore_trigger)

    def ignore(self):
        return self._ignore

    def cancel_ignore(self):
        return self._cancel_ignore


class ContextSensitiveMenuFactory(object):

    def __init__(self, actions, ignoreJobsFilter, qtgui=QtGuiFactory()):
        """
        @type actions: ContextMenuActions
        @type ignoreJobsFilter: trayjenkins.jobs.IgnoreJobsFilter
        @type qtgui: QtGuiFactory
        """
        self._actions = actions
        self._ignoreJobsFilter = ignoreJobsFilter
        self._qtgui = qtgui

    def create(self, parentWidget, itemText):
        """
        @type parentWidget: PySide.QtGui.Widget
        """
        menu = self._qtgui.QMenu(parentWidget)
        if self._ignoreJobsFilter.ignoring(itemText):
            menu.addAction(self._actions.cancel_ignore())
        else:
            menu.addAction(self._actions.ignore())
        return menu


class ListView(QtGui.QGroupBox, IView):

    def __init__(self, mediaFiles, ignoreJobsFilter):
        """
        @type mediaFiles: gui.media.MediaFiles
        @type ignoreJobsFilter: trayjenkins.jobs.IgnoreJobsFilter
        """
        QtGui.QGroupBox.__init__(self, "Jobs")

        self._actions = ContextMenuActions(self,
                                           ignore_trigger=self.ignoreJob,
                                           cancel_ignore_trigger=self.unignoreJob)

        self._jobs = QtGui.QListWidget(self)
        self._jobs.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self._jobs.customContextMenuRequested.connect(self.onCustomContextMenuRequested)
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

    def onCustomContextMenuRequested(self, point):
        """
        @type point: PySide.QtCore.QPoint
        """
        item = self._jobs.itemAt(point)
        if item is not None:
            factory = ContextSensitiveMenuFactory(self._actions, self._ignoreJobsFilter)
            menu = factory.create(self._jobs, item.text())
            menu.popup(self._jobs.mapToGlobal(point))

    def ignoreJob(self):

        item = self._jobs.currentItem()
        if item is not None:
            self._ignoreJobsFilter.ignore(item.text())
            item.setIcon(self._ignoredIcon)
        
    def unignoreJob(self):

        item = self._jobs.currentItem()
        if item is not None:
            self._ignoreJobsFilter.unignore(item.text())
            item.setIcon(self._icons[JobStatus.UNKNOWN])
        
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
