from PySide import QtCore, QtGui
from trayjenkins.jobs import IView
from pyjenkins.job import JobStatus

class _QMenuFactory(object):

    def create(self, parentWidget):
        """
        @type parentWidget: PySide.QtGui.Widget
        """
        return QtGui.QMenu(parentWidget)

class ContextSensitiveMenuFactory(object):

    def __init__(self, actions, ignoreJobsFilter, menuFactory=_QMenuFactory()):
        """
        @type actions: {str => PySide.QtGui.QAction}
        @type ignoreJobsFilter: trayjenkins.jobs.IgnoreJobsFilter
        @type menuFactory: _QMenuFactory
        """
        self._actions = actions
        self._ignoreJobsFilter = ignoreJobsFilter
        self._menuFactory = menuFactory

    def create(self, parentWidget, itemText):
        """
        @type parentWidget: PySide.QtGui.Widget
        """
        menu = self._menuFactory.create(parentWidget)
        if self._ignoreJobsFilter.ignoring(itemText):
            menu.addAction(self._actions['Cancel ignore'])
        else:
            menu.addAction(self._actions['Ignore'])
        return menu


class ListWithContextMenu(QtGui.QListWidget):

    def __init__(self, menuFactory, parent=0):
        """
        @type menuFactory: MenuFactory
        """
        super(ListWithContextMenu, self).__init__(parent)
        self._menuFactory = menuFactory

    def contextMenuEvent(self, event):
        """
        @type event: PySide.QtGui.QContextMenuEvent
        """
        item = self.itemAt(event.pos())
        if item is not None:
            menu = self._menuFactory.create(self, item.text())
            menu.popup(self.mapToGlobal(event.pos()))


class ListView(QtGui.QGroupBox, IView):

    def __init__(self, mediaFiles, ignoreJobsFilter):
        """
        @type mediaFiles: gui.media.MediaFiles
        @type ignoreJobsFilter: trayjenkins.jobs.IgnoreJobsFilter
        """
        QtGui.QGroupBox.__init__(self, "Jobs")

        actions = { 'Ignore': QtGui.QAction('Ignore', self, triggered=self.ignoreJob),
                    'Cancel ignore': QtGui.QAction('Cancel ignore', self, triggered=self.unignoreJob) }

        menuFactory = ContextSensitiveMenuFactory(actions, ignoreJobsFilter)
        self._jobs = ListWithContextMenu(menuFactory, self)
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
