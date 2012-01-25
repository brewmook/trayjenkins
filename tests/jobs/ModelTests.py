import mox
from unittest import TestCase
from pyjenkins.interfaces import IEvent, IJenkins, IJenkinsFactory
from pyjenkins.job import Job, JobStatus
from pyjenkins.event import Event
from pyjenkins.server import Server

from trayjenkins.jobs.model import Model

class ModelTests(TestCase):

    def test_updateJobs_FirstCall_FireJobsUpdatedEventWithRetrievedJobs(self):

        mocks = mox.Mox()
        jenkins = mocks.CreateMock(IJenkins)
        factory = mocks.CreateMock(IJenkinsFactory)
        event = mocks.CreateMock(IEvent)

        server = Server('host', 'uname', 'pw')
        jobs = [Job('job1', JobStatus.OK), Job('job2', JobStatus.FAILING)]
        factory.create(server).AndReturn(jenkins)
        jenkins.listJobs().AndReturn(jobs)
        event.fire(jobs)

        mocks.ReplayAll()

        model = Model(server, factory, event)
        model.updateJobs()

        mox.Verify(event)

    def test_updateJobs_SecondCallReturnsSameJobs_JobsUpdatedEventNotFiredOnceOnly(self):

        mocks = mox.Mox()
        jenkins = mocks.CreateMock(IJenkins)
        factory = mocks.CreateMock(IJenkinsFactory)
        event = mocks.CreateMock(IEvent)

        server = Server('host', 'uname', 'pw')
        jobs = [Job('job1', JobStatus.OK), Job('job2', JobStatus.FAILING)]
        factory.create(server).AndReturn(jenkins)
        jenkins.listJobs().AndReturn(jobs)
        jenkins.listJobs().AndReturn(jobs)
        event.fire(jobs)

        mocks.ReplayAll()

        model = Model(server, factory, event)
        model.updateJobs()
        model.updateJobs()

        mox.Verify(event)

    def test_updateJobs_SecondCallReturnsDifferentJobs_JobsUpdatedEventFiredForEachResult(self):

        mocks = mox.Mox()
        jenkins = mocks.CreateMock(IJenkins)
        factory = mocks.CreateMock(IJenkinsFactory)
        event = mocks.CreateMock(IEvent)

        server = Server('host', 'uname', 'pw')
        jobsOne = [Job('job1', JobStatus.OK), Job('job2', JobStatus.FAILING)]
        jobsTwo = [Job('job1', JobStatus.OK), Job('job2', JobStatus.OK)]
        factory.create(server).AndReturn(jenkins)
        jenkins.listJobs().AndReturn(jobsOne)
        jenkins.listJobs().AndReturn(jobsTwo)
        event.fire(jobsOne)
        event.fire(jobsTwo)

        mocks.ReplayAll()

        model = Model(server, factory, event)
        model.updateJobs()
        model.updateJobs()

        mox.Verify(event)

    def test_jobsUpdatedEvent_ReturnsEventFromConstructor(self):

        mocks = mox.Mox()
        factory = mocks.CreateMock(IJenkinsFactory)
        event = mocks.CreateMock(IEvent)

        server = Server('dunt', 'really', 'matter')
        factory.create(mox.IgnoreArg()).AndReturn(None)

        mocks.ReplayAll()

        model = Model(server, factory, event)

        self.assertTrue(event is model.jobsUpdatedEvent())
