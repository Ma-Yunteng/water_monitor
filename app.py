import logging
from metermonitor import Config, Viewer, NullViewer, Camera, Monitor, Meter

logger = logging.getLogger(__name__)


def app(config, modes):
    config = Config(config, modes)
    meter = Meter(config)
    viewer = Viewer() if config.is_calibrate() else NullViewer()
    camera = Camera(config.device(), config.meter_face())
    monitor = Monitor(config, viewer, camera, meter)

    logger.info('Start polling camera')

    while monitor.is_online():
        monitor.poll()
