from PySide import QtCore

class StatusUpdateThread(QtCore.QThread):

    def __init__(self, statusModel):
        """
        @type statusModel: trayjenkins.status.interfaces.IModel
        """
        QtCore.QThread.__init__(self)
        self.statusModel = statusModel

    def run(self):

        while True:
            self.sleep(5)
            self.statusModel.updateStatus()