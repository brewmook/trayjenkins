class IModel(object):

    def status(self):
        """
        @rtype: str
        """

class IView(object):

    def statusRefreshEvent(self):
        """
        Event arguments: <none>
        @rtype: pyjenkins.interfaces.IEvent
        """

    def setStatus(self, status):
        """
        @type status: str
        """
