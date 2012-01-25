#!/usr/bin/python

import unittest
import sys
import os

sys.path.append('submodules/pyjenkins')

from tests.server.ModelTests import ModelTests as ServerModelTests

from tests.status.ModelTests import ModelTests as StatusModelTests
from tests.status.PresenterTests import PresenterTests
from tests.status.StatusReaderTests import StatusReaderTests

if __name__ == '__main__':
    unittest.main(testRunner= unittest.TextTestRunner(stream= sys.stdout, verbosity=2))
