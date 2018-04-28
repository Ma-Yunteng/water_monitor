#!/usr/bin/env python

import argparse
import coloredlogs
import logging
import app

logger = logging.getLogger(__name__)

# Read command line args
parser = argparse.ArgumentParser(description='Monitor a water meter')

parser.add_argument('-m', '--modes', default='LIVE', help='Comma-separated modes to run this program in. May include DEBUG, CALIBRATE')

requiredNamed = parser.add_argument_group('Required named arguments')
requiredNamed.add_argument('-c', '--configFile', help='Path to configuration file for this meter', required=True)

args = parser.parse_args()

if "LOG-DEBUG" in args.modes:
    coloredlogs.install(level=logging.DEBUG)
else:
    coloredlogs.install()

logger.info('Run with config from {} in modes {}'.format(args.configFile, args.modes))

app.app(args.configFile, args.modes)
