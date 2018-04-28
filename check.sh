#!/usr/bin/env bash

radon cc ./metermonitor/ -a --min B
flake8 --ignore=E501