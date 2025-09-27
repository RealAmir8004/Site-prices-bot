from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow ,QTableWidget , QDialog ,QProgressDialog , QMessageBox , QApplication
from PyQt5.QtCore import Qt , pyqtSlot , pyqtSignal , QLocale
from constants import RESULTS
from import_logging import get_logger
import sys
from UI_mainWindow import Ui_MainWindow
from UI_translateDialog import Ui_TranslateDialog

logger = get_logger(__name__)

class TranslateApp(QDialog, Ui_TranslateDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.tableWidget.keyPressEvent = self.handle_keypress

    def handle_keypress(self, event):
        row = self.tableWidget.currentRow()
        col = self.tableWidget.currentColumn()

        if event.key() == Qt.Key_Delete:
            # Delete current row
            if row >= 0:
                self.tableWidget.removeRow(row)
        elif event.key() in (Qt.Key_Return, Qt.Key_Enter):
            if row == self.tableWidget.rowCount() - 1:
                self.tableWidget.insertRow(self.tableWidget.rowCount())
            self.tableWidget.setCurrentCell(min(row + 1, self.tableWidget.rowCount() - 1), col)
        else:
            # Default handling
            super(QTableWidget, self.tableWidget).keyPressEvent(event)

    def get_table_data(self):
        """Return table contents as a list of (col1, col2)."""
        data = []
        for row in range(self.tableWidget.rowCount()):
            col1 = self.tableWidget.item(row, 0).text() if self.tableWidget.item(row, 0) else ""
            col2 = self.tableWidget.item(row, 1).text() if self.tableWidget.item(row, 1) else ""
            data.append((col1, col2))
        return data

class MainApp(QMainWindow, Ui_MainWindow):
    _instance = None
    dataChanged = pyqtSignal(tuple)
    
    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        if MainApp._instance is not None:
            raise RuntimeError("Use MainApp.instance() to get the singleton instance.")
        super().__init__()
        self.setupUi(self)
        self.__setup_connections()
        self.local = QLocale(QLocale.Persian)
        self.radioButton_6.toggled.connect(self.spinBox.setEnabled)
        self.spinBox.setEnabled(self.radioButton_6.isChecked())
        MainApp._instance = self 

    def __setup_connections(self):
        self.dataChanged.connect(self.update_table) 
        self.action_translate.triggered.connect(self.open_translate_dialog)
    
    def open_translate_dialog(self):
        dlg = TranslateApp(self)
        dlg.exec_()
        
        data = dlg.get_table_data()
        print("Saved to db")
        print("Table contents:", data)


    def set_len_list(self , give_me_len_list : int):
        self.len_list = give_me_len_list

    @pyqtSlot(tuple)
    def update_table(self ,tuple_of_dataIndex):
        data , index = tuple_of_dataIndex
        if data is None:
            logger.warning("No data to display.")
            return
        if not data.sites or len(data.sites) < RESULTS: 
            logger.error("Data sites are not properly populated.")
            logger.error(f"len data.sites = {len(data.sites)}")
            return
        
        self.label_productName.setText(data.name)
        if index < 0 :
            index = self.len_list+index
        self.label_productCount.setText(f"{index+1}/{self.len_list} → id={data.id}")
        self.label_url.setText(f'<a href="{data.torob_url}">{data.torob_url}</a>') 

        for i, site in enumerate(data.sites):  
            bg_color ="background-color: red;" if site.badged else "background-color: white;"
            if site.name == None :
                getattr(self, f"label_{i}").setText('')
                getattr(self, f"radioButton_{i}").setText('')
                getattr(self, f"radioButton_{i}").setEnabled(False)
            else :
                getattr(self, f"label_{i}").setText(site.name)
                if site.name == "اسپارک دیجی":
                    getattr(self, f"radioButton_{i}").setText(site.suggested_price)
                    bg_color ="background-color: green;"
                    dont_radio = i
                else :
                    getattr(self, f"radioButton_{i}").setText(self.local.toString(site.suggested_price))
                getattr(self, f"radioButton_{i}").setEnabled(True)
            getattr(self, f"label_{i}0").setText(self.local.toString(site.price))
            getattr(self, f"label_{i}1").setText(site.city)
            getattr(self, f"label_{i}2").setText(site.score_text)
            getattr(self, f"label_{i}3").setText(site.last_change)

            getattr(self, f"label_{i}").setStyleSheet(bg_color)
            getattr(self, f"label_{i}1").setStyleSheet(bg_color)
            getattr(self, f"label_{i}2").setStyleSheet(bg_color)
            getattr(self, f"label_{i}3").setStyleSheet(bg_color)
            getattr(self, f"label_{i}0").setStyleSheet(bg_color)
            getattr(self, f"radioButton_{i}").setStyleSheet(bg_color)

        try:
            self.spinBox.setValue(data.sites[0].suggested_price)
        except TypeError:
            try:
                self.spinBox.setValue(data.sites[1].suggested_price)
            except TypeError:
                pass
        self.__set_radio_checked(data,  dont_radio)

    def __set_radio_checked(self , data , dont_radio):
        chosen = data.chosen_site
        if chosen is None :
            getattr(self, f"radioButton_{dont_radio}").setChecked(True)
        else :
            logger.debug(f"checking radio_checked from data (ram) = {chosen} ")
            if isinstance(chosen, str): #radioButton_0...5
                getattr(self, "radioButton_"+chosen).setChecked(True)
            else : #radioButton_6
                self.radioButton_6.setChecked(True)
                self.spinBox.setValue(chosen)  


def critical_message(message):
    QMessageBox.critical(MainApp.instance(), "!!!", str(message))

class ProgressDialog(QProgressDialog):
    def __init__(self):
        mainApp = MainApp.instance()
        self.max = mainApp.len_list
        super().__init__("Updating products...", "Cancel", 0, self.max, mainApp)
        self.setWindowTitle("Please Wait")
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowModality(QtCore.Qt.WindowModal)
        self.setMinimumDuration(0)
        self.setAutoClose(True)
        self.setAutoReset(True)
    
    def progress(self ,i) -> bool :
        self.setLabelText(f"Updating item {i + 1} of {self.max}")
        self.setValue(i + 1)
        QApplication.processEvents()
        if self.wasCanceled():
            return True
        return False


    @pyqtSlot()
    def back_clicked(self):
        pass

    @pyqtSlot()
    def save_clicked(self):
        logger.info("Save button clicked!")

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())