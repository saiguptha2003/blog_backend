import logging
import sys
from logging.handlers import RotatingFileHandler
import os

logs_dir = "logs"
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

logger = logging.getLogger("BlogApp")
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_format)

file_handler = RotatingFileHandler(
    os.path.join(logs_dir, 'app.log'),
    maxBytes=1024*1024,
    backupCount=5
)
file_handler.setLevel(logging.DEBUG)
file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')
file_handler.setFormatter(file_format)

logger.addHandler(console_handler)
logger.addHandler(file_handler)