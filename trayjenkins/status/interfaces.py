class IModel(object):

    def statusChangedEvent(self):
        """
        @rtype pyjenkins.interfaces.IEvent
        """

class IView(object):

    def updateStatus(self, status):
        """
        @type status: str
        """
