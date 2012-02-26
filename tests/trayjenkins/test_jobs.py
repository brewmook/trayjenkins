import mox
from unittest import TestCase
from pyjenkins.interfaces import IJenkins, IJenkinsFactory
from pyjenkins.job import Job, JobStatus
from pyjenkins.server import Server

from trayjenkins.event import Event, IEvent
from trayjenkins.jobs import Presenter, IView, IModel, Model

class JobsPresenterTests(TestCase):

    def test_Constructor_ModelFiresJobsUpdatedEvent_ViewSetJobsCalled(self):

        mocks= mox.Mox()

        jobs = 'list of jobs'
        model= mocks.CreateMock(IModel)
        view= mocks.CreateMock(IView)
        event= Event()

        model.jobsUpdatedEvent().AndReturn(event)
        view.setJobs(jobs)

        mocks.ReplayAll()

        presenter= Presenter(model, view)
        event.fire(jobs)

        mox.Verify(view)


class JobsModelTests(TestCase):

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