from unittest import TestCase

from trayjenkins.status.statusreader import StatusReader
from trayjenkins.jobs import IModel
from pyjenkins.job import Job, JobStatus

class StatusReaderTests(TestCase):

    def test_status_OneFailingJob_ReturnFailing(self):

        jobs = [Job('eric', JobStatus.UNKNOWN),
                Job('john', JobStatus.FAILING),
                Job('terry', JobStatus.OK)]

        reader = StatusReader()
        result = reader.status(jobs)

        self.assertEqual(JobStatus.FAILING, result)

    def test_status_NoFailingJobs_ReturnOk(self):

        jobs = [Job('eric', JobStatus.UNKNOWN),
                Job('terry', JobStatus.OK)]

        reader = StatusReader()
        result = reader.status(jobs)

        self.assertEqual(JobStatus.OK, result)

    def test_status_JobsListIsNone_ReturnUnknown(self):

        reader = StatusReader()
        result = reader.status(None)

        self.assertEqual(JobStatus.UNKNOWN, result)
