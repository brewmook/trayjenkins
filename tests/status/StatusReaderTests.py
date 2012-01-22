import mox
from unittest import TestCase
from trayjenkins.status.StatusReader import StatusReader
from pyjenkins.interfaces import IJenkins
from pyjenkins.Job import Job, JobStatus

class StatusReaderTests(TestCase):

    def test_status_OneFailingJob_ReturnFailing(self):

        mocks= mox.Mox()

        jenkins= mocks.CreateMock(IJenkins)
        jenkins.listJobs().AndReturn([Job('eric', JobStatus.UNKNOWN),
                                      Job('john', JobStatus.FAILING),
                                      Job('terry', JobStatus.OK)])
        mocks.ReplayAll()

        reader = StatusReader(jenkins)
        result = reader.status()

        self.assertEqual(JobStatus.FAILING, result)

    def test_status_NoFailingJobs_ReturnOk(self):

        mocks= mox.Mox()

        jenkins= mocks.CreateMock(IJenkins)
        jenkins.listJobs().AndReturn([Job('eric', JobStatus.UNKNOWN),
                                      Job('terry', JobStatus.OK)])
        mocks.ReplayAll()

        reader = StatusReader(jenkins)
        result = reader.status()

        self.assertEqual(JobStatus.OK, result)

    def test_status_ListJobsReturnsNone_ReturnUnknown(self):

        mocks= mox.Mox()

        jenkins= mocks.CreateMock(IJenkins)
        jenkins.listJobs().AndReturn(None)
        mocks.ReplayAll()

        reader = StatusReader(jenkins)
        result = reader.status()

        self.assertEqual(JobStatus.UNKNOWN, result)