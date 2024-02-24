# logger_setup.py
import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

class LoggerConfig:
    CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

def generate_log_file_name(log_type):
    current_time = datetime.now()
    return os.path.join(LoggerConfig.CURRENT_PATH, f"log_{log_type}_{current_time.strftime('%Y%m%d_%H%M%S')}.log")

def setup_logger():
    loggers_config = {
        'info': {
            'file': generate_log_file_name('info'),
            'level': logging.INFO,
            'format': '%(asctime)s - %(levelname)s - %(message)s',
            'rotation_size': 10,
            'backup_count': 5
        },
        'error': {
            'file': generate_log_file_name('error'),
            'level': logging.ERROR,
            'format': '%(asctime)s - %(levelname)s - %(message)s',
            'rotation_size': 10,
            'backup_count': 5
        }
    }

    loggers = {}
    for logger_name, config in loggers_config.items():
        logger = logging.getLogger(logger_name)
        logger.setLevel(config['level'])

        formatter = logging.Formatter(config['format'])

        file_handler = RotatingFileHandler(config['file'], maxBytes=config['rotation_size'] * 1024 * 1024,
                                           backupCount=config['backup_count'])
        file_handler.setLevel(config['level'])
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        loggers[logger_name] = logger

    return loggers
