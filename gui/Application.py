import sys
import trayjenkins
from PySide import QtGui, QtCore
from gui.status.TrayIconView import TrayIconView
from trayjenkins.status.Model import Model as StatusModel
from pyjenkins.Job import JobStatus

class FakeStatusReader(trayjenkins.status.interfaces.IStatusReader):

    def __init__(self):

        self._status= JobStatus.UNKNOWN

    def status(self):

        return self._status

class FakeStatusGroup(QtGui.QGroupBox):

    def __init__(self, fakeStatusReader):
        """
        @type fakeStatusReader: FakeStatusReader
        """
        QtGui.QGroupBox.__init__(self, "Fake status")

        self.fakeStatusReader = fakeStatusReader

        self.statusOkButton= QtGui.QPushButton("Ok")
        self.statusOkButton.clicked.connect(self.onStatusOkButtonClicked)
        self.statusFailingButton= QtGui.QPushButton("Failing")
        self.statusFailingButton.clicked.connect(self.onStatusFailingButtonClicked)
        self.statusUnknownButton= QtGui.QPushButton("Unknown")
        self.statusUnknownButton.clicked.connect(self.onStatusUnknownButtonClicked)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.statusOkButton)
        layout.addWidget(self.statusFailingButton)
        layout.addWidget(self.statusUnknownButton)
        self.setLayout(layout)

    def onStatusOkButtonClicked(self):
        self.fakeStatusReader._status = JobStatus.OK

    def onStatusFailingButtonClicked(self):
        self.fakeStatusReader._status = JobStatus.FAILING

    def onStatusUnknownButtonClicked(self):
        self.fakeStatusReader._status = JobStatus.UNKNOWN


class StatusUpdateThread(QtCore.QThread):

    def __init__(self, statusModel, *args, **kwargs):
        """
        @type statusModel: trayjenkins.status.interfaces.IModel
        """
        QtCore.QThread.__init__(self, *args, **kwargs)
        self.statusModel = statusModel

    def run(self):

        while True:
            self.sleep(5)
            self.statusModel.updateStatus()


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

