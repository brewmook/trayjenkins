import mox
from unittest import TestCase
from pyjenkins.Event import Event
from trayjenkins.status.Presenter import Presenter
from trayjenkins.status.interfaces import IView, IModel

class PresenterTests(TestCase):

    def test_Constructor_ViewFiresStatusRefreshEvent_ViewSetStatusCalled(self):

        mocks= mox.Mox()

        model= mocks.CreateMock(IModel)
        view= mocks.CreateMock(IView)
        event= Event()

        model.status().AndReturn('some status string')
        view.statusRefreshEvent().AndReturn(event)
        view.setStatus('some status string')

        mocks.ReplayAll()

        presenter= Presenter(model, view)
        event.fire()

        mox.Verify(view)
