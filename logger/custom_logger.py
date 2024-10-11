import logging

# Create a logger object
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Initial logging level

# Create a console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)  # Handler logging level

# Create a formatter and set it for the handler
formatter = logging.Formatter('[%(asctime)s] - [%(levelname)s] - [%(module)s.%(funcName)s] - %(message)s')
ch.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(ch)

# Disable logging by default by setting logger and handler levels higher than CRITICAL
logger.setLevel(logging.CRITICAL + 1)  # No messages will pass this level
# Disable logging globally by default
logging.disable(logging.CRITICAL)

# Function to enable logging
def enable_logger():
    logger.setLevel(logging.DEBUG)
    ch.setLevel(logging.DEBUG)
    logging.disable(logging.NOTSET)


# Function to disable logging
def disable_logger():
    logger.setLevel(logging.CRITICAL + 1)  # Higher than CRITICAL
    ch.setLevel(logging.CRITICAL + 1)
    logging.disable(logging.CRITICAL)
