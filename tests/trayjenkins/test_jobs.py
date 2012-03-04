import mox
from unittest import TestCase
from pyjenkins.interfaces import IJenkinsFactory
from pyjenkins.jenkins import Jenkins
from pyjenkins.job import Job, JobStatus

from trayjenkins.event import Event, IEvent
from trayjenkins.jobs import *


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

        presenter = Presenter(model, view)
        event.fire(jobs)

        mox.Verify(view)


class JobsModelTests(TestCase):

    def setUp(self):

        self.mocks = mox.Mox()
        self.filter = self.mocks.CreateMock(IFilter)
        self.jenkins = self.mocks.CreateMock(Jenkins)
        self.factory = self.mocks.CreateMock(IJenkinsFactory)
        self.event = self.mocks.CreateMock(IEvent)
        self.server = Server('host', 'uname', 'pw')

    def test__update_jobs__FirstCall_FireJobsUpdatedEventWithRetrievedJobs(self):

        jobs = [Job('job1', JobStatus.OK), Job('job2', JobStatus.FAILING)]
        self.filter.filter(mox.IgnoreArg()).AndReturn(jobs)
        self.factory.create(self.server).AndReturn(self.jenkins)
        self.jenkins.list_jobs().AndReturn(jobs)
        self.event.fire(jobs)
        self.mocks.ReplayAll()

        model = Model(self.server, self.filter, self.factory, self.event)
        model.update_jobs()

        mox.Verify(self.event)

    def test__update_jobs__SecondCallReturnsSameJobs_JobsUpdatedEventNotFiredOnceOnly(self):

        jobs = [Job('job1', JobStatus.OK), Job('job2', JobStatus.FAILING)]
        self.filter.filter(mox.IgnoreArg()).AndReturn(jobs)
        self.filter.filter(mox.IgnoreArg()).AndReturn(jobs)
        self.factory.create(self.server).AndReturn(self.jenkins)
        self.jenkins.list_jobs().AndReturn(jobs)
        self.jenkins.list_jobs().AndReturn(jobs)
        self.event.fire(jobs)
        self.mocks.ReplayAll()

        model = Model(self.server, self.filter, self.factory, self.event)
        model.update_jobs()
        model.update_jobs()

        mox.Verify(self.event)

    def test__update_jobs__SecondCallReturnsDifferentJobs_JobsUpdatedEventFiredForEachResult(self):

        jobsOne = [Job('job1', JobStatus.OK), Job('job2', JobStatus.FAILING)]
        jobsTwo = [Job('job1', JobStatus.OK), Job('job2', JobStatus.OK)]
        self.filter.filter(jobsOne).AndReturn(jobsOne)
        self.filter.filter(jobsTwo).AndReturn(jobsTwo)
        self.factory.create(self.server).AndReturn(self.jenkins)
        self.jenkins.list_jobs().AndReturn(jobsOne)
        self.jenkins.list_jobs().AndReturn(jobsTwo)
        self.event.fire(jobsOne)
        self.event.fire(jobsTwo)
        self.mocks.ReplayAll()

        model = Model(self.server, self.filter, self.factory, self.event)
        model.update_jobs()
        model.update_jobs()

        mox.Verify(self.event)

    def test__update_jobs__SameJobsButFilterAltersList_JobsUpdatedEventFiredForEachUpdate(self):

        real_jobs = [Job('job1', JobStatus.OK), Job('job2', JobStatus.FAILING)]
        filtered_jobs = [Job('job1', JobStatus.OK)]
        self.filter.filter(real_jobs).AndReturn(real_jobs)
        self.filter.filter(real_jobs).AndReturn(filtered_jobs)
        self.factory.create(self.server).AndReturn(self.jenkins)
        self.jenkins.list_jobs().AndReturn(real_jobs)
        self.jenkins.list_jobs().AndReturn(real_jobs)
        self.event.fire(real_jobs)
        self.event.fire(real_jobs)
        self.mocks.ReplayAll()

        model = Model(self.server, self.filter, self.factory, self.event)
        model.update_jobs()
        model.update_jobs()

        mox.Verify(self.event)

    def test__jobs_updated__event_ReturnsEventFromConstructor(self):

        self.factory.create(mox.IgnoreArg()).AndReturn(None)
        self.mocks.ReplayAll()

        model = Model(self.server, self.filter, self.factory, self.event)

        self.assertTrue(self.event is model.jobs_updated_event())


class NoFilterTests(TestCase):

    def test_filter_ReturnUnmodifiedList(self):

        jobs = ['list', 'of', 'jobs']
        filter = NoFilter()
        result = filter.filter(jobs)

        self.assertTrue(jobs is result)


class IgnoreJobsFilterTests(TestCase):

    def test_filter_NothingIgnored_ReturnUnmodifiedList(self):

        jobs = [Job('eric', JobStatus.FAILING),
                Job('terry', JobStatus.FAILING)]

        filter = IgnoreJobsFilter()
        result = filter.filter(jobs)

        self.assertEqual(jobs, result)

    def test_filter_EricIgnored_ReturnFilteredList(self):

        jobs = [Job('eric', JobStatus.FAILING),
                Job('terry', JobStatus.FAILING)]

        filter = IgnoreJobsFilter()
        filter.ignore('terry')

        expected = [Job('eric', JobStatus.FAILING)]
        result = filter.filter(jobs)

        self.assertEqual(expected, result)

    def test_filter_EricAndTerryIgnored_ReturnEmptyList(self):

        jobs = [Job('eric', JobStatus.FAILING),
                Job('terry', JobStatus.FAILING)]

        filter = IgnoreJobsFilter()
        filter.ignore('eric')
        filter.ignore('terry')

        expected = []
        result = filter.filter(jobs)

        self.assertEqual(expected, result)

    def test_filter_EricIgnoredThenUnignored_ReturnFilteredList(self):

        jobs = [Job('eric', JobStatus.FAILING),
                Job('terry', JobStatus.FAILING)]

        filter = IgnoreJobsFilter()
        filter.ignore('terry')
        filter.unignore('terry')

        result = filter.filter(jobs)

        self.assertEqual(jobs, result)

    def test_ignoring_JobNotIgnored_ReturnFalse(self):

        filter = IgnoreJobsFilter()

        result = filter.ignoring('norwegian blue')

        self.assertEqual(False, result)

    def test_ignoring_JobIsIgnored_ReturnTrue(self):

        filter = IgnoreJobsFilter()
        filter.ignore('norwegian blue')

        result = filter.ignoring('norwegian blue')

        self.assertEqual(True, result)
