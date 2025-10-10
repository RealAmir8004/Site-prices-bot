import logging
import sys

IMPORTANT_LEVEL_NUM = 5
BACK_THREAD_LEVEL_NUM = 6
logging.addLevelName(IMPORTANT_LEVEL_NUM, "IMPORTANT")
logging.addLevelName(BACK_THREAD_LEVEL_NUM, "BACKGROUND")

def important(self, message, *args, **kwargs):
    if self.isEnabledFor(IMPORTANT_LEVEL_NUM):
        self._log(IMPORTANT_LEVEL_NUM, message, args, **kwargs)

def background(self, message, *args, **kwargs):
    if self.isEnabledFor(BACK_THREAD_LEVEL_NUM):
        self._log(BACK_THREAD_LEVEL_NUM, message, args, **kwargs)

logging.Logger.important = important
logging.Logger.background = background

def _important_filter(record):
    return record.levelno == IMPORTANT_LEVEL_NUM

def _background_filter(record):
    return record.levelno == BACK_THREAD_LEVEL_NUM

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.NOTSET)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    simple_formatter = logging.Formatter('%(asctime)s - %(message)s')

    app = logging.FileHandler("app.log", encoding="utf-8")
    app.setLevel(logging.DEBUG)
    app.setFormatter(formatter)

    terminal = logging.StreamHandler(sys.stdout)
    terminal.setLevel(logging.DEBUG)
    terminal.setFormatter(formatter)

    important = logging.FileHandler("important.log", encoding="utf-8")
    important.setLevel(IMPORTANT_LEVEL_NUM)
    important.setFormatter(simple_formatter)
    important.addFilter(_important_filter)

    background = logging.FileHandler("background_updating.log", encoding="utf-8")
    background.setLevel(BACK_THREAD_LEVEL_NUM)
    background.setFormatter(simple_formatter)
    background.addFilter(_background_filter)

    if not logger.hasHandlers():
        logger.addHandler(app)
        logger.addHandler(terminal)
        logger.addHandler(important)
        logger.addHandler(background)

    if name == "__main__" :
        header = '"' + "_" * 113 + '"'
        logger.info(header)
        logger.important(header)
        logger.background(header)
    return logger