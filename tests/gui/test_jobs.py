import mox
from unittest import TestCase

import gui.jobs
import gui.qmock
import trayjenkins.jobs
import pyjenkins.job
from trayjenkins.event import Event
from trayjenkins.jobs import JobModel
from pyjenkins.job import Job, JobStatus


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
        self.qtgui.QAction(mox.IgnoreArg(), mox.IgnoreArg(), triggered=mox.IgnoreArg()).InAnyOrder().AndReturn('ignore/unignore action')
        self.qtgui.QAction(mox.IgnoreArg(), mox.IgnoreArg(), triggered=mox.IgnoreArg()).InAnyOrder().AndReturn('enable/disable action')
        self.menu.addAction(mox.IgnoreArg()).InAnyOrder()
        self.menu.addAction(mox.IgnoreArg()).InAnyOrder()
        self.mocks.ReplayAll()

        factory = gui.jobs.ContextMenuFactory(self.parent, self.qtgui)
        result = factory.create(job_model, 'ignore callback', 'unignore callback', 'enable callback', 'disable callback')

        self.assertTrue(self.menu is result)

    def test_create_JobIsNotIgnored_AddIgnoreAction(self):

        job_model = JobModel(Job('name', 'status'), False)
        self.qtgui.QAction('Ignore', self.parent, triggered='ignore callback').InAnyOrder().AndReturn('ignore action')
        self.qtgui.QAction(mox.IgnoreArg(), mox.IgnoreArg(), triggered=mox.IgnoreArg()).InAnyOrder().AndReturn('enable/disable action')
        self.menu.addAction('ignore action').InAnyOrder()
        self.menu.addAction(mox.IgnoreArg()).InAnyOrder()
        self.mocks.ReplayAll()

        factory = gui.jobs.ContextMenuFactory(self.parent, self.qtgui)
        factory.create(job_model, 'ignore callback', 'unignore callback', 'enable callback', 'disable callback')

        mox.Verify(self.menu)

    def test_create_JobIsIgnored_AddCancelIgnoreAction(self):

        job_model = JobModel(Job('name', 'status'), True)
        self.qtgui.QAction('Cancel ignore', self.parent, triggered='unignore callback').InAnyOrder().AndReturn('unignore action')
        self.qtgui.QAction(mox.IgnoreArg(), mox.IgnoreArg(), triggered=mox.IgnoreArg()).InAnyOrder().AndReturn('enable/disable action')
        self.menu.addAction('unignore action').InAnyOrder()
        self.menu.addAction(mox.IgnoreArg()).InAnyOrder()
        self.mocks.ReplayAll()

        factory = gui.jobs.ContextMenuFactory(self.parent, self.qtgui)
        factory.create(job_model, 'ignore callback', 'unignore callback', 'enable callback', 'disable callback')

        mox.Verify(self.menu)

    def test_create_JobIsDisabled_AddEnableAction(self):

        job_model = JobModel(Job('name', JobStatus.DISABLED), True)
        self.qtgui.QAction(mox.IgnoreArg(), mox.IgnoreArg(), triggered=mox.IgnoreArg()).InAnyOrder().AndReturn('ignore/unignore action')
        self.qtgui.QAction('Enable', self.parent, triggered='enable callback').InAnyOrder().AndReturn('enable action')
        self.menu.addAction(mox.IgnoreArg()).InAnyOrder()
        self.menu.addAction('enable action').InAnyOrder()
        self.mocks.ReplayAll()

        factory = gui.jobs.ContextMenuFactory(self.parent, self.qtgui)
        factory.create(job_model, 'ignore callback', 'unignore callback', 'enable callback', 'disable callback')

        mox.Verify(self.menu)

    def test_create___Job_status_is_OK___Add_disable_action(self):

        job_model = JobModel(Job('name', JobStatus.OK), True)
        self.qtgui.QAction(mox.IgnoreArg(), mox.IgnoreArg(), triggered=mox.IgnoreArg()).InAnyOrder().AndReturn('ignore/unignore action')
        self.qtgui.QAction('Disable', self.parent, triggered='disable callback').InAnyOrder().AndReturn('disable action')
        self.menu.addAction(mox.IgnoreArg()).InAnyOrder()
        self.menu.addAction('disable action').InAnyOrder()
        self.mocks.ReplayAll()

        factory = gui.jobs.ContextMenuFactory(self.parent, self.qtgui)
        factory.create(job_model, 'ignore callback', 'unignore callback', 'enable callback', 'disable callback')

        mox.Verify(self.menu)

    def test_create___Job_status_is_failing___Add_disable_action(self):

        job_model = JobModel(Job('name', JobStatus.FAILING), True)
        self.qtgui.QAction(mox.IgnoreArg(), mox.IgnoreArg(), triggered=mox.IgnoreArg()).InAnyOrder().AndReturn('ignore/unignore action')
        self.qtgui.QAction('Disable', self.parent, triggered='disable callback').InAnyOrder().AndReturn('disable action')
        self.menu.addAction(mox.IgnoreArg()).InAnyOrder()
        self.menu.addAction('disable action').InAnyOrder()
        self.mocks.ReplayAll()

        factory = gui.jobs.ContextMenuFactory(self.parent, self.qtgui)
        factory.create(job_model, 'ignore callback', 'unignore callback', 'enable callback', 'disable callback')

        mox.Verify(self.menu)

    def test_create___Job_status_is_unknown___No_enable_or_disable_added(self):

        job_model = JobModel(Job('name', JobStatus.UNKNOWN), False)
        self.qtgui.QAction(mox.IgnoreArg(), mox.IgnoreArg(), triggered='ignore callback').InAnyOrder().AndReturn('ignore/unignore action')
        self.qtgui.QAction(mox.IgnoreArg(), mox.IgnoreArg(), triggered='unignore callback').InAnyOrder().AndReturn('ignore/unignore action')
        self.menu.addAction('ignore/unignore action')
        self.mocks.ReplayAll()

        factory = gui.jobs.ContextMenuFactory(self.parent, self.qtgui)
        factory.create(job_model, 'ignore callback', 'unignore callback', 'enable callback', 'disable callback')

        mox.Verify(self.menu)


