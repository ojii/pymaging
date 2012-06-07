#!/bin/bash

PYTHON_VERSIONS="2.6 2.7 3.1 3.2 3.3"
NOSEBIN=`which nosetests`

if [ -z $NOSEBIN ]; then
    NOSEBIN="-m unittest discover"
fi

for version in $PYTHON_VERSIONS; do
    pybin="python$version"
    if [ `which $pybin` ]; then
        echo "****************************"
        echo "Running tests for Python $version"
        echo "****************************"
        $pybin $NOSEBIN
    fi
done

if [ `which pypy` ]; then
    pypyversion=`pypy -c "import sys;print(sys.version).splitlines()[1]"`
    echo "**************************************************"
    echo "Running tests for PyPy $pypyversion"
    echo "**************************************************"
    pypy $NOSEBIN
fi
