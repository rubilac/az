import logging
logging.basicConfig(filename = "/opt/dev/az/log/inventory.log", level = logging.DEBUG)
logger = logging.getLogger()
logger.info("Test message")
