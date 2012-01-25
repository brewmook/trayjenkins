import sys
from PySide import QtGui
from gui.jobs.view import JobsListView
from gui.status.view import TrayIconView
from gui.thread.jobsupdate import JobsUpdateThread
from trayjenkins.jobs.model import Model as JobsModel
from trayjenkins.jobs.presenter import Presenter as JobsPresenter
from trayjenkins.status.model import Model as StatusModel
from trayjenkins.status.statusreader import StatusReader
from trayjenkins.status.presenter import Presenter as StatusPresenter
from pyjenkins.server import Server

class MainWindow(QtGui.QDialog):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.createJobsMVP()
        self.createTrayIcon()

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.jobsView)
        self.setLayout(mainLayout)

        self.jobsUpdateThread = JobsUpdateThread(self.jobsModel)
        self.jobsUpdateThread.start()

    def createJobsMVP(self):

        self.jobsModel = JobsModel(Server('http://ci.jenkins-ci.org/', '', ''))
        self.jobsView = JobsListView()
        self.jobsPresenter = JobsPresenter(self.jobsModel, self.jobsView)

    def createTrayIcon(self):

        self.quitAction = QtGui.QAction("&Quit", self, triggered=QtGui.qApp.quit)

        self.trayMenu = QtGui.QMenu(self)
        self.trayMenu.addAction(self.quitAction)

        self.statusModel = StatusModel(self.jobsModel, StatusReader())
        self.statusPresenter = StatusPresenter(self.statusModel, TrayIconView(self, 5, self.trayMenu))


class Application(QtGui.QDialog):

    def __init__(self):

        self.application= QtGui.QApplication(sys.argv)

    def run(self):

        window = MainWindow()
        window.show()

        return self.application.exec_()

