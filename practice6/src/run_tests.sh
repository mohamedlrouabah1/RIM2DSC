#!/usr/bin/bash
coverage run -m pytest
coverage report
coverage html