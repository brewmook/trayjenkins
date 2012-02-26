import mox
from unittest import TestCase

from trayjenkins.event import Event, IEvent
from trayjenkins.jobs import IModel as JobsModel
from trayjenkins.status import *
from pyjenkins.interfaces import IJenkins
from pyjenkins.job import Job, JobStatus

class StatusPresenterTests(TestCase):

    def test_Constructor_ModelFiresStatusChangedEvent_ViewSetStatusCalled(self):

        mocks= mox.Mox()

        model= mocks.CreateMock(IModel)
        view= mocks.CreateMock(IView)
        event= Event()

        model.statusChangedEvent().AndReturn(event)
        view.setStatus('some status string', 'status message')

        mocks.ReplayAll()

        presenter= Presenter(model, view)
        event.fire('some status string', 'status message')

        mox.Verify(view)

class StatusModelTests(TestCase):

    def setUp(self):

        self.mocks = mox.Mox()
        self.filter = self.mocks.CreateMock(IJobsFilter)
        self.messageComposer = self.mocks.CreateMock(IMessageComposer)
        self.statusReader = self.mocks.CreateMock(IStatusReader)
        self.statusEvent = self.mocks.CreateMock(IEvent)
        self.jobsModel = self.mocks.CreateMock(JobsModel)
        self.jobsEvent = Event()
        self.jobsModel.jobsUpdatedEvent().AndReturn(self.jobsEvent)
        self.jobs = [Job('who', 'cares?')]

    def test_updateStatus_JobsModelFiresFirstUpdateEventStatusUnknownAndMessageNone_StatusChangedEventNotFired(self):

        self.filter.filter(self.jobs).AndReturn(self.jobs)
        self.messageComposer.message(self.jobs).AndReturn(None)
        self.statusReader.status(self.jobs).AndReturn(JobStatus.UNKNOWN)
        self.mocks.ReplayAll()

        model= Model(self.jobsModel, self.filter, self.messageComposer, self.statusReader, self.statusEvent)

        self.jobsEvent.fire(self.jobs)

        mox.Verify(self.statusEvent)

    def test_updateStatus_JobsModelFiresFirstUpdateEvent_StatusChangedEventFired(self):

        self.filter.filter(self.jobs).AndReturn(self.jobs)
        self.messageComposer.message(self.jobs).AndReturn('message')
        self.statusReader.status(self.jobs).AndReturn(JobStatus.FAILING)
        self.statusEvent.fire(JobStatus.FAILING, 'message')
        self.mocks.ReplayAll()

        model= Model(self.jobsModel, self.filter, self.messageComposer, self.statusReader, self.statusEvent)

        self.jobsEvent.fire(self.jobs)

        mox.Verify(self.statusEvent)

    def test_updateStatus_TwoJobsModelUpdatesWithSameStatusAndMessage_StatusChangedEventFiredOnce(self):

        self.filter.filter(self.jobs).AndReturn(self.jobs)
        self.filter.filter(self.jobs).AndReturn(self.jobs)
        self.messageComposer.message(self.jobs).AndReturn('message')
        self.messageComposer.message(self.jobs).AndReturn('message')
        self.statusReader.status(self.jobs).AndReturn(JobStatus.FAILING)
        self.statusReader.status(self.jobs).AndReturn(JobStatus.FAILING)
        self.statusEvent.fire(JobStatus.FAILING, 'message')
        self.mocks.ReplayAll()

        model= Model(self.jobsModel, self.filter, self.messageComposer, self.statusReader, self.statusEvent)

        self.jobsEvent.fire(self.jobs)
        self.jobsEvent.fire(self.jobs)

        mox.Verify(self.statusEvent)

    def test_updateStatus_TwoJobsModelUpdatesWithDifferentStatus_StatusChangedEventFiredTwice(self):

        self.filter.filter(self.jobs).AndReturn(self.jobs)
        self.filter.filter(self.jobs).AndReturn(self.jobs)
        self.messageComposer.message(self.jobs).AndReturn('message')
        self.messageComposer.message(self.jobs).AndReturn('message')
        self.statusReader.status(self.jobs).AndReturn(JobStatus.FAILING)
        self.statusReader.status(self.jobs).AndReturn(JobStatus.OK)
        self.statusEvent.fire(JobStatus.FAILING, 'message')
        self.statusEvent.fire(JobStatus.OK, 'message')
        self.mocks.ReplayAll()

        model= Model(self.jobsModel, self.filter, self.messageComposer, self.statusReader, self.statusEvent)

        self.jobsEvent.fire(self.jobs)
        self.jobsEvent.fire(self.jobs)

        mox.Verify(self.statusEvent)

    def test_updateStatus_TwoJobsModelUpdatesWithDifferentMessage_StatusChangedEventFiredTwice(self):

        self.filter.filter(self.jobs).AndReturn(self.jobs)
        self.filter.filter(self.jobs).AndReturn(self.jobs)
        self.messageComposer.message(self.jobs).AndReturn('message one')
        self.messageComposer.message(self.jobs).AndReturn('message two')
        self.statusReader.status(self.jobs).AndReturn(JobStatus.FAILING)
        self.statusReader.status(self.jobs).AndReturn(JobStatus.FAILING)
        self.statusEvent.fire(JobStatus.FAILING, 'message one')
        self.statusEvent.fire(JobStatus.FAILING, 'message two')
        self.mocks.ReplayAll()

        model= Model(self.jobsModel, self.filter, self.messageComposer, self.statusReader, self.statusEvent)

        self.jobsEvent.fire(self.jobs)
        self.jobsEvent.fire(self.jobs)

        mox.Verify(self.statusEvent)

    def test_updateStatus_JobsFilterReturnsModifiedList_ModifiedListPassedTo(self):

        filtered = [Job('completely', 'different')]
        self.filter.filter(self.jobs).AndReturn(filtered)
        self.messageComposer.message(filtered).AndReturn('message')
        self.statusReader.status(filtered).AndReturn(JobStatus.OK)
        self.statusEvent.fire(JobStatus.OK, 'message')
        self.mocks.ReplayAll()

        model= Model(self.jobsModel, self.filter, self.messageComposer, self.statusReader, self.statusEvent)

        self.jobsEvent.fire(self.jobs)

        mox.Verify(self.statusEvent)


