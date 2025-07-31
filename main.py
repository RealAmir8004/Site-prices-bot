from PyQt5.QtWidgets import QApplication 
import UI
import sys
from dataClass import DataList , DataDB
from import_logging import get_logger
# RESULTS defined in constants.py

logger = get_logger(__name__)

class MainController:
    def __init__(self): # ina ghable run shoden ui anjam mishan
        self.app = QApplication(sys.argv)
        self.ui_window = UI.MainApp()
        try:
            self.data_list = DataList()
        except Exception as e:
            UI.critical_message(e)
            sys.exit(1)

        self.ui_window.set_len_list(self.data_list.len)

        self.data_list.updateAll() # can be commented for not-updating All at first of program

        self.ui_window.nextButton.clicked.connect(self.handle_next_button)
        self.ui_window.backButton.clicked.connect(self.handle_back_button)
        self.ui_window.saveButton.clicked.connect(self.handle_save_button)
        
        self.ui_window.update_table(self.data_list.showData(True))

    def save_user_input(self):
        checked_button = self.ui_window.radioButtonGroup.checkedButton()
        if checked_button is None:
            logger.warning("->checked radio = None")
            UI.critical_message("No Option selected")
            return False
        checked_button = checked_button.objectName()[-1]
        logger.debug (f"->checked radio = {checked_button}")
        d = self.data_list.current()
        if checked_button == '6' :
            self.ui_window.spinBox.interpretText()
            d.chosen_site = self.ui_window.spinBox.value()
            logger.info(f"price updated from ={d.price} to ={d.chosen_site}")  
        else :# '1' , '2' , '3' , '4' , '5' 
            d.chosen_site = checked_button
            logger.info(f"price updated from ={d.price} to ={d.sites[int(d.chosen_site)].suggested_price}")  
        DataDB.instance().update_chosen(d)
        
    def handle_next_button(self):
        """save changes to memory and show next data"""
        logger.debug("Next clicked!")
        if self.save_user_input() is False :
            return 
        self.ui_window.dataChanged.emit(self.data_list.showData(True))

    def handle_save_button(self):
        """save all of changes maded untill now from memory to xlsx file"""
        logger.info("Save clicked!")
        self.save_user_input()
        self.data_list.saveData()
        UI.critical_message("Saved successfully")

    def handle_back_button(self):
        """save changes to memory (if changed)and show previuos data"""
        logger.debug(f"Back clicked!") 
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

