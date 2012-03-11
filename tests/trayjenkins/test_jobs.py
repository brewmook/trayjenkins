import mox
from unittest import TestCase

from pyjenkins.jenkins import Jenkins
from pyjenkins.job import Job, JobStatus
from trayjenkins.event import Event, IEvent
from trayjenkins.jobs import IModel, IView, Presenter, Model, IgnoreJobsFilter,\
    JobModel


class JobModelTests(TestCase):

    def test_constructor_JobAttributeMatchesThatPassedIn(self):

        model = JobModel('job instance', 'whatever')
        self.assertEqual('job instance', model.job)

    def test_constructor_IgnoredAttributeMatchesThatPassedIn(self):

        model = JobModel('whatever', 'job is ignored')
        self.assertEqual('job is ignored', model.ignored)

    def test_equalityop_TwoEquivalentObjects_ReturnTrue(self):

        job = Job('something', JobStatus.FAILING)
        modelOne = JobModel(job, False)
        modelTwo = JobModel(job, False)

        self.assertTrue(modelOne == modelTwo)

    def test_equalityop_JobsDiffer_ReturnFalse(self):

        jobOne = Job('something', JobStatus.FAILING)
        jobTwo = Job('blah', JobStatus.DISABLED)
        modelOne = JobModel(jobOne, False)
        modelTwo = JobModel(jobTwo, False)

        self.assertFalse(modelOne == modelTwo)

    def test_equalityop_IgnoredDiffers_ReturnFalse(self):

        job = Job('something', JobStatus.FAILING)
        modelOne = JobModel(job, False)
        modelTwo = JobModel(job, True)

        self.assertFalse(modelOne == modelTwo)

    def test_repr_ReturnsSensibleResult(self):

        model = JobModel('fake job', False)
        self.assertEquals("JobModel(job='fake job',ignored=False)", model.__repr__())


class JobsPresenterTests(TestCase):

    def test_Constructor_ModelFiresJobsUpdatedEvent_ViewSetJobsCalled(self):

        mocks = mox.Mox()

        jobs = 'list of jobs'
        model = mocks.CreateMock(IModel)
        view = mocks.CreateMock(IView)
        jobs_updated_event = Event()

        model.jobs_updated_event().AndReturn(jobs_updated_event)
        view.job_ignored_event().InAnyOrder().AndReturn(Event())
        view.job_unignored_event().InAnyOrder().AndReturn(Event())
        view.job_enabled_event().InAnyOrder().AndReturn(Event())
        view.job_disabled_event().InAnyOrder().AndReturn(Event())
        view.set_jobs(jobs)

        mocks.ReplayAll()

        presenter = Presenter(model, view)  # @UnusedVariable
        jobs_updated_event.fire(jobs)

        mox.Verify(view)

    def test_Constructor___View_fires_job_ignored_event___Model_ignore_job_called(self):

        mocks = mox.Mox()

        model = mocks.CreateMock(IModel)
        view = mocks.CreateMock(IView)
        job_ignored_event = Event()

        model.jobs_updated_event().AndReturn(Event())
        view.job_ignored_event().InAnyOrder().AndReturn(job_ignored_event)
        view.job_unignored_event().InAnyOrder().AndReturn(Event())
        view.job_enabled_event().InAnyOrder().AndReturn(Event())
        view.job_disabled_event().InAnyOrder().AndReturn(Event())
        model.ignore_job('spam')

        mocks.ReplayAll()

        presenter = Presenter(model, view)  # @UnusedVariable
        job_ignored_event.fire('spam')

        mox.Verify(model)

    def test_Constructor___View_fires_job_unignored_event___Model_unignore_job_called(self):

        mocks = mox.Mox()

        model = mocks.CreateMock(IModel)
        view = mocks.CreateMock(IView)
        job_unignored_event = Event()

        model.jobs_updated_event().AndReturn(Event())
        view.job_ignored_event().InAnyOrder().AndReturn(Event())
        view.job_unignored_event().InAnyOrder().AndReturn(job_unignored_event)
        view.job_enabled_event().InAnyOrder().AndReturn(Event())
        view.job_disabled_event().InAnyOrder().AndReturn(Event())
        model.unignore_job('eggs')

        mocks.ReplayAll()

        presenter = Presenter(model, view)  # @UnusedVariable
        job_unignored_event.fire('eggs')

        mox.Verify(model)

    def test_Constructor___View_fires_job_enabled_event___Model_enable_job_called(self):

        mocks = mox.Mox()

        model = mocks.CreateMock(IModel)
        view = mocks.CreateMock(IView)
        job_enabled_event = Event()

        model.jobs_updated_event().AndReturn(Event())
        view.job_ignored_event().InAnyOrder().AndReturn(Event())
        view.job_unignored_event().InAnyOrder().AndReturn(Event())
        view.job_enabled_event().InAnyOrder().AndReturn(job_enabled_event)
        view.job_disabled_event().InAnyOrder().AndReturn(Event())
        model.enable_job('eggs')

        mocks.ReplayAll()

        presenter = Presenter(model, view)  # @UnusedVariable
        job_enabled_event.fire('eggs')

        mox.Verify(model)

    def test_Constructor___View_fires_job_disabled_event___Model_disable_job_called(self):

        mocks = mox.Mox()

        model = mocks.CreateMock(IModel)
        view = mocks.CreateMock(IView)
        job_disabled_event = Event()

        model.jobs_updated_event().AndReturn(Event())
        view.job_ignored_event().InAnyOrder().AndReturn(Event())
        view.job_unignored_event().InAnyOrder().AndReturn(Event())
        view.job_enabled_event().InAnyOrder().AndReturn(Event())
        view.job_disabled_event().InAnyOrder().AndReturn(job_disabled_event)
        model.disable_job('eggs')

        mocks.ReplayAll()

        presenter = Presenter(model, view)  # @UnusedVariable
        job_disabled_event.fire('eggs')

        mox.Verify(model)


