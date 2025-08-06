import logging
import sys

IMPORTANT_LEVEL_NUM = 55
logging.addLevelName(IMPORTANT_LEVEL_NUM, "IMPORTANT")

def important(self, message, *args, **kwargs):
    if self.isEnabledFor(IMPORTANT_LEVEL_NUM):
        self._log(IMPORTANT_LEVEL_NUM, message, args, **kwargs)

logging.Logger.important = important
_seripator_printed = False

def get_logger(name):
    global _seripator_printed
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = logging.FileHandler("app.log", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)

    important_fh = logging.FileHandler("important.log", encoding="utf-8")
    important_fh.setLevel(IMPORTANT_LEVEL_NUM)
    important_fh.setFormatter(formatter)
    important_fh.addFilter(lambda record: record.levelno == IMPORTANT_LEVEL_NUM)

    if not logger.hasHandlers():
        if not _seripator_printed:
            header = "_" * 114 + "\n"
            for handler in (file_handler, important_fh):
                handler.stream.write(header)
                handler.stream.flush()
            _seripator_printed = True

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
        logger.addHandler(important_fh)

    return logger