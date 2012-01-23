import mox
from unittest import TestCase
from trayjenkins.status.Model import Model
from trayjenkins.status.interfaces import IStatusReader
from pyjenkins.interfaces import IJenkins, IEvent
from pyjenkins.job import JobStatus

class ModelTests(TestCase):

    def setUp(self):

        self.mocks = mox.Mox()
        self.statusReader = self.mocks.CreateMock(IStatusReader)
        self.event = self.mocks.CreateMock(IEvent)

    def test_updateStatus_FirstReaderStatusCallReturnsFailing_StatusChangedEventFired(self):

        self.statusReader.status().AndReturn(JobStatus.FAILING)
        self.event.fire(JobStatus.FAILING)
        self.mocks.ReplayAll()

        model= Model(self.statusReader)
        model._statusChangedEvent = self.event

        model.updateStatus()

        mox.Verify(self.event)

    def test_updateStatus_FirstReaderStatusCallReturnsOk_StatusChangedEventFired(self):

        self.statusReader.status().AndReturn(JobStatus.OK)
        self.event.fire(JobStatus.OK)
        self.mocks.ReplayAll()

        model= Model(self.statusReader)
        model._statusChangedEvent = self.event

        model.updateStatus()

        mox.Verify(self.event)

    def test_updateStatus_FirstReaderStatusCallReturnsUnknown_StatusChangedEventNotFired(self):

        self.statusReader.status().AndReturn(JobStatus.UNKNOWN)
        self.mocks.ReplayAll()

        model= Model(self.statusReader)
        # inject fake event
        model._statusChangedEvent = self.event

        model.updateStatus()

        mox.Verify(self.event)

    def test_updateStatus_TwoStatusCallsReturnFailing_StatusChangedEventFiredOnceWithFailing(self):

        self.statusReader.status().AndReturn(JobStatus.FAILING)
        self.statusReader.status().AndReturn(JobStatus.FAILING)
        self.event.fire(JobStatus.FAILING)
        self.mocks.ReplayAll()

        model= Model(self.statusReader)
        # inject fake event
        model._statusChangedEvent = self.event

        model.updateStatus()
        model.updateStatus()

        mox.Verify(self.event)

    def test_updateStatus_StatusCallsReturnFailingThenOk_StatusChangedEventFiredOnceWithFailingOnceWithOk(self):

        self.statusReader.status().AndReturn(JobStatus.FAILING)
        self.statusReader.status().AndReturn(JobStatus.OK)
        self.event.fire(JobStatus.FAILING)
        self.event.fire(JobStatus.OK)
        self.mocks.ReplayAll()

        model= Model(self.statusReader)
        # inject fake event
        model._statusChangedEvent = self.event

        model.updateStatus()
        model.updateStatus()

        mox.Verify(self.event)
