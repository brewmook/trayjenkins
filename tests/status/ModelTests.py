import mox
from unittest import TestCase
from trayjenkins.jobs.interfaces import IModel as JobsModel
from trayjenkins.status.model import Model
from trayjenkins.status.interfaces import IStatusReader
from pyjenkins.event import Event
from pyjenkins.interfaces import IJenkins, IEvent
from pyjenkins.job import Job, JobStatus

class ModelTests(TestCase):

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

        model= Model(self.jobsModel, self.statusReader)
        model._statusChangedEvent = self.statusEvent

        self.jobsEvent.fire(self.jobs)

        mox.Verify(self.statusEvent)

    def test_updateStatus_JobsModelFiresFirstJobsUpdatedEventAndNewStatusIsOk_StatusChangedEventFired(self):
    
        self.statusReader.status(self.jobs).AndReturn(JobStatus.OK)
        self.statusEvent.fire(JobStatus.OK)
        self.mocks.ReplayAll()
    
        model= Model(self.jobsModel, self.statusReader)
        model._statusChangedEvent = self.statusEvent
    
        self.jobsEvent.fire(self.jobs)
    
        mox.Verify(self.statusEvent)
    
    def test_updateStatus_JobsModelFiresFirstJobsUpdatedEventAndNewStatusIsUnknown_StatusChangedEventNotFired(self):
    
        self.statusReader.status(self.jobs).AndReturn(JobStatus.UNKNOWN)
        self.mocks.ReplayAll()
    
        model= Model(self.jobsModel, self.statusReader)
        # inject fake event
        model._statusChangedEvent = self.statusEvent
    
        self.jobsEvent.fire(self.jobs)
    
        mox.Verify(self.statusEvent)
    
    def test_updateStatus_JobsModelFiresTwoJobsUpdatedEventsBothWithStatusOfFailing_StatusChangedEventFiredOnceWithFailing(self):
    
        self.statusReader.status(self.jobs).AndReturn(JobStatus.FAILING)
        self.statusReader.status(self.jobs).AndReturn(JobStatus.FAILING)
        self.statusEvent.fire(JobStatus.FAILING)
        self.mocks.ReplayAll()
    
        model= Model(self.jobsModel, self.statusReader)
        # inject fake event
        model._statusChangedEvent = self.statusEvent
    
        self.jobsEvent.fire(self.jobs)
        self.jobsEvent.fire(self.jobs)
    
        mox.Verify(self.statusEvent)
    
    def test_updateStatus_JobsModelFiresTwoJobsUpdatedEventsBothWithStatusOfOk_StatusChangedEventFiredOnceWithOk(self):
    
        self.statusReader.status(self.jobs).AndReturn(JobStatus.OK)
        self.statusReader.status(self.jobs).AndReturn(JobStatus.OK)
        self.statusEvent.fire(JobStatus.OK)
        self.mocks.ReplayAll()
    
        model= Model(self.jobsModel, self.statusReader)
        # inject fake event
        model._statusChangedEvent = self.statusEvent
    
        self.jobsEvent.fire(self.jobs)
        self.jobsEvent.fire(self.jobs)
    
        mox.Verify(self.statusEvent)
    
    def test_updateStatus_JobsModelFiresTwoJobsUpdatedEventsWithStatusOfFailingThenOk_StatusChangedEventFiredOnceWithFailingOnceWithOk(self):
    
        self.statusReader.status(self.jobs).AndReturn(JobStatus.FAILING)
        self.statusReader.status(self.jobs).AndReturn(JobStatus.OK)
        self.statusEvent.fire(JobStatus.FAILING)
        self.statusEvent.fire(JobStatus.OK)
        self.mocks.ReplayAll()
    
        model= Model(self.jobsModel, self.statusReader)
        # inject fake event
        model._statusChangedEvent = self.statusEvent
    
        self.jobsEvent.fire(self.jobs)
        self.jobsEvent.fire(self.jobs)
    
        mox.Verify(self.statusEvent)
