import logging
import sys
import threading

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

# thread-local flag to mark a thread as a background worker
_thread_local = threading.local()

def background_thread_logging(flag: bool):
    setattr(_thread_local, 'is_background', bool(flag))

def is_background_logging() -> bool:
    return getattr(_thread_local, 'is_background', False)

def _background_filter(record):
    if record.levelno == BACK_THREAD_LEVEL_NUM:
        return True
    # If thread is flagged as background, accept all records from it
    return is_background_logging()

def _exclude_background_filter(_record) -> bool:
    return not is_background_logging()

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(IMPORTANT_LEVEL_NUM) # dont use logging.NOTSET → it will convert to warning

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    simple_formatter = logging.Formatter('%(asctime)s - %(message)s')

    app = logging.FileHandler("app.log", encoding="utf-8")
    app.setLevel(logging.DEBUG)
    app.setFormatter(formatter)
    app.addFilter(_exclude_background_filter)

    terminal = logging.StreamHandler(sys.stdout)
    terminal.setLevel(logging.DEBUG)
    terminal.setFormatter(formatter)
    terminal.addFilter(_exclude_background_filter)

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