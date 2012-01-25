class Presenter(object):

    def __init__(self, model, view):
        """
        @type model: trayjenkins.jobs.interfaces.IModel
        @type view:  trayjenkins.jobs.interfaces.IView
        """
        self._model= model
        self._view= view
        model.jobsUpdatedEvent().register(self.onModelJobsChanged)

    def onModelJobsChanged(self, jobs):
        
        self._view.setJobs(jobs)
