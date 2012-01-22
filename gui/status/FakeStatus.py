from PySide import QtGui
from pyjenkins.Job import JobStatus
from trayjenkins.status.interfaces import IStatusReader

class FakeStatusReader(IStatusReader):

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