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


class IErrorLogger(object):

    def log_error(self, error):
        """
        @type error: str
        """


class IModel(object):

    def update_jobs(self):
        """
        @rtype: None
        """

    def disable_job(self, job_name):
        """
        @type job_name: str
        """

    def enable_job(self, job_name):
        """
        @type job_name: str
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

    def job_enabled_event(self):
        """
        Listeners receive Event.fire(job_name:str)
        @rtype: trayjenkins.event.IEvent
        """

    def job_disabled_event(self):
        """
        Listeners receive Event.fire(job_name:str)
        @rtype: trayjenkins.event.IEvent
        """

    def job_ignored_event(self):
        """
        Listeners receive Event.fire(job_name:str)
        @rtype: trayjenkins.event.IEvent
        """

    def job_unignored_event(self):
        """
        Listeners receive Event.fire(job_name:str)
        @rtype: trayjenkins.event.IEvent
        """

    def set_jobs(self, jobs):
        """
        @type jobs: [trayjenkins.jobs.JobModel]
        """


class IFilter(object):

    def filter_jobs(self, job_models):
        """
        @type jobs: [trayyjenkins.jobs.JobModel]
        @rtype: [tryyjenkins.jobs.JobModel]
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
        view.job_ignored_event().register(self._on_view_job_ignored)
        view.job_unignored_event().register(self._on_view_job_unignored)
        view.job_enabled_event().register(self._on_view_job_enabled)
        view.job_disabled_event().register(self._on_view_job_disabled)

    def _on_model_jobs_changed(self, jobs):

        self._view.set_jobs(jobs)

    def _on_view_job_ignored(self, job_name):

        self._model.ignore_job(job_name)

    def _on_view_job_unignored(self, job_name):

        self._model.unignore_job(job_name)

    def _on_view_job_enabled(self, job_name):

        self._model.enable_job(job_name)

    def _on_view_job_disabled(self, job_name):

        self._model.disable_job(job_name)


class Model(IModel):

    def __init__(self, jenkins, error_logger, jobs_updated_event=Event()):

        self._jenkins = jenkins
        self._error_logger = error_logger
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

    def enable_job(self, job_name):
        """
        @type job_name: str
        """
        if not self._jenkins.enable_job(job_name):
            self._error_logger.log_error("Failed to enable job '%s', check username and/or password" % job_name)

    def disable_job(self, job_name):
        """
        @type job_name: str
        """
        if not self._jenkins.disable_job(job_name):
            self._error_logger.log_error("Failed to disable job '%s', check username and/or password" % job_name)

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


class IgnoreJobsFilter(IFilter):

    def filter_jobs(self, job_models):
        """
        @type jobs: [trayyjenkins.jobs.JobModel]
        @rtype: [tryyjenkins.jobs.JobModel]
        """
        return [model for model in job_models if not model.ignored]
