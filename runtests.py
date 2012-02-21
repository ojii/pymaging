#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest.main import TestProgram

class MyTestProgram(TestProgram):
    def parseArgs(self, argv):
        self._do_discovery(argv[1:])

def main():
    import optparse
    parser = optparse.OptionParser()
    parser.add_option('--coverage', dest='coverage', default=False, action='store_true')
    options, args = parser.parse_args()
    if options.coverage:
        import coverage
        cov = coverage.coverage(source=['notpil'], branch=True)
        cov.start()
    else:
        cov = None
    args.insert(0, 'runtests.py')
    try:
        MyTestProgram(argv=args)
    finally:
        if cov:
            cov.stop()
            cov.save()

if __name__ == '__main__':
    main()
