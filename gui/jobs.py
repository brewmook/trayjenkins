from PySide import QtCore, QtGui
from trayjenkins.event import Event
from trayjenkins.jobs import IView
from pyjenkins.job import JobStatus
from gui.qmock import QtGuiFactory


class ContextMenuFactory(object):

    def __init__(self, parent, qtgui=QtGuiFactory()):
        """
        @type parent: PySide.QtGui.Widget
        @type qtgui: QtGuiFactory
        """
        self._parent = parent
        self._qtgui = qtgui

    def create(self, job_model, ignore_callback, unignore_callback):
        """
        @type job_model: trayjenkins.jobs.JobModel
        @type ignore_callback: callable
        @type unignore_callback: callable
        """
        menu = self._qtgui.QMenu(self._parent)
        if job_model.ignored:
            action = self._qtgui.QAction('Cancel ignore', self._parent, triggered=unignore_callback)
        else:
            action = self._qtgui.QAction('Ignore', self._parent, triggered=ignore_callback)
        menu.addAction(action)
        return menu


class ListView(QtGui.QGroupBox):

    def right_click_event(self):
        """
        Listeners receive Event.fire(job_name:str, pos:PySide.QtCore.QPoint)
        @rtype: trayjenkins.event.IEvent
        """
        return self._right_click_event

    def __init__(self):
        QtGui.QGroupBox.__init__(self, "Jobs")

        self._right_click_event = Event()

        self._jobs = QtGui.QListWidget(self)
        self._jobs.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self._jobs.customContextMenuRequested.connect(self._on_custom_context_menu_requested)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self._jobs)
        self.setLayout(layout)

    def _on_custom_context_menu_requested(self, point):
        """
        @type point: PySide.QtCore.QPoint
        """
        item = self._jobs.itemAt(point)
        if item is not None:
            self._right_click_event.fire(item.text(), self._jobs.mapToGlobal(point))

    def set_list(self, items):
        """
        @type items: [PySide.QtGui.QListWidgetItem]
        """
        self._jobs.clear()
        for item in items:
            self._jobs.addItem(item)


class ListViewAdapter(IView):

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
                 menu_factory,
                 qtgui=QtGuiFactory()):
        """
        @type view: gui.jobs.ListView
        @type media_files: gui.media.MediaFiles
        @type menu_factory: gui.jobs.ContextMenuFactory
        @type qtgui: QtGuiFactory
        """
        self._view = view
        self._qtgui = qtgui
        self._menu_factory = menu_factory
        self._ignored_event = Event()
        self._unignored_event = Event()
        self._job_models = []

        view.right_click_event().register(self._on_view_right_click)

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
        self._job_models = job_models

    def _on_view_ignored(self, job_name):

        self._ignored_event.fire(job_name)

    def _on_view_unignored(self, job_name):

        self._unignored_event.fire(job_name)

    def _on_view_right_click(self, job_name, pos):
        """
        @type job_name: str
        @param pos: Absolute screen coordinates
        @type pos: PySide.QtCore.QPoint
        """
        menu = self._menu_factory.create(self._find_model(job_name),
                                         lambda: self._ignored_event.fire(job_name),
                                         lambda: self._unignored_event.fire(job_name))
        menu.popup(pos)

    def _find_model(self, job_name):
        result = None
        for model in self._job_models:
            if model.job.name == job_name:
                result = model
                break
        return result


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
