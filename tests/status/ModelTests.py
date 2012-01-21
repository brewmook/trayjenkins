import mox
from unittest import TestCase
import trayjenkins
from trayjenkins.status.Model import Model
from pyjenkins.interfaces import IJenkins
from pyjenkins.Job import Job, JobStatus

class ModelTests(TestCase):

    def test_status_OneFailingJob_ReturnFailing(self):

        mocks= mox.Mox()

        jenkins= mocks.CreateMock(IJenkins)

        jenkins.listJobs().AndReturn([Job('eric', JobStatus.UNKNOWN),
                                      Job('john', JobStatus.FAILING),
                                      Job('terry', JobStatus.OK)])
        mocks.ReplayAll()

        model= Model(jenkins)

        self.assertEqual(JobStatus.FAILING, model.status())

    def test_status_NoFailingJobs_ReturnOk(self):

        mocks= mox.Mox()

        jenkins= mocks.CreateMock(IJenkins)

        jenkins.listJobs().AndReturn([Job('eric', JobStatus.UNKNOWN),
                                      Job('terry', JobStatus.OK)])
        mocks.ReplayAll()

        model= Model(jenkins)

        self.assertEqual(JobStatus.OK, model.status())

    def test_status_ListJobsReturnsNone_ReturnUnknown(self):

        mocks= mox.Mox()

        jenkins= mocks.CreateMock(IJenkins)

        jenkins.listJobs().AndReturn(None)
        mocks.ReplayAll()

        model= Model(jenkins)

        self.assertEqual(JobStatus.UNKNOWN, model.status())