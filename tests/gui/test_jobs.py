import mox
from unittest import TestCase
from PySide import QtGui

import gui.jobs
import gui.qmock
import trayjenkins.jobs

class MockQMenu(object):
    def addAction(self, parameter):
        pass

class ContextSensitiveMenuFactoryTests(TestCase):

    def setUp(self):

        self.parent = 'fake parent'
        self.mocks = mox.Mox()
        self.actions = self.mocks.CreateMock(gui.jobs.ContextMenuActions)
        self.menu = self.mocks.CreateMock(MockQMenu)
        self.qtgui = self.mocks.CreateMock(gui.qmock.QtGuiFactory)
        self.ignoreJobsFilter = self.mocks.CreateMock(trayjenkins.jobs.IgnoreJobsFilter)

        self.actions.ignore().InAnyOrder().AndReturn('ignore action')
        self.actions.cancel_ignore().InAnyOrder().AndReturn('cancel ignore action')
        self.qtgui.QMenu(self.parent).AndReturn(self.menu)

    def test_create_AnyJob_ReturnMenu(self):

        self.ignoreJobsFilter.ignoring(mox.IgnoreArg()).AndReturn(False)
        self.menu.addAction(mox.IgnoreArg())
        self.mocks.ReplayAll()

        factory = gui.jobs.ContextSensitiveMenuFactory(self.actions,
                                                       self.ignoreJobsFilter,
                                                       self.qtgui)

        result = factory.create(self.parent, 'job')

        self.assertTrue(self.menu is result)

    def test_create_JobIsNotIgnored_AddIgnoreAction(self):

        self.ignoreJobsFilter.ignoring('job').AndReturn(False)
        self.menu.addAction('ignore action')
        self.mocks.ReplayAll()

        factory = gui.jobs.ContextSensitiveMenuFactory(self.actions,
                                                       self.ignoreJobsFilter,
                                                       self.qtgui)

        result = factory.create(self.parent, 'job')

        mox.Verify(self.menu)

    def test_create_JobIsIgnored_AddCancelIgnoreAction(self):

        self.ignoreJobsFilter.ignoring('job').AndReturn(True)
        self.menu.addAction('cancel ignore action')
        self.mocks.ReplayAll()

        factory = gui.jobs.ContextSensitiveMenuFactory(self.actions,
                                                       self.ignoreJobsFilter,
                                                       self.qtgui)

        result = factory.create(self.parent, 'job')

        mox.Verify(self.menu)

