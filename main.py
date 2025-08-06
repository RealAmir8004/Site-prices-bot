from PyQt5.QtWidgets import QApplication 
import UI
import sys
from dataClass import DataList , DataDB
from import_logging import get_logger
import msvcrt
# RESULTS defined in constants.py

logger = get_logger(__name__)

class MainController:
    def __init__(self , use_db , updateAll ,retry_failures):
        self.app = QApplication(sys.argv)
        self.ui_window = UI.MainApp()
        try:
            self.data_list = DataList(use_db)
        except Exception as e:
            UI.critical_message(e)
            sys.exit(1)

        self.ui_window.set_len_list(self.data_list.len)
        if updateAll :
            self.data_list.updateAll(retry_failures)

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
        logger.debug(f"->checked radio = {checked_button}")
        d = self.data_list.current()
        if checked_button == '6' :
            self.ui_window.spinBox.interpretText()
            chosen = changed_price = self.ui_window.spinBox.value()
        else :# '1' , '2' , '3' , '4' , '5' 
            chosen = checked_button
            changed_price = d.sites[int(checked_button)].suggested_price

        if chosen != d.chosen_site :
            d.chosen_site = chosen
            DataDB.instance().update_chosen(d)
            logger.info(f"price updated from ={d.price} to ={changed_price}")
            logger.important(f"ID='{d.id}':→{changed_price}")
        else :
            logger.info(f"price didnt change from previous chosed !")

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


def get_bool_input(prompt: str) -> bool:
    """Prompt the user for True/False input (1/0)."""
    print(f"{prompt} (1 = Yes, 0 = No): ", end='', flush=True)
    while True:
        key = msvcrt.getch()
        if key == b'1':
            print('1')
            return True
        elif key == b'0':
            print('0')
            return False
        else:
            print("\nInvalid input. Please enter 1 or 0: ", end='', flush=True)


if __name__ == "__main__":
    use_db = get_bool_input("Continue previous run?")
    updateAll = get_bool_input("Run 'UpdateAll' at first?")
    retry_failures = get_bool_input("Retry failed updates?") if updateAll else False
    logger.info("Starting MainController")
    controller = MainController(use_db , updateAll ,retry_failures)
    controller.run()

