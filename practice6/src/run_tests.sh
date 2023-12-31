#!/usr/bin/bash
pip install coverage
pip install pytest
python3 practice6/test/conftest.py
coverage run -m pytest
coverage report
coverage html