class IModel(object):

    def updateJobs(self):
        """
        @rtype: None
        """

    def jobsUpdatedEvent(self):
        """
        Listeners receive Event.fire([pyjenkins.job.Job])
        @rtype: pyjenkins.interfaces.IEvent
        """
