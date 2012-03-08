from PySide import QtCore, QtGui
from trayjenkins.event import Event
from trayjenkins.jobs import IView, IViewReplacement
from pyjenkins.job import JobStatus
from gui.qmock import QtGuiFactory


class ContextMenuActions(object):

    def __init__(self, ignore, cancel_ignore):
        self.ignore = ignore
        self.cancel_ignore = cancel_ignore


class ContextMenuFactory(object):

    def __init__(self, parent, actions, ignore_jobs_filter, qtgui=QtGuiFactory()):
        """
        @type parent: PySide.QtGui.Widget
        @type actions: ContextMenuActions
        @type ignore_jobs_filter: trayjenkins.jobs.IgnoreJobsFilter
        @type qtgui: QtGuiFactory
        """
        self._parent = parent
        self._actions = actions
        self._ignore_jobs_filter = ignore_jobs_filter
        self._qtgui = qtgui

    def create(self, job_name):
        """
        @type job_name: str
        """
        menu = self._qtgui.QMenu(self._parent)
        if self._ignore_jobs_filter.ignoring(job_name):
            menu.addAction(self._actions.cancel_ignore)
        else:
            menu.addAction(self._actions.ignore)
        return menu


class ListView(QtGui.QGroupBox):

    def job_ignored_event(self):
        """
        Listeners receive Event.fire(job_name:str)
        @rtype: trayjenkins.event.IEvent
        @todo: implement me
        """

    def job_unignored_event(self):
        """
        Listeners receive Event.fire(job_name:str)
        @rtype: trayjenkins.event.IEvent
        @todo: implement me
        """

    def __init__(self, media_files, ignore_jobs_filter):
        """
        @type media_files: gui.media.MediaFiles
        @type ignore_jobs_filter: trayjenkins.jobs.IgnoreJobsFilter
        """
        QtGui.QGroupBox.__init__(self, "Jobs")

        self._jobs = QtGui.QListWidget(self)
        self._jobs.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self._jobs.customContextMenuRequested.connect(self._on_custom_context_menu_requested)

        self._ignore_jobs_filter = ignore_jobs_filter

        actions = ContextMenuActions(QtGui.QAction('Ignore', self, triggered=self._ignore_job),
                                     QtGui.QAction('Cancel ignore', self, triggered=self._unignore_job))
        self._menu_factory = ContextMenuFactory(self._jobs, actions, ignore_jobs_filter)

        self._icons = {
            JobStatus.DISABLED: media_files.disabled_icon(),
            JobStatus.FAILING: media_files.failing_icon(),
            JobStatus.OK: media_files.ok_icon(),
            JobStatus.UNKNOWN: media_files.unknown_icon(),
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
            menu = self._menu_factory.create(item.text())
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

    def set_list(self, items):
        """
        @type items: [PySide.QtGui.QListWidgetItem]
        """
        self._jobs.clear()
        for item in items:
            self._jobs.addItem(item)


class ListViewReplacementAdapter(IViewReplacement):

    def job_ignored_event(self):
        """
        Listeners receive Event.fire(job_name:str)
        @rtype: trayjenkins.event.IEvent
        """
        return self._ignored_event

    def job_unignored_event(self):
        """
        Listeners receive Event.fire(job_name:str)
        @rtype: trayjenkins.event.IEvent
        """
        return self._unignored_event

    def __init__(self,
                 view,
                 media_files,
                 qtgui=QtGuiFactory()):
        """
        @type view: gui.jobs.ListView
        @type media_files: gui.media.MediaFiles
        @type qtgui: QtGuiFactory
        @type ignored_event: trayjenkins.event.IEvent
        @type unignored_event: trayjenkins.event.IEvent
        """
        self._view = view
        self._qtgui = qtgui
        self._ignored_event = Event()
        self._unignored_event = Event()

        view.job_ignored_event().register(self._on_view_ignored)
        view.job_unignored_event().register(self._on_view_unignored)

        self._ignored_icon = media_files.ignored_icon()
        self._status_icons = {JobStatus.DISABLED: media_files.disabled_icon(),
                              JobStatus.FAILING: media_files.failing_icon(),
                              JobStatus.OK: media_files.ok_icon(),
                              JobStatus.UNKNOWN: media_files.unknown_icon()}

    def set_jobs(self, job_models):
        """
        @type jobs: [trayjenkins.jobs.JobModel]
        """
        items = []
        for model in job_models:
            if model.ignored:
                icon = self._ignored_icon
            else:
                icon = self._status_icons[model.job.status]
            items.append(self._qtgui.QListWidgetItem(icon, model.job.name))

        self._view.set_list(items)

    def _on_view_ignored(self, job_name):

        self._ignored_event.fire(job_name)

    def _on_view_unignored(self, job_name):

        self._unignored_event.fire(job_name)


class ListViewAdapter(IView):

    def __init__(self, view, media_files, ignore_jobs_filter, qtgui=QtGuiFactory()):
        """
        @type view: gui.jobs.ListView
        @type media_files: gui.media.MediaFiles
        @type ignore_jobs_filter: trayjenkins.jobs.IgnoreJobsFilter
        @type qtgui: QtGuiFactory
        """
        self._view = view
        self._qtgui = qtgui
        self._ignore_jobs_filter = ignore_jobs_filter

        self._ignored_icon = media_files.ignored_icon()
        self._status_icons = {JobStatus.DISABLED: media_files.disabled_icon(),
                              JobStatus.FAILING: media_files.failing_icon(),
                              JobStatus.OK: media_files.ok_icon(),
                              JobStatus.UNKNOWN: media_files.unknown_icon()}

    def set_jobs(self, jobs):
        """
        @type jobs: [pyjenkins.job.Job]
        """
        items = []
        for job in jobs:
            if self._ignore_jobs_filter.ignoring(job.name):
                icon = self._ignored_icon
            else:
                icon = self._status_icons[job.status]
            items.append(self._qtgui.QListWidgetItem(icon, job.name))

        self._view.set_list(items)


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
