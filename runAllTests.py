#!/usr/bin/python

import unittest
import sys

sys.path.append('submodules/pyjenkins')

from tests.trayjenkins.EventTests import EventTests  # @UnusedImport

from tests.trayjenkins.test_jobs import *  # @UnusedWildImport
from tests.trayjenkins.test_settings import *  # @UnusedWildImport
from tests.trayjenkins.test_status import *  # @UnusedWildImport

from tests.gui.test_jobs import *  # @UnusedWildImport
from tests.gui.test_status import *  # @UnusedWildImport

if __name__ == '__main__':
    unittest.main(testRunner=unittest.TextTestRunner(stream=sys.stdout, verbosity=2))
