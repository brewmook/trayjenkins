import sys
from PySide import QtGui
from gui.status.view import TrayIconView
from gui.thread.jobsupdate import JobsUpdateThread
from trayjenkins.jobs.model import Model as JobsModel
from trayjenkins.status.model import Model as StatusModel
from trayjenkins.status.statusreader import StatusReader
from trayjenkins.status.presenter import Presenter as StatusPresenter
from pyjenkins.server import Server

class MainWindow(QtGui.QDialog):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.jobsModel = JobsModel(Server('http://ci.jenkins-ci.org/', '', ''))

        self.createTrayIcon()

        self.jobsUpdateThread = JobsUpdateThread(self.jobsModel)
        self.jobsUpdateThread.start()

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

        return self.application.exec_()

