class Presenter(object):

    def __init__(self, model, view):
        """
        @type model: trayjenkins.status.interfaces.IModel
        @type view:  trayjenkins.status.interfaces.IView
        """
        model.statusChangedEvent().register(self.onModelStatusChanged)
        self._model= model
        self._view= view

    def onModelStatusChanged(self, status):

        self._view.updateStatus(status)
