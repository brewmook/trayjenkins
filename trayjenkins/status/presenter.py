class Presenter(object):

    def __init__(self, model, view):
        """
        @type model: trayjenkins.status.interfaces.IModel
        @type view:  trayjenkins.status.interfaces.IView
        """
        self._model= model
        self._view= view
        model.statusChangedEvent().register(self.onModelStatusChanged)

    def onModelStatusChanged(self, status):

        self._view.setStatus(status)
