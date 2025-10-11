from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from import_logging import get_logger
from import_logging import background_thread_logging

logger = get_logger(__name__)

class UpdateWorker(QObject):
    updated = pyqtSignal(object)
    progress = pyqtSignal(int)

    def __init__(self, data_list, retry_failures=False):
        super().__init__()
        self.data_list = data_list
        self.retry_failures = retry_failures
        self._stopped = False

    @pyqtSlot()
    def run(self):
        logger.background("UpdateWorker started ----------")
        try:
            items = self.data_list._DataList__list_data
            for idx, d in enumerate(items):
                if self._stopped:
                    break
                if self.retry_failures:
                    condition = (d.sites is None) or (len(d.sites) > 1 and d.sites[1].name is None)
                else:
                    condition = d.sites is None
                if condition:
                    try:
                        background_thread_logging(True)
                        d.update()
                        background_thread_logging(False)
                        self.updated.emit(d)
                    except Exception as e:
                        background_thread_logging(False) #making sure
                        logger.background(f"error : {e}")
                try:
                    self.progress.emit(idx)
                except Exception:
                    logger.background("failed to emit progress signal")
        except Exception as e:
            logger.background(f"exception : {e}")
        finally:
            logger.background("UpdateWorker finished ----------")

    def stop(self):
        self._stopped = True
