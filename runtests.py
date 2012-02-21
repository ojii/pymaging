#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest.main import TestProgram

class MyTestProgram(TestProgram):
    def parseArgs(self, argv):
        self._do_discovery([])

if __name__ == '__main__':
    MyTestProgram()
