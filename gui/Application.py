import sys
import trayjenkins
from PySide import QtGui
from gui.status.TrayIconView import TrayIconView
from pyjenkins.Job import JobStatus

class FakeStatusModel(trayjenkins.status.interfaces.IModel):

    def __init__(self):
        self._status= JobStatus.UNKNOWN

    def status(self):

        if self._status is JobStatus.FAILING:
            self._status= JobStatus.OK
        elif self._status is JobStatus.OK:
            self._status= JobStatus.UNKNOWN
        elif self._status is JobStatus.UNKNOWN:
            self._status= JobStatus.FAILING

        return self._status

class MainWindow(QtGui.QDialog):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.createTrayIcon()
        self.createWidgets()
        self.layoutWidgets()

    def layoutWidgets(self):

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.refreshButton)
        self.setLayout(mainLayout)

    def createWidgets(self):

        self.refreshButton= QtGui.QPushButton("Refresh")
        self.refreshButton.clicked.connect(self.onRefreshButtonClicked)

        #self.iconComboBox = QtGui.QComboBox()
        #self.iconComboBox.addItem(QtGui.QIcon('images/status/failing.svg'), "Failing")
        #self.iconComboBox.addItem(QtGui.QIcon('images/status/ok.svg'),      "Ok")
        #self.iconComboBox.addItem(QtGui.QIcon('images/status/unknown.svg'), "Unknown")

    def onRefreshButtonClicked(self):
        # This is hackery. The model obviously needs fixed.
        self.statusView.statusRefreshEvent().fire()

    def createTrayIcon(self):
        from trayjenkins.status.Presenter import Presenter
        model= FakeStatusModel()
        self.statusView= TrayIconView(self, 5)
        self.statusPresenter= Presenter(model, self.statusView)


class Application(QtGui.QDialog):

    def __init__(self):

        self.application= QtGui.QApplication(sys.argv)

    def run(self):

        window = MainWindow()
        window.show()

        return self.application.exec_()

