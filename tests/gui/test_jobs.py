import mox
from unittest import TestCase
from PySide import QtGui

import gui.jobs
import trayjenkins.jobs

class MockQMenu(object):
    def addAction(self, parameter):
        pass

class ContextSensitiveMenuFactoryTests(TestCase):

    def setUp(self):

        self.parent = 'fake parent'
        self.actions = {
            'Ignore':'ignore action',
            'Cancel ignore':'cancel ignore action',
            }

        self.mocks = mox.Mox()
        self.menu = self.mocks.CreateMock(MockQMenu)
        self.menuFactory = self.mocks.CreateMock(gui.jobs._QMenuFactory)
        self.ignoreJobsFilter = self.mocks.CreateMock(trayjenkins.jobs.IgnoreJobsFilter)

        self.menuFactory.create(self.parent).AndReturn(self.menu)

    def test_create_AnyJob_ReturnMenu(self):

        self.ignoreJobsFilter.ignoring(mox.IgnoreArg()).AndReturn(False)
        self.menu.addAction(mox.IgnoreArg())
        self.mocks.ReplayAll()

        factory = gui.jobs.ContextSensitiveMenuFactory(self.actions,
                                                       self.ignoreJobsFilter,
                                                       self.menuFactory)

        result = factory.create(self.parent, 'job')

        self.assertTrue(self.menu is result)

    def test_create_JobIsNotIgnored_AddIgnoreAction(self):

        self.ignoreJobsFilter.ignoring('job').AndReturn(False)
        self.menu.addAction('ignore action')
        self.mocks.ReplayAll()

        factory = gui.jobs.ContextSensitiveMenuFactory(self.actions,
                                                       self.ignoreJobsFilter,
                                                       self.menuFactory)

        result = factory.create(self.parent, 'job')

        mox.Verify(self.menu)

    def test_create_JobIsIgnored_AddCancelIgnoreAction(self):

        self.ignoreJobsFilter.ignoring('job').AndReturn(True)
        self.menu.addAction('cancel ignore action')
        self.mocks.ReplayAll()

        factory = gui.jobs.ContextSensitiveMenuFactory(self.actions,
                                                       self.ignoreJobsFilter,
                                                       self.menuFactory)

        result = factory.create(self.parent, 'job')

        mox.Verify(self.menu)
