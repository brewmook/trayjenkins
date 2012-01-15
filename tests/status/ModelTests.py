import mox
from unittest import TestCase
import trayjenkins
from trayjenkins.status.Model import Model
from pyjenkins.interfaces import IJenkins

class ModelTests(TestCase):

    def test_status_SomeFailingJobsNoExemptions_ReturnFailing(self):

        mocks= mox.Mox()

        jenkins= mocks.CreateMock(IJenkins)

        jenkins.listFailingJobs().AndReturn(['spam', 'eggs'])
        mocks.ReplayAll()

        model= Model(jenkins)

        self.assertEqual(trayjenkins.status.FAILING, model.status())

    def test_status_NoFailingJobsNoExemptions_ReturnOk(self):

        mocks= mox.Mox()

        jenkins= mocks.CreateMock(IJenkins)

        jenkins.listFailingJobs().AndReturn([])
        mocks.ReplayAll()

        model= Model(jenkins)

        self.assertEqual(trayjenkins.status.OK, model.status())

    def test_status_ListFailingJobsReturnsNone_ReturnUnknown(self):

        mocks= mox.Mox()

        jenkins= mocks.CreateMock(IJenkins)

        jenkins.listFailingJobs().AndReturn(None)
        mocks.ReplayAll()

        model= Model(jenkins)

        self.assertEqual(trayjenkins.status.UNKNOWN, model.status())
