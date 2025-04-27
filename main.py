from PyQt5.QtWidgets import QApplication
from UI import MainApp
import sys
from dataClass import CsvData

# RESULTS defined in scraping.py 
# main.py :
if __name__ == "__main__" :
    csv_list = CsvData()
    app = QApplication(sys.argv)
    ui_window = MainApp()

    ui_window.nextButton.clicked.connect(lambda: ui_window.dataChanged.emit(csv_list.showData(True)))
    ui_window.backButton.clicked.connect(lambda: ui_window.dataChanged.emit(csv_list.showData(False)))
    ui_window.saveButton.clicked.connect(lambda: print("Custom Save logic"))

    ui_window.show()
    sys.exit(app.exec_())

