class Presenter(object):

    def __init__(self, model, view):
        """
        @type model: trayjenkins.status.interfaces.IModel
        @type view:  trayjenkins.status.interfaces.IView
        """
        self._model= model
        self._view= view
        view.statusRefreshEvent().register(self.onViewStatusRefresh)

    def onViewStatusRefresh(self):

        status= self._model.status()
        self._view.setStatus(status)
