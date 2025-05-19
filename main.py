from PyQt5.QtWidgets import QApplication
from UI import MainApp
import sys
from dataClass import CsvData
from scraping import Site
# RESULTS defined in constants.py

class MainController:
    def __init__(self):
        self.csv_list = CsvData()
        self.app = QApplication(sys.argv)
        self.ui_window = MainApp()

        self.ui_window.update_table(self.csv_list.showData(True))

        self.ui_window.nextButton.clicked.connect(self.handle_next_button)
        self.ui_window.backButton.clicked.connect(lambda: self.ui_window.dataChanged.emit(self.csv_list.showData(False)))
        self.ui_window.saveButton.clicked.connect(self.handle_save_button)

    def handle_next_button(self):
        checked_button = self.ui_window.radioButtonGroup.checkedButton()
        
        current_data = self.csv_list.current()
        if current_data is None or not current_data.sites:
            print("No data available or sites are not populated!")
            return

        chosen_one = None

        if checked_button is None:
            print("No option selected!")
            return
        elif checked_button == self.ui_window.radioButton_0:
            chosen_one = current_data.sites[0]
        elif checked_button == self.ui_window.radioButton_1:
            chosen_one = current_data.sites[1]
        elif checked_button == self.ui_window.radioButton_2:
            chosen_one = current_data.sites[2]
        elif checked_button == self.ui_window.radioButton_3:
            chosen_one = current_data.sites[3]
        elif checked_button == self.ui_window.radioButton_4:
            chosen_one = current_data.sites[4]
        elif checked_button == self.ui_window.radioButton_5:
            chosen_one = current_data.sites[5]
        elif checked_button == self.ui_window.radioButton_6:
            chosen_one = Site("Custom", self.ui_window.spinBox.value())

        current_data.chose_site(chosen_one)

        self.ui_window.dataChanged.emit(self.csv_list.showData(True))

    def handle_save_button(self):
        print("saved")

    def run(self):
        self.ui_window.show()
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    controller = MainController()
    controller.run()

