#!/usr/bin/env python

import argparse
import coloredlogs
import logging
from metermonitor import Config, Viewer, NullViewer, Camera, Monitor, Meter

coloredlogs.install()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Read command line args
parser = argparse.ArgumentParser(description='Monitor a water meter')

parser.add_argument('-m', '--modes', default='LIVE', help='Comma-separated modes to run this program in. May include DEBUG, CALIBRATE')

requiredNamed = parser.add_argument_group('Required named arguments')
requiredNamed.add_argument('-c', '--configFile', help='Path to configuration file for this meter', required=True)

args = parser.parse_args()

logger.info('Run %s with config from %s', args.modes, args.configFile)

# Build app configuration
config = Config(args.configFile, args.modes)

meter = Meter(config)
viewer = Viewer() if config.is_calibrate() else NullViewer()
camera = Camera(config.device(), config.meter_face())
monitor = Monitor(config, viewer, camera, meter)

logger.info('Start polling camera')

while monitor.is_online():
    monitor.poll()
