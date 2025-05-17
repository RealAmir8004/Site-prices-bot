from PyQt5.QtWidgets import QApplication
from UI import MainApp
import sys
from dataClass import CsvData
from scraping import Site

def handle_next_button(ui_window, csv_list: CsvData):
    checked_button = ui_window.radioButtonGroup.checkedButton()

    current_data = csv_list.current()
    if current_data is None or not current_data.sites:
        print("No data available or sites are not populated!")
        return

    chosen_one = None

    if checked_button is None:
        print("No option selected!")
        chosen_one = 0 
    elif checked_button == ui_window.radioButton_1:
        chosen_one = current_data.sites[0]
    elif checked_button == ui_window.radioButton_2:
        chosen_one = current_data.sites[1]
    elif checked_button == ui_window.radioButton_3:
        chosen_one = current_data.sites[2]
    elif checked_button == ui_window.radioButton_4:
        chosen_one = current_data.sites[3]
    elif checked_button == ui_window.radioButton_5:
        chosen_one = current_data.sites[4]
    elif checked_button == ui_window.radioButton_6:
        chosen_one = Site("Custom", ui_window.spinBox.value())

    current_data.chose_site(chosen_one) 

    ui_window.dataChanged.emit(csv_list.showData(True))


# RESULTS defined in constants.py
# main.py :
if __name__ == "__main__" :
    csv_list = CsvData()
    app = QApplication(sys.argv)
    ui_window = MainApp()

    ui_window.update_table(csv_list.showData(True)) # showing first data
    
    ui_window.nextButton.clicked.connect(lambda: handle_next_button(ui_window, csv_list))
    ui_window.backButton.clicked.connect(lambda: ui_window.dataChanged.emit(csv_list.showData(False)))
    ui_window.saveButton.clicked.connect(lambda: print("Custom Save logic"))

    ui_window.show()
    sys.exit(app.exec_())

