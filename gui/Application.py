import sys
import trayjenkins
from PySide import QtGui
from gui.status.TrayIconView import TrayIconView
from trayjenkins.status.Model import Model as StatusModel
from pyjenkins.Job import JobStatus

class FakeStatusReader(trayjenkins.status.interfaces.IStatusReader):

    def __init__(self):

        self._status= JobStatus.UNKNOWN

    def status(self, jenkins):

        return self._status


class MainWindow(QtGui.QDialog):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.createTrayIcon()
        self.createWidgets()
        self.layoutWidgets()

    def layoutWidgets(self):

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.statusOkButton)
        mainLayout.addWidget(self.statusFailingButton)
        mainLayout.addWidget(self.statusUnknownButton)
        self.setLayout(mainLayout)

    def createWidgets(self):

        self.statusOkButton= QtGui.QPushButton("Ok")
        self.statusOkButton.clicked.connect(self.onStatusOkButtonClicked)
        self.statusFailingButton= QtGui.QPushButton("Failing")
        self.statusFailingButton.clicked.connect(self.onStatusFailingButtonClicked)
        self.statusUnknownButton= QtGui.QPushButton("Unknown")
        self.statusUnknownButton.clicked.connect(self.onStatusUnknownButtonClicked)

    def onStatusOkButtonClicked(self):
        self.fakeStatusReader._status = JobStatus.OK
        self.statusModel.updateStatus()

    def onStatusFailingButtonClicked(self):
        self.fakeStatusReader._status = JobStatus.FAILING
        self.statusModel.updateStatus()

    def onStatusUnknownButtonClicked(self):
        self.fakeStatusReader._status = JobStatus.UNKNOWN
        self.statusModel.updateStatus()

    def createTrayIcon(self):
        from trayjenkins.status.Presenter import Presenter
        self.fakeStatusReader = FakeStatusReader()
        self.statusModel = StatusModel(None, self.fakeStatusReader)
        self.statusPresenter= Presenter(self.statusModel, TrayIconView(self, 5))


class Application(QtGui.QDialog):

    def __init__(self):

        self.application= QtGui.QApplication(sys.argv)

    def run(self):

        window = MainWindow()
        window.show()

        return self.application.exec_()

