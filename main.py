from PyQt5.QtWidgets import QApplication 
import UI
import sys
from dataClass import DataList , DataDB
from import_logging import get_logger
from workers import UpdateWorker
from PyQt5.QtCore import QThread
import msvcrt
# RESULTS defined in constants.py

logger = get_logger(__name__)

class MainController:
    def __init__(self , use_db , updateAll ,retry_failures):
        self.db = DataDB()
        self.app = QApplication(sys.argv)
        self.ui_window = UI.MainApp()
        try:
            self.data_list = DataList(self.db , use_db)
        except Exception as e:
            UI.critical_message(e)
            sys.exit(1)

        self.ui_window.set_len_list(self.data_list.len)
        self.update_worker = None
        self.update_thread = None
        if updateAll:
            self.start_background_updater(retry_failures)

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
        log_changes = []
        if chosen != d.chosen_site :
            d.chosen_site = chosen
            self.db.update_chosen(d)
            log_changes.append(f"new_price:→ {changed_price}")
        self.ui_window.spinBox_newQuantity.interpretText()
        new_quantity = self.ui_window.spinBox_newQuantity.value()
        if new_quantity != d.new_quantity:
            d.new_quantity = new_quantity
            self.db.update_quantity(d)
            log_changes.append(f"new_quantity:→{new_quantity}")
        if log_changes:
            combined = " | ".join(log_changes)
            logger.info(combined)
            logger.important(f"ID='{d.id}': {combined}")
        else :
            logger.info("no changes from previous choice for price or quantity")

    def start_background_updater(self, retry_failures: bool):
        self.update_thread = QThread()
        self.update_worker = UpdateWorker(self.data_list, retry_failures)
        self.update_worker.moveToThread(self.update_thread)
        self.update_thread.started.connect(self.update_worker.run)

        def on_updated(product_id):
            try:
                curr = self.data_list.current()
            except Exception:
                return
            # compare product ids so we don't access private indices
            if curr.id == product_id:
                # request the UI to refresh current shown data
                self.ui_window.dataChanged.emit(self.data_list.showData(False))

        self.update_worker.updated.connect(on_updated)
        # log errors and finish
        self.update_worker.error.connect(lambda e: logger.error(f"Background update error: {e}"))
        self.update_worker.finished.connect(lambda: logger.info("Background updater finished."))
        self.update_thread.start()

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
        try:
            sys.exit(self.app.exec_())
        finally:
            # ensure worker stops and thread quits on app exit
            if self.update_worker:
                try:
                    self.update_worker.stop()
                except Exception:
                    pass
            if self.update_thread:
                self.update_thread.quit()
                self.update_thread.wait()


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

