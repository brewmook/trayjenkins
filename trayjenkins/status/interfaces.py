class IModel(object):

    def updateStatus(self):
        """
        @rtype: None
        """

    def statusChangedEvent(self):
        """
        Event arguments: status:str
        @rtype: pyjenkins.interfaces.IEvent
        """

class IView(object):

    def setStatus(self, status):
        """
        @type status: str
        """

class IStatusReader(object):

    def status(self, jenkins):
        """
        @type jenkins: pyjenkins.interfaces.IJenkins
        """