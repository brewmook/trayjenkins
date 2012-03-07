import mox
from unittest import TestCase

import gui.jobs
import gui.qmock
import trayjenkins.jobs
import pyjenkins.job


class MockQMenu(object):
    def addAction(self, parameter):
        pass


class ContextMenuFactoryTests(TestCase):

    def setUp(self):

        self.parent = 'fake parent'
        self.actions = gui.jobs.ContextMenuActions('ignore action', 'cancel ignore action')
        self.mocks = mox.Mox()
        self.menu = self.mocks.CreateMock(MockQMenu)
        self.qtgui = self.mocks.CreateMock(gui.qmock.QtGuiFactory)
        self.ignoreJobsFilter = self.mocks.CreateMock(trayjenkins.jobs.IgnoreJobsFilter)

        self.qtgui.QMenu(self.parent).AndReturn(self.menu)

    def test_create_AnyJob_ReturnMenu(self):

        self.ignoreJobsFilter.ignoring(mox.IgnoreArg()).AndReturn(False)
        self.menu.addAction(mox.IgnoreArg())
        self.mocks.ReplayAll()

        factory = gui.jobs.ContextMenuFactory(self.parent,
                                              self.actions,
                                              self.ignoreJobsFilter,
                                              self.qtgui)

        result = factory.create('job')

        self.assertTrue(self.menu is result)

    def test_create_JobIsNotIgnored_AddIgnoreAction(self):

        self.ignoreJobsFilter.ignoring('job').AndReturn(False)
        self.menu.addAction('ignore action')
        self.mocks.ReplayAll()

        factory = gui.jobs.ContextMenuFactory(self.parent,
                                              self.actions,
                                              self.ignoreJobsFilter,
                                              self.qtgui)

        factory.create('job')

        mox.Verify(self.menu)

    def test_create_JobIsIgnored_AddCancelIgnoreAction(self):

        self.ignoreJobsFilter.ignoring('job').AndReturn(True)
        self.menu.addAction('cancel ignore action')
        self.mocks.ReplayAll()

        factory = gui.jobs.ContextMenuFactory(self.parent,
                                              self.actions,
                                              self.ignoreJobsFilter,
                                              self.qtgui)

        factory.create('job')

        mox.Verify(self.menu)


class ListViewAdapterTests(TestCase):

    def setUp(self):

        self.mocks = mox.Mox()
        self.view = self.mocks.CreateMock(gui.jobs.ListView)
        self.media = self.mocks.CreateMock(gui.media.MediaFiles)
        self.ignore_jobs_filter = self.mocks.CreateMock(trayjenkins.jobs.IgnoreJobsFilter)
        self.qtgui = self.mocks.CreateMock(gui.qmock.QtGuiFactory)

        self.media.disabled_icon().InAnyOrder().AndReturn('disabled icon')
        self.media.failing_icon().InAnyOrder().AndReturn('failing icon')
        self.media.ignored_icon().InAnyOrder().AndReturn('ignored icon')
        self.media.ok_icon().InAnyOrder().AndReturn('ok icon')
        self.media.unknown_icon().InAnyOrder().AndReturn('unknown icon')

    def test___set_jobs___Empty_list___Empty_list_passed_to_view_set_list(self):

        self.view.set_list([])
        self.mocks.ReplayAll()

        adapter = gui.jobs.ListViewAdapter(self.view, self.media, self.ignore_jobs_filter, self.qtgui)
        adapter.set_jobs([])

        mox.Verify(self.view)

    def test___set_jobs___Four_jobs___List_with_correct_names_and_statuses_passed_to_view(self):

        jobs = [pyjenkins.job.Job('eric', pyjenkins.job.JobStatus.DISABLED),
                pyjenkins.job.Job('john', pyjenkins.job.JobStatus.FAILING),
                pyjenkins.job.Job('terry', pyjenkins.job.JobStatus.OK),
                pyjenkins.job.Job('graham', pyjenkins.job.JobStatus.UNKNOWN)]

        self.ignore_jobs_filter.ignoring(mox.IgnoreArg()).AndReturn(False)
        self.ignore_jobs_filter.ignoring(mox.IgnoreArg()).AndReturn(False)
        self.ignore_jobs_filter.ignoring(mox.IgnoreArg()).AndReturn(False)
        self.ignore_jobs_filter.ignoring(mox.IgnoreArg()).AndReturn(False)
        self.qtgui.QListWidgetItem('disabled icon', 'eric').AndReturn('item for eric')
        self.qtgui.QListWidgetItem('failing icon', 'john').AndReturn('item for john')
        self.qtgui.QListWidgetItem('ok icon', 'terry').AndReturn('item for terry')
        self.qtgui.QListWidgetItem('unknown icon', 'graham').AndReturn('item for graham')
        self.view.set_list(['item for eric', 'item for john', 'item for terry', 'item for graham'])
        self.mocks.ReplayAll()

        adapter = gui.jobs.ListViewAdapter(self.view, self.media, self.ignore_jobs_filter, self.qtgui)
        adapter.set_jobs(jobs)

        mox.Verify(self.view)

    def test___set_jobs___Ignored_job___Ignored_job_gets_ignored_icon(self):

        jobs = [pyjenkins.job.Job('john', pyjenkins.job.JobStatus.FAILING),
                pyjenkins.job.Job('terry', pyjenkins.job.JobStatus.OK)]

        self.ignore_jobs_filter.ignoring('john').AndReturn(False)
        self.ignore_jobs_filter.ignoring('terry').AndReturn(True)
        self.qtgui.QListWidgetItem('failing icon', 'john').AndReturn('item for john')
        self.qtgui.QListWidgetItem('ignored icon', 'terry').AndReturn('item for terry')
        self.view.set_list(['item for john', 'item for terry'])
        self.mocks.ReplayAll()

        adapter = gui.jobs.ListViewAdapter(self.view, self.media, self.ignore_jobs_filter, self.qtgui)
        adapter.set_jobs(jobs)

        mox.Verify(self.view)
