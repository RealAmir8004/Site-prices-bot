import logging
import sys

IMPORTANT_LEVEL_NUM = 5
logging.addLevelName(IMPORTANT_LEVEL_NUM, "IMPORTANT")

def important(self, message, *args, **kwargs):
    if self.isEnabledFor(IMPORTANT_LEVEL_NUM):
        self._log(IMPORTANT_LEVEL_NUM, message, args, **kwargs)

logging.Logger.important = important

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(IMPORTANT_LEVEL_NUM)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = logging.FileHandler("app.log", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)

    important_fh = logging.FileHandler("important.log", encoding="utf-8")
    important_fh.setLevel(IMPORTANT_LEVEL_NUM)
    important_fh.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
    important_fh.addFilter(lambda record: record.levelno == IMPORTANT_LEVEL_NUM)

    if not logger.hasHandlers():
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
        logger.addHandler(important_fh)

    if name == "__main__" :
        header = '"' + "_" * 113 + '"'
        logger.info(header)
        logger.important(header)
    return logger