class StatusReaderTests(TestCase):

    def test_status_OneFailingJob_ReturnFailing(self):

        jobs = [Job('eric', JobStatus.UNKNOWN),
                Job('john', JobStatus.FAILING),
                Job('terry', JobStatus.OK),
                Job('graham', JobStatus.DISABLED)]

        reader = StatusReader()
        result = reader.status(jobs)

        self.assertEqual(JobStatus.FAILING, result)

    def test_status_NoFailingJobs_ReturnOk(self):

        jobs = [Job('eric', JobStatus.UNKNOWN),
                Job('terry', JobStatus.OK),
                Job('graham', JobStatus.DISABLED)]

        reader = StatusReader()
        result = reader.status(jobs)

        self.assertEqual(JobStatus.OK, result)

    def test_status_JobsListIsNone_ReturnUnknown(self):

        reader = StatusReader()
        result = reader.status(None)

        self.assertEqual(JobStatus.UNKNOWN, result)


class DefaultMessageComposerTests(TestCase):

    def test_message_EmptyJobs_ReturnCorrectMessage(self):

        jobs = []

        composer = DefaultMessageComposer()
        result = composer.message(jobs)

        self.assertEqual('No jobs', result)

    def test_message_AllJobsOk_ReturnCorrectMessage(self):

        jobs = [Job('eric', JobStatus.OK),
                Job('terry', JobStatus.OK)]

        composer = DefaultMessageComposer()
        result = composer.message(jobs)

        self.assertEqual('All active jobs pass', result)

    def test_message_OneFailingJob_ReturnCorrectMessage(self):

        jobs = [Job('eric', JobStatus.OK),
                Job('terry', JobStatus.FAILING)]

        composer = DefaultMessageComposer()
        result = composer.message(jobs)

        self.assertEqual('FAILING:\nterry', result)

    def test_message_TwoFailingJobs_ReturnCorrectMessage(self):

        jobs = [Job('eric', JobStatus.FAILING),
                Job('terry', JobStatus.FAILING)]

        composer = DefaultMessageComposer()
        result = composer.message(jobs)

        self.assertEqual('FAILING:\neric\nterry', result)

    def test_message_JobsListIsNone_ReturnUnknown(self):

        composer = DefaultMessageComposer()
        result = composer.message(None)

        self.assertEqual('', result)


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