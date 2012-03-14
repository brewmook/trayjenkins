from trayjenkins.event import Event
from pyjenkins.job import JobStatus


class IModel(object):

    def status_changed_event(self):
        """
        Event arguments: (status:str, message:str)
        @rtype: trayjenkins.event.IEvent
        """


class IView(object):

    def set_status(self, status, message):
        """
        @type status: str
        @type message: str
        """


class IStatusReader(object):

    def status(self, jobs):
        """
        @type jobs: [pyjenkins.job.Job]
        @return String from pyjenkins.job.JobStatus
        @rtype: str
        """


class IMessageComposer(object):

    def message(self, jobs):
        """
        @type jobs: [pyjenkins.job.Job]
        @return Brief message describing the job statuses.
        @rtype: str
        """


class Presenter(object):

    def __init__(self, model, view):
        """
        @type model: trayjenkins.status.IModel
        @type view:  trayjenkins.status.IView
        """
        self._model = model
        self._view = view
        model.status_changed_event().register(self._on_model_status_changed)

    def _on_model_status_changed(self, status, message):

        self._view.set_status(status, message)


class DefaultMessageComposer(IMessageComposer):

    def message(self, jobs):
        """
        @type jobs: [pyjenkins.job.Job]
        @return Brief message describing the job statuses.
        @rtype: str
        """
        result = ''
        if jobs is not None:
            if len(jobs) == 0:
                result = 'No jobs'
            else:
                failing = [job.name for job in jobs if job.status == JobStatus.FAILING]
                if failing:
                    result = 'FAILING:\n' + '\n'.join(failing)
                else:
                    result = 'All active jobs pass'

        return result


class StatusReader(IStatusReader):

    def status(self, jobs):
        """
        @type jobs: [pyjenkins.job.Job]
        @return String from pyjenkins.job.JobStatus
        @rtype: str
        """
        result = JobStatus.OK

        if jobs is None:
            result = JobStatus.UNKNOWN
        else:
            for job in jobs:
                if job.status is JobStatus.FAILING:
                    result = JobStatus.FAILING
                    break

        return result


class Model(IModel):

    def __init__(self,
                 jobs_model,
                 jobs_filter,
                 message_composer=DefaultMessageComposer(),
                 status_reader=StatusReader(),
                 status_changed_event=Event()):
        """
        @type jobs_model: trayjenkins.jobs.IModel
        @type jobs_filter: trayjenkins.jobs.IFilter
        @type message_composer: trayjenkins.status.IMessageComposer
        @type status_reader: trayjenkins.status.IStatusReader
        @type status_changed_event: trayjenkins.event.Event
        """
        self._jobs_filter = jobs_filter
        self._message_composer = message_composer
        self._status_reader = status_reader
        self._status_changed_event = status_changed_event
        self._lastStatus = JobStatus.UNKNOWN
        self._lastMessage = None

        jobs_model.jobs_updated_event().register(self._on_jobs_updated)

    def _on_jobs_updated(self, job_models):
        job_models = self._jobs_filter.filter_jobs(job_models)
        jobs = [model.job for model in job_models]
        status = self._status_reader.status(jobs)
        message = self._message_composer.message(jobs)
        if self._lastStatus != status or self._lastMessage != message:
            self._status_changed_event.fire(status, message)
        self._lastStatus = status
        self._lastMessage = message

    def status_changed_event(self):
        """
        Event arguments: status:str
        @rtype: trayjenkins.event.IEvent
        """
        return self._status_changed_event
