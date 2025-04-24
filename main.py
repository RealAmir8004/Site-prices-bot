from PyQt5.QtWidgets import QApplication
from UI import MainApp
import sys
from data import CsvData

# main.py :
def main():
    csv_list = CsvData()
    app = QApplication(sys.argv)
    ui_window = MainApp()

    ui_window.nextButton.clicked.connect(lambda: ui_window.next_clicked(csv_list.nextData()))
    ui_window.backButton.clicked.connect(lambda: print("Custom Back logic"))
    ui_window.saveButton.clicked.connect(lambda: print("Custom Save logic"))

    ui_window.show()
    sys.exit(app.exec_())


main()