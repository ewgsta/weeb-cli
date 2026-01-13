import logging
import os
from pathlib import Path
from datetime import datetime
from weeb_cli.config import config

_logger = None

def get_logger():
    global _logger
    if _logger is None:
        _logger = _setup_logger()
    return _logger

def _setup_logger():
    logger = logging.getLogger("weeb-cli")
    logger.setLevel(logging.DEBUG)
    logger.handlers = []
    
    if config.get("debug_mode", False):
        log_dir = Path.home() / ".weeb-cli" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / f"debug_{datetime.now().strftime('%Y%m%d')}.log"
        
        handler = logging.FileHandler(log_file, encoding='utf-8')
        handler.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(module)s:%(lineno)d | %(message)s',
            datefmt='%H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    else:
        logger.addHandler(logging.NullHandler())
    
    return logger

def debug(msg, *args):
    get_logger().debug(msg, *args)

def info(msg, *args):
    get_logger().info(msg, *args)

def warning(msg, *args):
    get_logger().warning(msg, *args)

def error(msg, *args):
    get_logger().error(msg, *args)

def reload():
    global _logger
    _logger = None
    get_logger()
