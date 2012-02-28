from pyjenkins.backend.http import Http
from pyjenkins.jenkins import Jenkins, JenkinsFactory
from pyjenkins.server import Server
from trayjenkins.event import Event

class IModel(object):

    def update_jobs(self):
        """
        @rtype: None
        """

    def jobs_updated_event(self):
        """
        Listeners receive Event.fire([pyjenkins.job.Job])
        @rtype: trayjenkins.event.IEvent
        """

class IView(object):
    
    def set_jobs(self, jobs):
        """
        @type jobs: [pyjenkins.job.Job]
        """

class IFilter(object):

    def filter(self, jobs):
        """
        @type jobs: [pyjenkins.job.Job]
        @rtype: [pyjenkins.job.Job]
        """

class Presenter(object):

    def __init__(self, model, view):
        """
        @type model: trayjenkins.jobs.IModel
        @type view:  trayjenkins.jobs.IView
        """
        self._model= model
        self._view= view
        model.jobs_updated_event().register(self._on_model_jobs_changed)

    def _on_model_jobs_changed(self, jobs):
        
        self._view.set_jobs(jobs)


class NoFilter(IFilter):

    def filter(self, jobs):

        return jobs


class Model(IModel):

    def __init__(self,
                 server,
                 jobs_filter=NoFilter(),
                 jenkins_factory=JenkinsFactory(),
                 event=Event()):
        """
        @type server: pyjenkins.server.Server
        @type jobs_filter: trayjenkins.jobs.IFilter
        @type jenkins_factory: pyjenkins.interfaces.IJenkinsFactory
        @type event: trayjenkins.event.IEvent
        """
        self._jobs_filter = jobs_filter
        self._jenkins = jenkins_factory.create(server)
        self._jobs_updated_event = event
        self._jobs = None

    def update_jobs(self):
        """
        @rtype: None
        """
        jobs = self._jenkins.list_jobs()
        filtered = self._jobs_filter.filter(jobs)
        if self._jobs != filtered:
            self._jobs = filtered
            self._jobs_updated_event.fire(jobs)

    def jobs_updated_event(self):
        """
        Listeners receive Event.fire([pyjenkins.job.Job])
        @rtype: trayjenkins.event.IEvent
        """
        return self._jobs_updated_event


class IgnoreJobsFilter(IFilter):

    def __init__(self):

        self._ignores = set()

    def filter(self, jobs):

        return [job for job in jobs if job.name not in self._ignores]

    def ignore(self, jobName):

        self._ignores.add(jobName)

    def unignore(self, jobName):

        self._ignores.discard(jobName)

    def ignoring(self, jobName):

        return jobName in self._ignores
