import logging.handlers
import os
import sys
import time


LOG_HANDLERS = ['console', 'file']
log_level = logging.INFO
log_file = os.path.join("fast_api" + "_" + time.strftime("%Y%m%d") + '.log')

logger = logging.getLogger("SCHEDULING APP")
logger.setLevel(log_level)


formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s  - %(filename)s - %(module)s: '
                              '%(funcName)s: %(lineno)d - %(message)s')

if 'console' in LOG_HANDLERS:
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

if 'file' in LOG_HANDLERS:
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

logger.info("Logging is now set up.")
