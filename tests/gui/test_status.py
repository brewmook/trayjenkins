import mox
from unittest import TestCase
from PySide import QtGui

from pyjenkins.job import JobStatus

import gui.media
import gui.status

class TrayIconViewAdapterTests(TestCase):

    def setUp(self):

        self.mocks = mox.Mox()

        self.view = self.mocks.CreateMock(gui.status.TrayIconView)
        self.media = self.mocks.CreateMock(gui.media.MediaFiles)
        self.media.failingIcon().InAnyOrder().AndReturn('failing.png')
        self.media.okIcon().InAnyOrder().AndReturn('ok.png')
        self.media.unknownIcon().InAnyOrder().AndReturn('unknown.png')

    def test_setStatus_FailingStatus_PassCorrectArgumentsToView(self):

        self.view.setIcon('failing.png',
                          'Failing',
                          u'Jenkins status change',
                          u'fail message',
                          QtGui.QSystemTrayIcon.Warning)

        self.mocks.ReplayAll()

        adapter = gui.status.TrayIconViewAdapter(self.view, self.media)
        adapter.setStatus(JobStatus.FAILING, 'fail message')

        mox.Verify(self.view)

    def test_setStatus_OkStatus_PassCorrectArgumentsToView(self):

        self.view.setIcon('ok.png',
                          'Ok',
                          u'Jenkins status change',
                          u'pass message',
                          QtGui.QSystemTrayIcon.Information)

        self.mocks.ReplayAll()

        adapter = gui.status.TrayIconViewAdapter(self.view, self.media)
        adapter.setStatus(JobStatus.OK, 'pass message')

        mox.Verify(self.view)

    def test_setStatus_UnknownStatus_PassCorrectArgumentsToView(self):

        self.view.setIcon('unknown.png',
                          'Unknown',
                          u'Jenkins status change',
                          u'unknown message',
                          QtGui.QSystemTrayIcon.Information)

        self.mocks.ReplayAll()

        adapter = gui.status.TrayIconViewAdapter(self.view, self.media)
        adapter.setStatus(JobStatus.UNKNOWN, 'unknown message')

        mox.Verify(self.view)

    def test_setStatus_NonsenseStatus_PassCorrectArgumentsToView(self):

        self.view.setIcon('unknown.png',
                          'Nonsense',
                          u'Jenkins status change',
                          u'any message',
                          QtGui.QSystemTrayIcon.Information)

        self.mocks.ReplayAll()

        adapter = gui.status.TrayIconViewAdapter(self.view, self.media)
        adapter.setStatus('nonsense', 'any message')

        mox.Verify(self.view)

    def test_setStatus_StatusIsNone_PassCorrectArgumentsToView(self):

        self.view.setIcon('unknown.png',
                          'None',
                          u'Jenkins status change',
                          u'any message',
                          QtGui.QSystemTrayIcon.Information)

        self.mocks.ReplayAll()

        adapter = gui.status.TrayIconViewAdapter(self.view, self.media)
        adapter.setStatus(None, 'any message')

        mox.Verify(self.view)

    def test_setStatus_MessageIsNone_PassCorrectArgumentsToView(self):

        self.view.setIcon(mox.IgnoreArg(),
                          mox.IgnoreArg(),
                          mox.IgnoreArg(),
                          u'',
                          mox.IgnoreArg())

        self.mocks.ReplayAll()

        adapter = gui.status.TrayIconViewAdapter(self.view, self.media)
        adapter.setStatus('shrubbery', None)

        mox.Verify(self.view)
