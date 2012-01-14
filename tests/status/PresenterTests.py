import mox
from unittest import TestCase
from pyjenkins.Event import Event
from trayjenkins.status.Presenter import Presenter
from trayjenkins.status.interfaces import IView, IModel

class PresenterTests(TestCase):

    def test_Constructor_ModelSendsStatusChangedEvent_ViewUpdateStatusCalled(self):

        mocks= mox.Mox()

        model= mocks.CreateMock(IModel)
        view= mocks.CreateMock(IView)
        event= Event()

        model.statusChangedEvent().AndReturn(event)
        view.updateStatus('pies')

        mocks.ReplayAll()

        presenter= Presenter(model, view)
        event.fire('pies')

        mox.Verify(view)
