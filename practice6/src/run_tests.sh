#!/usr/bin/bash
pip install coverage
coverage run -m pytest
coverage report
coverage html