class MockEventHandler(object):

    def __init__(self):
        self.argument = None

    def __call__(self, argument):
        self.argument = argument


class MockMenuFactory(object):

    def __init__(self, menu):
        self._menu = menu
        self.ignore_callback = None
        self.unignore_callback = None
        self.enable_callback = None
        self.disable_callback = None

    def create(self, model, ignore_callback, unignore_callback, enable_callback, disable_callback):
        self.ignore_callback = ignore_callback
        self.unignore_callback = unignore_callback
        self.enable_callback = enable_callback
        self.disable_callback = disable_callback
        return self._menu


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

        self.view.right_click_event().InAnyOrder().AndReturn(Event())
        self.view.set_list([])
        self.mocks.ReplayAll()

        adapter = gui.jobs.ListViewAdapter(self.view, self.media, self.menu_factory, self.qtgui)
        adapter.set_jobs([])

        mox.Verify(self.view)

    def test___set_jobs___Four_jobs___List_with_correct_names_and_statuses_passed_to_view(self):

        jobs = [JobModel(Job('eric', pyjenkins.job.JobStatus.DISABLED), False),
                JobModel(Job('john', pyjenkins.job.JobStatus.FAILING), False),
                JobModel(Job('terry', pyjenkins.job.JobStatus.OK), False),
                JobModel(Job('graham', pyjenkins.job.JobStatus.UNKNOWN), False)]

        self.qtgui.QListWidgetItem('disabled icon', 'eric').AndReturn('item for eric')
        self.qtgui.QListWidgetItem('failing icon', 'john').AndReturn('item for john')
        self.qtgui.QListWidgetItem('ok icon', 'terry').AndReturn('item for terry')
        self.qtgui.QListWidgetItem('unknown icon', 'graham').AndReturn('item for graham')
        self.view.right_click_event().InAnyOrder().AndReturn(Event())
        self.view.set_list(['item for eric', 'item for john', 'item for terry', 'item for graham'])
        self.mocks.ReplayAll()

        adapter = gui.jobs.ListViewAdapter(self.view, self.media, self.menu_factory, self.qtgui)
        adapter.set_jobs(jobs)

        mox.Verify(self.view)

    def test___set_jobs___Ignored_job___Ignored_job_gets_ignored_icon(self):

        jobs = [JobModel(Job('john', pyjenkins.job.JobStatus.FAILING), False),
                JobModel(Job('terry', pyjenkins.job.JobStatus.OK), True)]

        self.qtgui.QListWidgetItem('failing icon', 'john').AndReturn('item for john')
        self.qtgui.QListWidgetItem('ignored icon', 'terry').AndReturn('item for terry')
        self.view.right_click_event().InAnyOrder().AndReturn(Event())
        self.view.set_list(['item for john', 'item for terry'])
        self.mocks.ReplayAll()

        adapter = gui.jobs.ListViewAdapter(self.view, self.media, self.menu_factory, self.qtgui)
        adapter.set_jobs(jobs)

        mox.Verify(self.view)

    def test_constructor___View_fires_right_click_event___Show_menu_at_correct_coordinates(self):

        right_click_event = Event()
        menu = self.mocks.CreateMock(MockQMenu)
        menu.popup('screen coordinates')

        job_models = [JobModel(Job('eric', pyjenkins.job.JobStatus.DISABLED), False),
                      JobModel(Job('john', pyjenkins.job.JobStatus.FAILING), False),
                      JobModel(Job('terry', pyjenkins.job.JobStatus.OK), False)]

        self._stub_out_set_jobs()
        self.menu_factory.create(job_models[1], mox.IgnoreArg(), mox.IgnoreArg(), mox.IgnoreArg(), mox.IgnoreArg()).AndReturn(menu)
        self.view.right_click_event().InAnyOrder().AndReturn(right_click_event)
        self.mocks.ReplayAll()

        adapter = gui.jobs.ListViewAdapter(self.view, self.media, self.menu_factory, self.qtgui)  # @UnusedVariable
        adapter.set_jobs(job_models)
        right_click_event.fire('john', 'screen coordinates')

        mox.Verify(menu)

    def test_constructor___User_clicks_ignore_menu_item___Fire_job_ignored_event(self):

        job_models = [JobModel(Job('eric', pyjenkins.job.JobStatus.DISABLED), False)]
        right_click_event = Event()
        menu = self.mocks.CreateMock(MockQMenu)
        menu_factory = MockMenuFactory(menu)
        mock_event_handler = MockEventHandler()

        self.view.right_click_event().InAnyOrder().AndReturn(right_click_event)
        self._stub_out_set_jobs()
        menu.popup(mox.IgnoreArg())
        self.mocks.ReplayAll()

        adapter = gui.jobs.ListViewAdapter(self.view, self.media, menu_factory, self.qtgui)  # @UnusedVariable
        adapter.job_ignored_event().register(mock_event_handler)
        adapter.set_jobs(job_models)
        right_click_event.fire('eric', 'screen coordinates')
        menu_factory.ignore_callback()

        self.assertEqual('eric', mock_event_handler.argument)

    def test_constructor___User_clicks_unignore_menu_item___Fire_job_unignored_event(self):

        job_models = [JobModel(Job('eric', pyjenkins.job.JobStatus.DISABLED), False)]
        right_click_event = Event()
        menu = self.mocks.CreateMock(MockQMenu)
        menu_factory = MockMenuFactory(menu)
        mock_event_handler = MockEventHandler()

        self.view.right_click_event().InAnyOrder().AndReturn(right_click_event)
        self._stub_out_set_jobs()
        menu.popup(mox.IgnoreArg())
        self.mocks.ReplayAll()

        adapter = gui.jobs.ListViewAdapter(self.view, self.media, menu_factory, self.qtgui)  # @UnusedVariable
        adapter.job_unignored_event().register(mock_event_handler)
        adapter.set_jobs(job_models)
        right_click_event.fire('eric', 'screen coordinates')
        menu_factory.unignore_callback()

        self.assertEqual('eric', mock_event_handler.argument)

    def test_constructor___User_clicks_enable_menu_item___Fire_job_enabled_event(self):

        job_models = [JobModel(Job('eric', pyjenkins.job.JobStatus.DISABLED), False)]
        right_click_event = Event()
        menu = self.mocks.CreateMock(MockQMenu)
        menu_factory = MockMenuFactory(menu)
        mock_event_handler = MockEventHandler()

        self.view.right_click_event().InAnyOrder().AndReturn(right_click_event)
        self._stub_out_set_jobs()
        menu.popup(mox.IgnoreArg())
        self.mocks.ReplayAll()

        adapter = gui.jobs.ListViewAdapter(self.view, self.media, menu_factory, self.qtgui)  # @UnusedVariable
        adapter.job_enabled_event().register(mock_event_handler)
        adapter.set_jobs(job_models)
        right_click_event.fire('eric', 'screen coordinates')
        menu_factory.enable_callback()

        self.assertEqual('eric', mock_event_handler.argument)

    def test_constructor___User_clicks_disable_menu_item___Fire_job_disabled_event(self):

        job_models = [JobModel(Job('eric', pyjenkins.job.JobStatus.FAILING), False)]
        right_click_event = Event()
        menu = self.mocks.CreateMock(MockQMenu)
        menu_factory = MockMenuFactory(menu)
        mock_event_handler = MockEventHandler()

        self.view.right_click_event().InAnyOrder().AndReturn(right_click_event)
        self._stub_out_set_jobs()
        menu.popup(mox.IgnoreArg())
        self.mocks.ReplayAll()

        adapter = gui.jobs.ListViewAdapter(self.view, self.media, menu_factory, self.qtgui)  # @UnusedVariable
        adapter.job_disabled_event().register(mock_event_handler)
        adapter.set_jobs(job_models)
        right_click_event.fire('eric', 'screen coordinates')
        menu_factory.disable_callback()

        self.assertEqual('eric', mock_event_handler.argument)

    def _stub_out_set_jobs(self):

        self.qtgui.QListWidgetItem(mox.IgnoreArg(), mox.IgnoreArg()).AndReturn('whatever')
        self.qtgui.QListWidgetItem(mox.IgnoreArg(), mox.IgnoreArg()).AndReturn('whatever')
        self.qtgui.QListWidgetItem(mox.IgnoreArg(), mox.IgnoreArg()).AndReturn('whatever')
        self.view.set_list(mox.IgnoreArg()).InAnyOrder()
