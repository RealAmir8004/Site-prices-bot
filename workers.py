from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from dataClass import DataDB, DB_PATH


class UpdateWorker(QObject):
    """Background updater that updates Data objects and persists changes to DB.

    Emits:
        updated(index: int) - when an item is updated (so UI may refresh)
        finished() - when work is done
        error(str) - on unexpected errors
    """
    updated = pyqtSignal(int)
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, data_list, retry_failures=False):
        super().__init__()
        self.data_list = data_list
        self.retry_failures = retry_failures
        self._stopped = False

    @pyqtSlot()
    def run(self):
        try:
            # create a local DB connection inside this thread
            local_db = DataDB()
            items = self.data_list.__list_data
            for d in items:
                if self._stopped:
                    break
                if self.retry_failures:
                    condition = (d.sites is None) or (len(d.sites) > 1 and d.sites[1].name is None)
                else:
                    condition = d.sites is None
                if condition:
                    try:
                        d.update()
                        local_db.update(d)
                        # notify UI that product with id was updated (emit id to avoid exposing internal indices)
                        self.updated.emit(d.id)
                    except Exception as e:
                        # log and continue
                        self.error.emit(str(e))
            local_db.close()
        except Exception as e:
            self.error.emit(str(e))
        finally:
            self.finished.emit()

    def stop(self):
        self._stopped = True
