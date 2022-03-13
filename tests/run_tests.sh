#!/bin/bash

export PYTHONPATH=/src

flake8 --ignore E24,W504,E501 --exclude=tests .
flakeExit=$?

if [ $flakeExit -ne 0 ]; then
    echo "flake error"
    exit $flakeExit
fi

# coverage run -m pytest
# coverage report -m
# coverage --rcfile=/src/tests/.coveragerc report
# --cov-config=/src/tests/.coveragerc
pytest # --cov-report term-missing --cov=src --cov-config=/src/tests/.coveragerc tests/
