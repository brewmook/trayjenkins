import mox
from unittest import TestCase
from trayjenkins.event import Event
from trayjenkins.status import IView, IModel, Presenter

class PresenterTests(TestCase):

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
