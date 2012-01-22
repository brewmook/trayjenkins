import sys
from PySide import QtGui
from gui.status.FakeStatus import FakeStatusReader, FakeStatusGroup
from gui.status.StatusUpdateThread import StatusUpdateThread
from gui.status.TrayIconView import TrayIconView
from trayjenkins.status.Model import Model as StatusModel

class MainWindow(QtGui.QDialog):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.createStatusReader()
        self.createTrayIcon()
        self.layoutWidgets()

        self.statusThread = StatusUpdateThread(self.statusModel)
        self.statusThread.start()

    def layoutWidgets(self):

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.statusReaderView)
        self.setLayout(mainLayout)

    def createStatusReader(self):

        self.statusReader = FakeStatusReader()
        self.statusReaderView = FakeStatusGroup(self.statusReader)

    def createTrayIcon(self):
        from trayjenkins.status.Presenter import Presenter
        self.statusModel = StatusModel(self.statusReader)
        self.statusPresenter= Presenter(self.statusModel, TrayIconView(self, 5))


class Application(QtGui.QDialog):

    def __init__(self):

        self.application= QtGui.QApplication(sys.argv)

    def run(self):

        window = MainWindow()
        window.show()

        return self.application.exec_()

