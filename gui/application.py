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
        self.status_model = StatusModel(jobs_model, jobsFilter=ignore_jobs_filter)
        self.status_presenter = StatusPresenter(self.status_model, status_view)
        status_view.setStatus(JobStatus.UNKNOWN, None)

        self._tray_icon.show()

    def _on_activated(self, reason):
        if reason in (QtGui.QSystemTrayIcon.Trigger, QtGui.QSystemTrayIcon.DoubleClick):
            self._show_controls_action.trigger()

    def _on_message_clicked(self):
        self._show_jenkins_action.trigger()


class MainWindow(QtGui.QDialog):

    def __init__(self, jenkinsHost, mediaFiles):
        super(MainWindow, self).__init__()

        self.ignoreJobsFilter = IgnoreJobsFilter()

        self.createActions()
        self.createJobsMVP(jenkinsHost, mediaFiles, self.ignoreJobsFilter)

        self.trayIcon = TrayIcon(self,
                                 mediaFiles,
                                 self.showControlsAction,
                                 self.showJenkinsAction,
                                 self.quitAction,
                                 self.jobsModel,
                                 self.ignoreJobsFilter)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.jobsView)
        self.setLayout(mainLayout)

        self.jobsUpdateTimer = gui.jobs.UpdateTimer(self.jobsModel, 15, self)

        self.setWindowTitle("TrayJenkins (%s)" % __version__)
        self.resize(640, 480)

    def createJobsMVP(self, jenkinsHost, mediaFiles, ignoreJobsFilter):

        if jenkinsHost == 'FAKE':
            self.jobsModel = gui.fake.JobsModel()
            self.jenkinsUrl = QtCore.QUrl('https://github.com/coolhandmook/trayjenkins')
        else:
            self.jobsModel = JobsModel(Server(jenkinsHost, '', ''), ignoreJobsFilter)
            self.jenkinsUrl = QtCore.QUrl(jenkinsHost)

        self.jobsView = gui.jobs.ListView(mediaFiles, ignoreJobsFilter)
        self.jobsPresenter = JobsPresenter(self.jobsModel, self.jobsView)

    def createActions(self):

        self.quitAction = QtGui.QAction("&Quit", self, triggered=QtGui.qApp.quit)
        self.showControlsAction = QtGui.QAction("Show &Controls", self, triggered=self.showNormal)
        self.showJenkinsAction = QtGui.QAction("Show &Jenkins", self, triggered=self.openJenkinsUrl)

    def closeEvent(self, event):
        self.hide()
        event.ignore()

    def openJenkinsUrl(self):
        QtGui.QDesktopServices.openUrl(self.jenkinsUrl)


class Application(QtGui.QDialog):

    def __init__(self):

        self.application= QtGui.QApplication(sys.argv)
        self.application.setApplicationName('Trayjenkins')

    def run(self):

        jenkinsHost = self.parseOptions()
        mediaFiles = gui.media.MediaFiles(self.executablePath())

        window = MainWindow(jenkinsHost, mediaFiles)

        return self.application.exec_()

    def parseOptions(self):

        parser = OptionParser(usage='usage: %prog [options] host')
        (options, args) = parser.parse_args()

        if len(args) is 1:
            jenkinsHost = args[0]
        else:
            parser.print_help()
            sys.exit(1)

        return jenkinsHost

    def executablePath(self):

        path = ''
        try:
            path = sys._MEIPASS
        except AttributeError:
            path = os.path.abspath(".")
            
        return path