class JobsModelTests(TestCase):

    def setUp(self):

        self.mocks = mox.Mox()
        self.jenkins = self.mocks.CreateMock(Jenkins)
        self.event = self.mocks.CreateMock(IEvent)

    def test__update_jobs__First_call__Fire_jobs_updated_event_with_no_ignores(self):

        jobOne = Job('job1', JobStatus.OK)
        jobTwo = Job('job2', JobStatus.FAILING)
        self.jenkins.list_jobs().AndReturn([jobOne, jobTwo])
        self.event.fire([JobModel(jobOne, False), JobModel(jobTwo, False)])
        self.mocks.ReplayAll()

        model = Model(self.jenkins, self.event)
        model.update_jobs()

        mox.Verify(self.event)

    def test__update_jobs__Second_call_same_jobs__Jobs_updated_event_not_fired(self):

        jobOne = Job('job1', JobStatus.OK)
        jobTwo = Job('job2', JobStatus.FAILING)
        self.jenkins.list_jobs().AndReturn([jobOne, jobTwo])
        self.jenkins.list_jobs().AndReturn([jobOne, jobTwo])
        self.event.fire([JobModel(jobOne, False), JobModel(jobTwo, False)])
        self.mocks.ReplayAll()

        model = Model(self.jenkins, self.event)
        model.update_jobs()
        model.update_jobs()

        mox.Verify(self.event)

    def test_update_jobs___Ignore_job2_before_update___JobModel_ignored_on_event_fired(self):

        jobOne = Job('job1', JobStatus.OK)
        jobTwo = Job('job2', JobStatus.FAILING)
        self.jenkins.list_jobs().AndReturn([jobOne, jobTwo])
        self.event.fire([JobModel(jobOne, False), JobModel(jobTwo, True)])
        self.mocks.ReplayAll()

        model = Model(self.jenkins, self.event)
        model.ignore_job('job2')
        model.update_jobs()

        mox.Verify(self.event)

    def test_update_jobs___Ignore_job2_after_update___event_fired_with_new_ignore_status(self):

        jobOne = Job('job1', JobStatus.OK)
        jobTwo = Job('job2', JobStatus.FAILING)
        self.jenkins.list_jobs().AndReturn([jobOne, jobTwo])
        self.jenkins.list_jobs().AndReturn([jobOne, jobTwo])
        self.event.fire([JobModel(jobOne, False), JobModel(jobTwo, False)])
        self.event.fire([JobModel(jobOne, False), JobModel(jobTwo, True)])
        self.mocks.ReplayAll()

        model = Model(self.jenkins, self.event)
        model.update_jobs()
        model.ignore_job('job2')

        mox.Verify(self.event)

    def test_update_jobs___Ignore_job2_then_unignore_before_update___JobModel_not_ignored_on_event_fired(self):

        jobOne = Job('job1', JobStatus.OK)
        jobTwo = Job('job2', JobStatus.FAILING)
        self.jenkins.list_jobs().AndReturn([jobOne, jobTwo])
        self.event.fire([JobModel(jobOne, False), JobModel(jobTwo, False)])
        self.mocks.ReplayAll()

        model = Model(self.jenkins, self.event)
        model.ignore_job('job2')
        model.unignore_job('job2')
        model.update_jobs()

        mox.Verify(self.event)

    def test_update_jobs___Ignore_job2_then_update_then_unignore___event_fired_with_new_ignore_status(self):

        jobOne = Job('job1', JobStatus.OK)
        jobTwo = Job('job2', JobStatus.FAILING)
        self.jenkins.list_jobs().AndReturn([jobOne, jobTwo])
        self.jenkins.list_jobs().AndReturn([jobOne, jobTwo])
        self.event.fire([JobModel(jobOne, False), JobModel(jobTwo, True)])
        self.event.fire([JobModel(jobOne, False), JobModel(jobTwo, False)])
        self.mocks.ReplayAll()

        model = Model(self.jenkins, self.event)
        model.ignore_job('job2')
        model.update_jobs()
        model.unignore_job('job2')

        mox.Verify(self.event)

    def test_jobs_updated___ReturnsEventFromConstructor(self):

        self.mocks.ReplayAll()

        model = Model(self.jenkins, self.event)

        self.assertTrue(self.event is model.jobs_updated_event())


class IgnoreJobsFilterTests(TestCase):

    def test___filter_jobs___Nothing_ignored___Return_unmodified_list(self):

        job_models = [JobModel(Job('eric', JobStatus.FAILING), False),
                      JobModel(Job('terry', JobStatus.FAILING), False)]

        jobs_filter = IgnoreJobsFilter()
        result = jobs_filter.filter_jobs(job_models)

        self.assertEqual(job_models, result)

    def test___filter_jobs___One_ignored___Return_non_ignored_jobs(self):

        non_ignored = JobModel(Job('eric', JobStatus.FAILING), False)
        ignored = JobModel(Job('terry', JobStatus.FAILING), True)

        jobs_filter = IgnoreJobsFilter()
        result = jobs_filter.filter_jobs([non_ignored, ignored])

        self.assertEqual([non_ignored], result)
