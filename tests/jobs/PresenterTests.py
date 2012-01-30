import mox
from unittest import TestCase
from trayjenkins.event import Event
from trayjenkins.jobs.presenter import Presenter
from trayjenkins.jobs.interfaces import IView, IModel

class PresenterTests(TestCase):

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
