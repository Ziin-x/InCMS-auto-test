import logging
from config.setting import LOG_CONFIG


def get_logger(name='pyUI0103', file='pyUI0103.log',
               fmt='%(levelname)s %(asctime)s [%(filename)s-->line:%(lineno)d]:%(message)s', debug=False):
    logger = logging.getLogger(name)
    # 如果已经有 handler，说明已经配置过，直接返回
    if logger.handlers:
        return logger

    if debug:
        file_level = logging.DEBUG
        console_level = logging.DEBUG
    else:
        file_level = logging.WARNING
        console_level = logging.INFO

    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(filename=file, encoding='utf-8')
    file_handler.setLevel(file_level)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)

    formatter = logging.Formatter(fmt=fmt)
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


# 确保只调用一次
logger = get_logger(**LOG_CONFIG)