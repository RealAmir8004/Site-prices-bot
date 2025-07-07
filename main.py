from PyQt5.QtWidgets import QApplication , QMessageBox
from UI import MainApp
import sys
from dataClass import DataList
from scraping import Site
from import_logging import get_logger
# RESULTS defined in constants.py

logger = get_logger(__name__)

class MainController:
    def __init__(self): # ina ghable run shoden ui anjam mishan
        self.app = QApplication(sys.argv)
        self.ui_window = MainApp()
        try:
            self.data_list = DataList()
        except Exception as e:
            QMessageBox.critical(self.ui_window, "Error", str(e))
            sys.exit(1)

        self.ui_window.nextButton.clicked.connect(self.handle_next_button)
        self.ui_window.backButton.clicked.connect(self.handle_back_button)
        self.ui_window.saveButton.clicked.connect(self.handle_save_button)
        
        self.ui_window.update_table(self.data_list.showData(True))

    def handle_next_button(self):
        checked_button = self.ui_window.radioButtonGroup.checkedButton()

        chosen_one = None

        if checked_button is None:
            logger.warning("Next clicked ->checked radio = None")
            QMessageBox.critical(self.ui_window, "warning", "No Option selected")
            return
        elif checked_button == self.ui_window.radioButton_0:
            chosen_one = "0"
        elif checked_button == self.ui_window.radioButton_1:
            chosen_one = "1"
        elif checked_button == self.ui_window.radioButton_2:
            chosen_one = "2"
        elif checked_button == self.ui_window.radioButton_3:
            chosen_one = "3"
        elif checked_button == self.ui_window.radioButton_4:
            chosen_one = "4"
        elif checked_button == self.ui_window.radioButton_5:
            chosen_one = "5"
        elif checked_button == self.ui_window.radioButton_6:
            self.ui_window.spinBox.interpretText()
            chosen_one = self.ui_window.spinBox.value()

        self.data_list.current().chosen_site = chosen_one
        logger.debug(f"Next clicked ->checked radio = {chosen_one}")

        self.ui_window.dataChanged.emit(self.data_list.showData(True))


    def handle_save_button(self):
        logger.debug("Save button clicked!")

    def handle_back_button(self):
        logger.debug(f"Back clicked ") 
        self.ui_window.dataChanged.emit(self.data_list.showData(False))

    def run(self):
        self.ui_window.show()
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    with open("app.log", "a", encoding="utf-8") as f:
        f.write("--------------------------------------------------------------------------------------------------------------\n")
    logger.info("Starting MainController")
    controller = MainController()
    controller.run()

