import argparse
from metermonitor import Config, Viewer, NullViewer, Camera

# Read command line args
parser = argparse.ArgumentParser(description='Monitor a water meter')

parser.add_argument('-configFile', help='Path to configuration file for this meter')
parser.add_argument('--modes', default='LIVE', help='Comma-separated modes to run this program in. May include DEBUG, CALIBRATE')
args = parser.parse_args()

print(args)
print('Run', args.modes, 'with config from', args.configFile)

# Build app configuration
config = Config(args.configFile, args.modes)

viewer = Viewer() if config.is_calibrate() else NullViewer()

camera = Camera(config.device())
