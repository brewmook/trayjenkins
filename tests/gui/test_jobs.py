import mox
from unittest import TestCase

import gui.jobs
import gui.qmock
import trayjenkins.jobs
import pyjenkins.job
from trayjenkins.event import Event
from trayjenkins.jobs import JobModel
from pyjenkins.job import Job


class MockQMenu(object):

    def addAction(self, parameter):
        pass

    def popup(self, coordinates):
        pass


class ContextMenuFactoryTests(TestCase):

    def setUp(self):

        self.parent = 'fake parent'
        self.mocks = mox.Mox()
        self.menu = self.mocks.CreateMock(MockQMenu)
        self.qtgui = self.mocks.CreateMock(gui.qmock.QtGuiFactory)

        self.qtgui.QMenu(self.parent).AndReturn(self.menu)

    def test_create_AnyJob_ReturnMenu(self):

        job_model = JobModel(Job('name', 'status'), False)
        self.qtgui.QAction(mox.IgnoreArg(), mox.IgnoreArg(), triggered=mox.IgnoreArg()).AndReturn('ignore action')
        self.menu.addAction(mox.IgnoreArg())
        self.mocks.ReplayAll()

        factory = gui.jobs.ContextMenuFactory(self.parent, self.qtgui)
        result = factory.create(job_model, 'ignore callback', 'unignore callback')

        self.assertTrue(self.menu is result)

    def test_create_JobIsNotIgnored_AddIgnoreAction(self):

        job_model = JobModel(Job('name', 'status'), False)
        self.qtgui.QAction('Ignore', self.parent, triggered='ignore callback').AndReturn('ignore action')
        self.menu.addAction('ignore action')
        self.mocks.ReplayAll()

        factory = gui.jobs.ContextMenuFactory(self.parent, self.qtgui)
        factory.create(job_model, 'ignore callback', 'unignore callback')

        mox.Verify(self.menu)

    def test_create_JobIsIgnored_AddCancelIgnoreAction(self):

        job_model = JobModel(Job('name', 'status'), True)
        self.qtgui.QAction('Cancel ignore', self.parent, triggered='unignore callback').AndReturn('unignore action')
        self.menu.addAction('unignore action')
        self.mocks.ReplayAll()

        factory = gui.jobs.ContextMenuFactory(self.parent, self.qtgui)
        factory.create(job_model, 'ignore callback', 'unignore callback')

        mox.Verify(self.menu)


class MockEventHandler(object):
    def __call__(self, argument):
        self.argument = argument


