import os
import sys
from optparse import OptionParser
from PySide import QtCore, QtGui

import gui.fake
import gui.jobs
import gui.media
import gui.status

from trayjenkins.jobs import Model as JobsModel, Presenter as JobsPresenter, IgnoreJobsFilter
from trayjenkins.status import Model as StatusModel, Presenter as StatusPresenter
from pyjenkins.job import JobStatus
from pyjenkins.server import Server
from trayjenkins import __version__
from pyjenkins.jenkins import JenkinsFactory


class TrayIcon(object):

    def __init__(self,
                 parent,
                 media_files,
                 show_controls_action,
                 show_jenkins_action,
                 quit_action,
                 jobs_model,
                 ignore_jobs_filter):

        self._show_controls_action = show_controls_action
        self._show_jenkins_action = show_jenkins_action

        self._tray_menu = QtGui.QMenu(parent)
        self._tray_menu.addAction(show_controls_action)
        self._tray_menu.addAction(show_jenkins_action)
        self._tray_menu.addAction(quit_action)

        self._tray_icon = QtGui.QSystemTrayIcon(parent)
        self._tray_icon.setContextMenu(self._tray_menu)
        self._tray_icon.messageClicked.connect(self._on_message_clicked)
        self._tray_icon.activated.connect(self._on_activated)

        tray_icon_view = gui.status.TrayIconView(self._tray_icon)
        tray_icon_view_adapter = gui.status.TrayIconViewAdapter(tray_icon_view, media_files)
        status_view = gui.status.MultiView([tray_icon_view_adapter,
                                            gui.status.SoundView(parent, media_files)])
        self.status_model = StatusModel(jobs_model, jobs_filter=ignore_jobs_filter)
        self.status_presenter = StatusPresenter(self.status_model, status_view)
        status_view.set_status(JobStatus.UNKNOWN, None)

        self._tray_icon.show()

    def _on_activated(self, reason):
        if reason in (QtGui.QSystemTrayIcon.Trigger, QtGui.QSystemTrayIcon.DoubleClick):
            self._show_controls_action.trigger()

    def _on_message_clicked(self):
        self._show_jenkins_action.trigger()


class MainWindow(QtGui.QDialog):

    def __init__(self, jenkins_host, media_files):
        super(MainWindow, self).__init__()

        self._ignore_jobs_filter = IgnoreJobsFilter()

        self._create_actions()
        self._create_jobs_mvp(jenkins_host, media_files, self._ignore_jobs_filter)

        self._trayIcon = TrayIcon(self,
                                  media_files,
                                  self._show_controls_action,
                                  self._show_jenkins_action,
                                  self._quitAction,
                                  self._jobs_model,
                                  self._ignore_jobs_filter)

        main_layout = QtGui.QVBoxLayout()
        main_layout.addWidget(self._jobs_view)
        self.setLayout(main_layout)

        self._jobs_update_timer = gui.jobs.UpdateTimer(self._jobs_model, 15, self)

        self.setWindowTitle("TrayJenkins (%s)" % __version__)
        self.resize(640, 480)

    def _create_jobs_mvp(self, jenkins_host, media_files, ignore_jobs_filter):

        if jenkins_host == 'FAKE':
            jenkins = gui.fake.Jenkins()
            self._jenkins_url = QtCore.QUrl('https://github.com/coolhandmook/trayjenkins')
        else:
            server = Server(jenkins_host, '', '')
            jenkins = JenkinsFactory().create(server)
            self._jenkins_url = QtCore.QUrl(jenkins_host)

        self._jobs_model = JobsModel(jenkins)
        self._jobs_view = gui.jobs.ListView(ignore_jobs_filter)
        menu_factory = gui.jobs.ContextMenuFactory(self._jobs_view)
        view_adapter = gui.jobs.ListViewAdapter(self._jobs_view, media_files, menu_factory)
        self._jobs_presenter = JobsPresenter(self._jobs_model, view_adapter)

    def _create_actions(self):

        self._quitAction = QtGui.QAction("&Quit", self, triggered=QtGui.qApp.quit)
        self._show_controls_action = QtGui.QAction("Show &Controls", self, triggered=self.showNormal)
        self._show_jenkins_action = QtGui.QAction("Show &Jenkins", self, triggered=self._open_jenkins_url)

    def closeEvent(self, event):
        self.hide()
        event.ignore()

    def _open_jenkins_url(self):
        QtGui.QDesktopServices.openUrl(self._jenkins_url)


class Application(QtGui.QDialog):

    def __init__(self):

        self._application = QtGui.QApplication(sys.argv)
        self._application.setApplicationName('Trayjenkins')

    def run(self):

        jenkins_host = self._parse_options()
        media_files = gui.media.MediaFiles(self._executable_path())

        window = MainWindow(jenkins_host, media_files)  # @UnusedVariable

        return self._application.exec_()

    def _parse_options(self):

        parser = OptionParser(usage='usage: %prog [options] host')
        (options, args) = parser.parse_args()  # @UnusedVariable

        if len(args) is 1:
            jenkins_host = args[0]
        else:
            parser.print_help()
            sys.exit(1)

        return jenkins_host

    def _executable_path(self):

        path = ''
        try:
            path = sys._MEIPASS  # @UndefinedVariable
        except AttributeError:
            path = os.path.abspath(".")

        return path
