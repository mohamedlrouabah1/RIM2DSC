#!/usr/bin/bash
pip install coverage
pip install pytest
coverage run -m pytest
coverage report
coverage html