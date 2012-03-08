from pyjenkins.jenkins import JenkinsFactory
from trayjenkins.event import Event
import copy


class JobModel(object):

    def __init__(self, job, ignored):
        """
        @type job: pyjenkins.job.Job
        @type ignored: bool
        """
        self.job = job
        self.ignored = ignored

    def __eq__(self, other):
        """
        @type other: trayjenkins.jobs.JobModel
        @rtype: bool
        """
        return self.job == other.job \
           and self.ignored == other.ignored

    def __repr__(self):
        """
        @rtype: str
        """
        return 'JobModel(job=%r,ignored=%r)' % (self.job, self.ignored)


class IModel(object):

    def update_jobs(self):
        """
        @rtype: None
        """

    def ignore_job(self, job_name):
        """
        @type job_name: str
        """

    def unignore_job(self, job_name):
        """
        @type job_name: str
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

    def filter_jobs(self, jobs):
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
        self._model = model
        self._view = view
        model.jobs_updated_event().register(self._on_model_jobs_changed)

    def _on_model_jobs_changed(self, jobs):

        self._view.set_jobs(jobs)


class NoFilter(IFilter):

    def filter_jobs(self, jobs):

        return jobs


class ModelReplacement(IModel):

    def __init__(self, jenkins, jobs_updated_event=Event()):

        self._jenkins = jenkins
        self._jobs_updated_event = jobs_updated_event
        self._models = []
        self._ignore = set()

    def update_jobs(self):
        """
        @rtype: None
        """
        jobs = self._jenkins.list_jobs()
        models = [JobModel(job, job.name in self._ignore) for job in jobs]
        self._update_models(models)

    def ignore_job(self, job_name):
        """
        @type job_name: str
        """
        self._ignore.add(job_name)
        self._set_ignore_status(job_name, True)

    def unignore_job(self, job_name):
        """
        @type job_name: str
        """
        self._ignore.remove(job_name)
        self._set_ignore_status(job_name, False)

    def jobs_updated_event(self):
        """
        Listeners receive Event.fire([pyjenkins.job.Job])
        @rtype: trayjenkins.event.IEvent
        """
        return self._jobs_updated_event

    def _set_ignore_status(self, job_name, ignored):
        models = copy.deepcopy(self._models)
        for model in models:
            if model.job.name == job_name:
                model.ignored = ignored
        self._update_models(models)

    def _update_models(self, models):
        if models != self._models:
            self._jobs_updated_event.fire(models)
            self._models = models


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
        filtered = self._jobs_filter.filter_jobs(jobs)
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

    def filter_jobs(self, jobs):
        """
        @type jobs: [pyjenkins.job.Job]
        @rtype: [pyjenkins.job.Job]
        """
        return [job for job in jobs if job.name not in self._ignores]

    def ignore(self, job_name):
        """
        @type job_name: str
        """
        self._ignores.add(job_name)

    def unignore(self, job_name):
        """
        @type job_name: str
        """
        self._ignores.discard(job_name)

    def ignoring(self, job_name):
        """
        @type jobName: str
        @rtype: bool
        """
        return job_name in self._ignores
