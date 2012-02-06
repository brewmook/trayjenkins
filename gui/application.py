import os
import sys
from optparse import OptionParser
from PySide import QtGui
from gui.jobs.view import JobsListView
from gui.jobs.fake import FakeJobsModel
from gui.status.view import TrayIconView, SoundView, MultiView
from gui.timer.jobsupdate import JobsUpdateTimer
from trayjenkins.jobs.model import Model as JobsModel
from trayjenkins.jobs.presenter import Presenter as JobsPresenter
from trayjenkins.status.model import Model as StatusModel
from trayjenkins.status.statusreader import StatusReader
from trayjenkins.status.presenter import Presenter as StatusPresenter
from pyjenkins.server import Server

class MainWindow(QtGui.QDialog):

    def __init__(self, jenkinsHost, executablePath):
        super(MainWindow, self).__init__()

        self.createActions()
        self.createJobsMVP(jenkinsHost)
        self.createTrayIcon(executablePath)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.jobsView)
        self.setLayout(mainLayout)

        self.jobsUpdateTimer = JobsUpdateTimer(self.jobsModel, 5, self)

    def createJobsMVP(self, jenkinsHost):

        if jenkinsHost == 'FAKE':
            self.jobsModel = FakeJobsModel()
        else:
            self.jobsModel = JobsModel(Server(jenkinsHost, '', ''))

        self.jobsView = JobsListView()
        self.jobsPresenter = JobsPresenter(self.jobsModel, self.jobsView)

    def createActions(self):

        self.quitAction = QtGui.QAction("&Quit", self, triggered=QtGui.qApp.quit)
        self.showControlsAction = QtGui.QAction("&Show controls", self, triggered=self.showNormal)

    def createTrayIcon(self, executablePath):

        self.trayMenu = QtGui.QMenu(self)
        self.trayMenu.addAction(self.showControlsAction)
        self.trayMenu.addAction(self.quitAction)

        view = MultiView([TrayIconView(self, self.trayMenu, executablePath),
                          SoundView(self, executablePath)])
        self.statusModel = StatusModel(self.jobsModel, StatusReader())
        self.statusPresenter = StatusPresenter(self.statusModel, view)

    def closeEvent(self, event):
        self.hide()
        event.ignore()

class Application(QtGui.QDialog):

    def __init__(self):

        self.application= QtGui.QApplication(sys.argv)
        self.application.setApplicationName('Trayjenkins')

    def run(self):

        jenkinsHost = self.parseOptions()
        path = self.executablePath()

        window = MainWindow(jenkinsHost, path)

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