class ListViewAdapterTests(TestCase):

    def setUp(self):

        self.mocks = mox.Mox()
        self.view = self.mocks.CreateMock(gui.jobs.ListView)
        self.media = self.mocks.CreateMock(gui.media.MediaFiles)
        self.qtgui = self.mocks.CreateMock(gui.qmock.QtGuiFactory)
        self.menu_factory = self.mocks.CreateMock(gui.jobs.ContextMenuFactory)

        self.media.disabled_icon().InAnyOrder().AndReturn('disabled icon')
        self.media.failing_icon().InAnyOrder().AndReturn('failing icon')
        self.media.ignored_icon().InAnyOrder().AndReturn('ignored icon')
        self.media.ok_icon().InAnyOrder().AndReturn('ok icon')
        self.media.unknown_icon().InAnyOrder().AndReturn('unknown icon')

    def test___set_jobs___Empty_list___Empty_list_passed_to_view_set_list(self):

        self.view.job_ignored_event().InAnyOrder().AndReturn(Event())
        self.view.job_unignored_event().InAnyOrder().AndReturn(Event())
        self.view.right_click_event().InAnyOrder().AndReturn(Event())
        self.view.set_list([])
        self.mocks.ReplayAll()

        adapter = gui.jobs.ListViewAdapter(self.view, self.media, self.menu_factory, self.qtgui)
        adapter.set_jobs([])

        mox.Verify(self.view)

    def test___set_jobs___Four_jobs___List_with_correct_names_and_statuses_passed_to_view(self):

        jobs = [trayjenkins.jobs.JobModel(pyjenkins.job.Job('eric', pyjenkins.job.JobStatus.DISABLED),
                                          False),
                trayjenkins.jobs.JobModel(pyjenkins.job.Job('john', pyjenkins.job.JobStatus.FAILING),
                                          False),
                trayjenkins.jobs.JobModel(pyjenkins.job.Job('terry', pyjenkins.job.JobStatus.OK),
                                          False),
                trayjenkins.jobs.JobModel(pyjenkins.job.Job('graham', pyjenkins.job.JobStatus.UNKNOWN),
                                          False)
                ]

        self.qtgui.QListWidgetItem('disabled icon', 'eric').AndReturn('item for eric')
        self.qtgui.QListWidgetItem('failing icon', 'john').AndReturn('item for john')
        self.qtgui.QListWidgetItem('ok icon', 'terry').AndReturn('item for terry')
        self.qtgui.QListWidgetItem('unknown icon', 'graham').AndReturn('item for graham')
        self.view.job_ignored_event().InAnyOrder().AndReturn(Event())
        self.view.job_unignored_event().InAnyOrder().AndReturn(Event())
        self.view.right_click_event().InAnyOrder().AndReturn(Event())
        self.view.set_list(['item for eric', 'item for john', 'item for terry', 'item for graham'])
        self.mocks.ReplayAll()

        adapter = gui.jobs.ListViewAdapter(self.view, self.media, self.menu_factory, self.qtgui)
        adapter.set_jobs(jobs)

        mox.Verify(self.view)

    def test___set_jobs___Ignored_job___Ignored_job_gets_ignored_icon(self):

        jobs = [trayjenkins.jobs.JobModel(pyjenkins.job.Job('john', pyjenkins.job.JobStatus.FAILING),
                                          False),
                trayjenkins.jobs.JobModel(pyjenkins.job.Job('terry', pyjenkins.job.JobStatus.OK),
                                          True),
                ]

        self.qtgui.QListWidgetItem('failing icon', 'john').AndReturn('item for john')
        self.qtgui.QListWidgetItem('ignored icon', 'terry').AndReturn('item for terry')
        self.view.job_ignored_event().InAnyOrder().AndReturn(Event())
        self.view.job_unignored_event().InAnyOrder().AndReturn(Event())
        self.view.right_click_event().InAnyOrder().AndReturn(Event())
        self.view.set_list(['item for john', 'item for terry'])
        self.mocks.ReplayAll()

        adapter = gui.jobs.ListViewAdapter(self.view, self.media, self.menu_factory, self.qtgui)
        adapter.set_jobs(jobs)

        mox.Verify(self.view)

    def test___job_ignored_event___View_fires_job_ignored___fire_job_ignored_event(self):

        view_event = Event()
        self.view.job_ignored_event().InAnyOrder().AndReturn(view_event)
        self.view.job_unignored_event().InAnyOrder().AndReturn(Event())
        self.view.right_click_event().InAnyOrder().AndReturn(Event())
        self.mocks.ReplayAll()

        mock_event_handler = MockEventHandler()

        adapter = gui.jobs.ListViewAdapter(self.view, self.media, self.menu_factory, self.qtgui)  # @UnusedVariable
        adapter.job_ignored_event().register(mock_event_handler)
        view_event.fire('some job name')

        self.assertEqual('some job name', mock_event_handler.argument)

    def test___job_unignored_event___View_fires_job_unignored___fire_job_unignored_event(self):

        view_event = Event()
        self.view.job_ignored_event().InAnyOrder().AndReturn(Event())
        self.view.job_unignored_event().InAnyOrder().AndReturn(view_event)
        self.view.right_click_event().InAnyOrder().AndReturn(Event())
        self.mocks.ReplayAll()

        mock_event_handler = MockEventHandler()

        adapter = gui.jobs.ListViewAdapter(self.view, self.media, self.menu_factory, self.qtgui)  # @UnusedVariable
        adapter.job_unignored_event().register(mock_event_handler)
        view_event.fire('some job name')

        self.assertEqual('some job name', mock_event_handler.argument)

    def test_constructor___View_fires_right_click_event___Show_menu_at_correct_coordinates(self):

        right_click_event = Event()
        menu = self.mocks.CreateMock(MockQMenu)
        menu.popup('screen coordinates')

        self.menu_factory.create(mox.IgnoreArg(), mox.IgnoreArg(), mox.IgnoreArg()).AndReturn(menu)
        self.qtgui.QMenu(self.view).AndReturn(menu)
        self.view.job_ignored_event().InAnyOrder().AndReturn(Event())
        self.view.job_unignored_event().InAnyOrder().AndReturn(Event())
        self.view.right_click_event().InAnyOrder().AndReturn(right_click_event)
        self.view.set_list(mox.IgnoreArg()).InAnyOrder()
        self.mocks.ReplayAll()

        adapter = gui.jobs.ListViewAdapter(self.view, self.media, self.menu_factory, self.qtgui)  # @UnusedVariable

        right_click_event.fire('job name', 'screen coordinates')

        mox.Verify(menu)
