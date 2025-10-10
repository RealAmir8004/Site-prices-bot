from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class UpdateWorker(QObject):
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
                        self.updated.emit(d)
                    except Exception as e:
                        self.error.emit(str(e))
        except Exception as e:
            self.error.emit(str(e))
        finally:
            self.finished.emit()

    def stop(self):
        self._stopped = True
