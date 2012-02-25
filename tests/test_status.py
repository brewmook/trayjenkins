import mox
from unittest import TestCase

from trayjenkins.event import Event, IEvent
from trayjenkins.jobs import IModel as JobsModel
from trayjenkins.status import IStatusReader, IView, IModel, Presenter, Model, StatusReader
from pyjenkins.interfaces import IJenkins
from pyjenkins.job import Job, JobStatus

class StatusPresenterTests(TestCase):

    def test_Constructor_ModelFiresStatusChangedEvent_ViewSetStatusCalled(self):

        mocks= mox.Mox()

        model= mocks.CreateMock(IModel)
        view= mocks.CreateMock(IView)
        event= Event()

        model.statusChangedEvent().AndReturn(event)
        view.setStatus('some status string')

        mocks.ReplayAll()

        presenter= Presenter(model, view)
        event.fire('some status string')

        mox.Verify(view)

class StatusModelTests(TestCase):

    def setUp(self):

        self.mocks = mox.Mox()
        self.statusReader = self.mocks.CreateMock(IStatusReader)
        self.statusEvent = self.mocks.CreateMock(IEvent)
        self.jobsModel = self.mocks.CreateMock(JobsModel)
        self.jobsEvent = Event()
        self.jobsModel.jobsUpdatedEvent().AndReturn(self.jobsEvent)
        self.jobs = [Job('who', 'cares?')]

    def test_updateStatus_JobsModelFiresFirstJobsUpdatedEventAndNewStatusIsFailing_StatusChangedEventFired(self):

        self.statusReader.status(self.jobs).AndReturn(JobStatus.FAILING)
        self.statusEvent.fire(JobStatus.FAILING)
        self.mocks.ReplayAll()

        model= Model(self.jobsModel, self.statusReader, self.statusEvent)

        self.jobsEvent.fire(self.jobs)

        mox.Verify(self.statusEvent)

    def test_updateStatus_JobsModelFiresFirstJobsUpdatedEventAndNewStatusIsOk_StatusChangedEventFired(self):
    
        self.statusReader.status(self.jobs).AndReturn(JobStatus.OK)
        self.statusEvent.fire(JobStatus.OK)
        self.mocks.ReplayAll()
    
        model= Model(self.jobsModel, self.statusReader, self.statusEvent)
    
        self.jobsEvent.fire(self.jobs)
    
        mox.Verify(self.statusEvent)
    
    def test_updateStatus_JobsModelFiresFirstJobsUpdatedEventAndNewStatusIsUnknown_StatusChangedEventNotFired(self):
    
        self.statusReader.status(self.jobs).AndReturn(JobStatus.UNKNOWN)
        self.mocks.ReplayAll()
    
        model= Model(self.jobsModel, self.statusReader, self.statusEvent)
    
        self.jobsEvent.fire(self.jobs)
    
        mox.Verify(self.statusEvent)
    
    def test_updateStatus_JobsModelFiresTwoJobsUpdatedEventsBothWithStatusOfFailing_StatusChangedEventFiredOnceWithFailing(self):
    
        self.statusReader.status(self.jobs).AndReturn(JobStatus.FAILING)
        self.statusReader.status(self.jobs).AndReturn(JobStatus.FAILING)
        self.statusEvent.fire(JobStatus.FAILING)
        self.mocks.ReplayAll()
    
        model= Model(self.jobsModel, self.statusReader, self.statusEvent)
    
        self.jobsEvent.fire(self.jobs)
        self.jobsEvent.fire(self.jobs)
    
        mox.Verify(self.statusEvent)
    
    def test_updateStatus_JobsModelFiresTwoJobsUpdatedEventsBothWithStatusOfOk_StatusChangedEventFiredOnceWithOk(self):
    
        self.statusReader.status(self.jobs).AndReturn(JobStatus.OK)
        self.statusReader.status(self.jobs).AndReturn(JobStatus.OK)
        self.statusEvent.fire(JobStatus.OK)
        self.mocks.ReplayAll()
    
        model= Model(self.jobsModel, self.statusReader, self.statusEvent)
    
        self.jobsEvent.fire(self.jobs)
        self.jobsEvent.fire(self.jobs)
    
        mox.Verify(self.statusEvent)
    
    def test_updateStatus_JobsModelFiresTwoJobsUpdatedEventsWithStatusOfFailingThenOk_StatusChangedEventFiredOnceWithFailingOnceWithOk(self):
    
        self.statusReader.status(self.jobs).AndReturn(JobStatus.FAILING)
        self.statusReader.status(self.jobs).AndReturn(JobStatus.OK)
        self.statusEvent.fire(JobStatus.FAILING)
        self.statusEvent.fire(JobStatus.OK)
        self.mocks.ReplayAll()
    
        model= Model(self.jobsModel, self.statusReader, self.statusEvent)
    
        self.jobsEvent.fire(self.jobs)
        self.jobsEvent.fire(self.jobs)
    
        mox.Verify(self.statusEvent)

class StatusReaderTests(TestCase):

    def test_status_OneFailingJob_ReturnFailing(self):

        jobs = [Job('eric', JobStatus.UNKNOWN),
                Job('john', JobStatus.FAILING),
                Job('terry', JobStatus.OK)]

        reader = StatusReader()
        result = reader.status(jobs)

        self.assertEqual(JobStatus.FAILING, result)

    def test_status_NoFailingJobs_ReturnOk(self):

        jobs = [Job('eric', JobStatus.UNKNOWN),
                Job('terry', JobStatus.OK)]

        reader = StatusReader()
        result = reader.status(jobs)

        self.assertEqual(JobStatus.OK, result)

    def test_status_JobsListIsNone_ReturnUnknown(self):

        reader = StatusReader()
        result = reader.status(None)

        self.assertEqual(JobStatus.UNKNOWN, result)
