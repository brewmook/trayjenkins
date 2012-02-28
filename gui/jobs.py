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


class ContextMenuFactory(object):

    def __init__(self, actions, ignore_jobs_filter, qtgui=QtGuiFactory()):
        """
        @type actions: ContextMenuActions
        @type ignore_jobs_filter: trayjenkins.jobs.IgnoreJobsFilter
        @type qtgui: QtGuiFactory
        """
        self._actions = actions
        self._ignore_jobs_filter = ignore_jobs_filter
        self._qtgui = qtgui

    def create(self, parent, job_name):
        """
        @type parent: PySide.QtGui.Widget
        @type job_name: str
        """
        menu = self._qtgui.QMenu(parent)
        if self._ignore_jobs_filter.ignoring(job_name):
            menu.addAction(self._actions.cancel_ignore())
        else:
            menu.addAction(self._actions.ignore())
        return menu


class ListView(QtGui.QGroupBox, IView):

    def __init__(self, media_files, ignore_jobs_filter):
        """
        @type media_files: gui.media.MediaFiles
        @type ignore_jobs_filter: trayjenkins.jobs.IgnoreJobsFilter
        """
        QtGui.QGroupBox.__init__(self, "Jobs")

        self._actions = ContextMenuActions(self,
                                           ignore_trigger=self._ignore_job,
                                           cancel_ignore_trigger=self._unignore_job)

        self._jobs = QtGui.QListWidget(self)
        self._jobs.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self._jobs.customContextMenuRequested.connect(self._on_custom_context_menu_requested)
        self._ignore_jobs_filter = ignore_jobs_filter
        self._icons = {
            JobStatus.DISABLED: media_files.disabled_icon(),
            JobStatus.FAILING:  media_files.failing_icon(),
            JobStatus.OK:       media_files.ok_icon(),
            JobStatus.UNKNOWN:  media_files.unknown_icon(),
            }
        self._ignored_icon = media_files.ignored_icon()

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self._jobs)
        self.setLayout(layout)

    def _on_custom_context_menu_requested(self, point):
        """
        @type point: PySide.QtCore.QPoint
        """
        item = self._jobs.itemAt(point)
        if item is not None:
            factory = ContextMenuFactory(self._actions, self._ignore_jobs_filter)
            menu = factory.create(self._jobs, item.text())
            menu.popup(self._jobs.mapToGlobal(point))

    def _ignore_job(self):

        item = self._jobs.currentItem()
        if item is not None:
            self._ignore_jobs_filter.ignore(item.text())
            item.setIcon(self._ignored_icon)
        
    def _unignore_job(self):

        item = self._jobs.currentItem()
        if item is not None:
            self._ignore_jobs_filter.unignore(item.text())
            item.setIcon(self._icons[JobStatus.UNKNOWN])
        
    def set_jobs(self, jobs):
        """
        @type jobs: [pyjenkins.job.Job]
        """
        self._jobs.clear()
        for job in jobs:
            if self._ignore_jobs_filter.ignoring(job.name):
                icon = self._ignored_icon
            else:
                icon = self._icons[job.status]
            self._jobs.addItem(QtGui.QListWidgetItem(icon, job.name))

class UpdateTimer(QtCore.QObject):

    def __init__(self, jobs_model, seconds, parent=None):
        """
        @type jobs_model: trayjenkins.jobs.IModel
        @type seconds: int
        @type parent: PySide.QtCore.QObject
        """
        QtCore.QObject.__init__(self, parent)

        self._jobs_timer_id = self.startTimer(seconds * 1000)
        self._jobs_model = jobs_model
        self._jobs_model.update_jobs()

    def timerEvent(self, event):

        if event.timerId() == self._jobs_timer_id:
            self._jobs_model.update_jobs()
