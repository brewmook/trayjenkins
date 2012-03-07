import mox
from unittest import TestCase

from pyjenkins.interfaces import IJenkinsFactory
from pyjenkins.jenkins import Jenkins
from pyjenkins.job import Job, JobStatus
from pyjenkins.server import Server
from trayjenkins.event import Event, IEvent
from trayjenkins.jobs import IModel, IView, IFilter, Presenter, Model, NoFilter, IgnoreJobsFilter,\
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
        event = Event()

        model.jobs_updated_event().AndReturn(event)
        view.set_jobs(jobs)

        mocks.ReplayAll()

        presenter = Presenter(model, view)  # @UnusedVariable
        event.fire(jobs)

        mox.Verify(view)


class JobsModelTests(TestCase):

    def setUp(self):

        self.mocks = mox.Mox()
        self.jobs_filter = self.mocks.CreateMock(IFilter)
        self.jenkins = self.mocks.CreateMock(Jenkins)
        self.factory = self.mocks.CreateMock(IJenkinsFactory)
        self.event = self.mocks.CreateMock(IEvent)
        self.server = Server('host', 'uname', 'pw')

    def test__update_jobs__FirstCall_FireJobsUpdatedEventWithRetrievedJobs(self):

        jobs = [Job('job1', JobStatus.OK), Job('job2', JobStatus.FAILING)]
        self.jobs_filter.filter_jobs(mox.IgnoreArg()).AndReturn(jobs)
        self.factory.create(self.server).AndReturn(self.jenkins)
        self.jenkins.list_jobs().AndReturn(jobs)
        self.event.fire(jobs)
        self.mocks.ReplayAll()

        model = Model(self.server, self.jobs_filter, self.factory, self.event)
        model.update_jobs()

        mox.Verify(self.event)

    def test__update_jobs__SecondCallReturnsSameJobs_JobsUpdatedEventNotFiredOnceOnly(self):

        jobs = [Job('job1', JobStatus.OK), Job('job2', JobStatus.FAILING)]
        self.jobs_filter.filter_jobs(mox.IgnoreArg()).AndReturn(jobs)
        self.jobs_filter.filter_jobs(mox.IgnoreArg()).AndReturn(jobs)
        self.factory.create(self.server).AndReturn(self.jenkins)
        self.jenkins.list_jobs().AndReturn(jobs)
        self.jenkins.list_jobs().AndReturn(jobs)
        self.event.fire(jobs)
        self.mocks.ReplayAll()

        model = Model(self.server, self.jobs_filter, self.factory, self.event)
        model.update_jobs()
        model.update_jobs()

        mox.Verify(self.event)

    def test__update_jobs__SecondCallReturnsDifferentJobs_JobsUpdatedEventFiredForEachResult(self):

        jobsOne = [Job('job1', JobStatus.OK), Job('job2', JobStatus.FAILING)]
        jobsTwo = [Job('job1', JobStatus.OK), Job('job2', JobStatus.OK)]
        self.jobs_filter.filter_jobs(jobsOne).AndReturn(jobsOne)
        self.jobs_filter.filter_jobs(jobsTwo).AndReturn(jobsTwo)
        self.factory.create(self.server).AndReturn(self.jenkins)
        self.jenkins.list_jobs().AndReturn(jobsOne)
        self.jenkins.list_jobs().AndReturn(jobsTwo)
        self.event.fire(jobsOne)
        self.event.fire(jobsTwo)
        self.mocks.ReplayAll()

        model = Model(self.server, self.jobs_filter, self.factory, self.event)
        model.update_jobs()
        model.update_jobs()

        mox.Verify(self.event)

    def test__update_jobs__SameJobsButFilterAltersList_JobsUpdatedEventFiredForEachUpdate(self):

        real_jobs = [Job('job1', JobStatus.OK), Job('job2', JobStatus.FAILING)]
        filtered_jobs = [Job('job1', JobStatus.OK)]
        self.jobs_filter.filter_jobs(real_jobs).AndReturn(real_jobs)
        self.jobs_filter.filter_jobs(real_jobs).AndReturn(filtered_jobs)
        self.factory.create(self.server).AndReturn(self.jenkins)
        self.jenkins.list_jobs().AndReturn(real_jobs)
        self.jenkins.list_jobs().AndReturn(real_jobs)
        self.event.fire(real_jobs)
        self.event.fire(real_jobs)
        self.mocks.ReplayAll()

        model = Model(self.server, self.jobs_filter, self.factory, self.event)
        model.update_jobs()
        model.update_jobs()

        mox.Verify(self.event)

    def test__jobs_updated__event_ReturnsEventFromConstructor(self):

        self.factory.create(mox.IgnoreArg()).AndReturn(None)
        self.mocks.ReplayAll()

        model = Model(self.server, self.jobs_filter, self.factory, self.event)

        self.assertTrue(self.event is model.jobs_updated_event())


class NoFilterTests(TestCase):

    def test_filter_ReturnUnmodifiedList(self):

        jobs = ['list', 'of', 'jobs']
        no_filter = NoFilter()
        result = no_filter.filter_jobs(jobs)

        self.assertTrue(jobs is result)


class IgnoreJobsFilterTests(TestCase):

    def test_filter_NothingIgnored_ReturnUnmodifiedList(self):

        jobs = [Job('eric', JobStatus.FAILING),
                Job('terry', JobStatus.FAILING)]

        jobs_filter = IgnoreJobsFilter()
        result = jobs_filter.filter_jobs(jobs)

        self.assertEqual(jobs, result)

    def test_filter_EricIgnored_ReturnFilteredList(self):

        jobs = [Job('eric', JobStatus.FAILING),
                Job('terry', JobStatus.FAILING)]

        jobs_filter = IgnoreJobsFilter()
        jobs_filter.ignore('terry')

        expected = [Job('eric', JobStatus.FAILING)]
        result = jobs_filter.filter_jobs(jobs)

        self.assertEqual(expected, result)

    def test_filter_EricAndTerryIgnored_ReturnEmptyList(self):

        jobs = [Job('eric', JobStatus.FAILING),
                Job('terry', JobStatus.FAILING)]

        jobs_filter = IgnoreJobsFilter()
        jobs_filter.ignore('eric')
        jobs_filter.ignore('terry')

        expected = []
        result = jobs_filter.filter_jobs(jobs)

        self.assertEqual(expected, result)

    def test_filter_EricIgnoredThenUnignored_ReturnFilteredList(self):

        jobs = [Job('eric', JobStatus.FAILING),
                Job('terry', JobStatus.FAILING)]

        jobs_filter = IgnoreJobsFilter()
        jobs_filter.ignore('terry')
        jobs_filter.unignore('terry')

        result = jobs_filter.filter_jobs(jobs)

        self.assertEqual(jobs, result)

    def test_ignoring_JobNotIgnored_ReturnFalse(self):

        jobs_filter = IgnoreJobsFilter()

        result = jobs_filter.ignoring('norwegian blue')

        self.assertEqual(False, result)

    def test_ignoring_JobIsIgnored_ReturnTrue(self):

        jobs_filter = IgnoreJobsFilter()
        jobs_filter.ignore('norwegian blue')

        result = jobs_filter.ignoring('norwegian blue')

        self.assertEqual(True, result)
