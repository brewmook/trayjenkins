import os
import sys
from optparse import OptionParser
from PySide import QtCore, QtGui

import gui.fake
import gui.jobs
import gui.media
import gui.status

from trayjenkins.jobs import Model as JobsModel, Presenter as JobsPresenter
from trayjenkins.status import Model as StatusModel, Presenter as StatusPresenter
from pyjenkins.job import JobStatus
from pyjenkins.server import Server
from trayjenkins import __version__

class TrayIcon(object):

    def __init__(self, parent, mediaFiles, showControlsAction, showJenkinsAction, quitAction, jobsModel):

        self.showControlsAction = showControlsAction
        self.showJenkinsAction = showJenkinsAction

        self.trayMenu = QtGui.QMenu(parent)
        self.trayMenu.addAction(showControlsAction)
        self.trayMenu.addAction(showJenkinsAction)
        self.trayMenu.addAction(quitAction)

        self.trayIcon = QtGui.QSystemTrayIcon(parent)
        self.trayIcon.setContextMenu(self.trayMenu)
        self.trayIcon.messageClicked.connect(self.onMessageClicked)
        self.trayIcon.activated.connect(self.onActivated)

        trayIconView = gui.status.TrayIconView(self.trayIcon)
        trayIconViewAdapter = gui.status.TrayIconViewAdapter(trayIconView, mediaFiles)
        statusView = gui.status.MultiView([trayIconViewAdapter,
                                           gui.status.SoundView(parent, mediaFiles)])
        self.statusModel = StatusModel(jobsModel)
        self.statusPresenter = StatusPresenter(self.statusModel, statusView)
        statusView.setStatus(JobStatus.UNKNOWN, None)

        self.trayIcon.show()

    def onActivated(self, reason):
        if reason in (QtGui.QSystemTrayIcon.Trigger, QtGui.QSystemTrayIcon.DoubleClick):
            self.showControlsAction.trigger()

    def onMessageClicked(self):
        self.showJenkinsAction.trigger()


class MainWindow(QtGui.QDialog):

    def __init__(self, jenkinsHost, mediaFiles):
        super(MainWindow, self).__init__()

        self.createActions()
        self.createJobsMVP(jenkinsHost, mediaFiles)

        self.trayIcon = TrayIcon(self,
                                 mediaFiles,
                                 self.showControlsAction,
                                 self.showJenkinsAction,
                                 self.quitAction,
                                 self.jobsModel)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.jobsView)
        self.setLayout(mainLayout)

        self.jobsUpdateTimer = gui.jobs.UpdateTimer(self.jobsModel, 15, self)

        self.setWindowTitle("TrayJenkins (%s)" % __version__)
        self.resize(640, 480)

    def createJobsMVP(self, jenkinsHost, mediaFiles):

        if jenkinsHost == 'FAKE':
            self.jobsModel = gui.fake.JobsModel()
            self.jenkinsUrl = QtCore.QUrl('https://github.com/coolhandmook/trayjenkins')
        else:
            self.jobsModel = JobsModel(Server(jenkinsHost, '', ''))
            self.jenkinsUrl = QtCore.QUrl(jenkinsHost)

        self.jobsView = gui.jobs.ListView(mediaFiles)
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
