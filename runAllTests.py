#!/usr/bin/python

import unittest
import sys

sys.path.append('submodules/pyjenkins')

from tests.trayjenkins.EventTests import EventTests

from tests.trayjenkins.test_jobs import *
from tests.trayjenkins.test_status import *

from tests.gui.test_jobs import *
from tests.gui.test_status import *

if __name__ == '__main__':
    unittest.main(testRunner=unittest.TextTestRunner(stream=sys.stdout, verbosity=2))
