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
        self.media.failing_icon().InAnyOrder().AndReturn('failing.png')
        self.media.ok_icon().InAnyOrder().AndReturn('ok.png')
        self.media.unknown_icon().InAnyOrder().AndReturn('unknown.png')

    def test__set_status__FailingStatus_PassCorrectArgumentsToView(self):

        self.view.setIcon('failing.png',
                          'Failing',
                          u'Jenkins status change',
                          u'fail message',
                          QtGui.QSystemTrayIcon.Warning)

        self.mocks.ReplayAll()

        adapter = gui.status.TrayIconViewAdapter(self.view, self.media)
        adapter.set_status(JobStatus.FAILING, 'fail message')

        mox.Verify(self.view)

    def test__set_status__OkStatus_PassCorrectArgumentsToView(self):

        self.view.setIcon('ok.png',
                          'Ok',
                          u'Jenkins status change',
                          u'pass message',
                          QtGui.QSystemTrayIcon.Information)

        self.mocks.ReplayAll()

        adapter = gui.status.TrayIconViewAdapter(self.view, self.media)
        adapter.set_status(JobStatus.OK, 'pass message')

        mox.Verify(self.view)

    def test__set_status__UnknownStatus_PassCorrectArgumentsToView(self):

        self.view.setIcon('unknown.png',
                          'Unknown',
                          u'Jenkins status change',
                          u'unknown message',
                          QtGui.QSystemTrayIcon.Information)

        self.mocks.ReplayAll()

        adapter = gui.status.TrayIconViewAdapter(self.view, self.media)
        adapter.set_status(JobStatus.UNKNOWN, 'unknown message')

        mox.Verify(self.view)

    def test__set_status__NonsenseStatus_PassCorrectArgumentsToView(self):

        self.view.setIcon('unknown.png',
                          'Nonsense',
                          u'Jenkins status change',
                          u'any message',
                          QtGui.QSystemTrayIcon.Information)

        self.mocks.ReplayAll()

        adapter = gui.status.TrayIconViewAdapter(self.view, self.media)
        adapter.set_status('nonsense', 'any message')

        mox.Verify(self.view)

    def test__set_status__StatusIsNone_PassCorrectArgumentsToView(self):

        self.view.setIcon('unknown.png',
                          'None',
                          u'Jenkins status change',
                          u'any message',
                          QtGui.QSystemTrayIcon.Information)

        self.mocks.ReplayAll()

        adapter = gui.status.TrayIconViewAdapter(self.view, self.media)
        adapter.set_status(None, 'any message')

        mox.Verify(self.view)

    def test__set_status__MessageIsNone_PassCorrectArgumentsToView(self):

        self.view.setIcon(mox.IgnoreArg(),
                          mox.IgnoreArg(),
                          mox.IgnoreArg(),
                          u'',
                          mox.IgnoreArg())

        self.mocks.ReplayAll()

        adapter = gui.status.TrayIconViewAdapter(self.view, self.media)
        adapter.set_status('shrubbery', None)

        mox.Verify(self.view)
