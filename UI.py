from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow , QProgressDialog , QMessageBox , QApplication
from PyQt5.QtCore import pyqtSlot , pyqtSignal , QLocale
from constants import RESULTS
from import_logging import get_logger
import sys

logger = get_logger(__name__)

# WARNING: Do not do any update in Ui_MainWindow class 
# Ui_MainWindow exacly copyd from .py file created by qt designer ( PyQt5 UI code generator 5.15.11)
# only change Ui_MainWindow in qt designer (create a versionN.ui )

# generated from reading ui file 'version4.ui' 
# +all extra are removed
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1010, 656)
        MainWindow.setWindowTitle("MainWindow")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_productName = QtWidgets.QLabel(self.centralwidget)
        self.label_productName.setGeometry(QtCore.QRect(70, 10, 631, 27))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_productName.setFont(font)
        self.label_productName.setText("Product")
        self.label_productName.setScaledContents(False)
        self.label_productName.setAlignment(QtCore.Qt.AlignCenter)
        self.label_productName.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.label_productName.setObjectName("label_productName")
        self.nextButton = QtWidgets.QPushButton(self.centralwidget)
        self.nextButton.setGeometry(QtCore.QRect(710, 540, 75, 23))
        self.nextButton.setFont(font)
        self.nextButton.setText("Next")
        self.nextButton.setObjectName("nextButton")
        self.backButton = QtWidgets.QPushButton(self.centralwidget)
        self.backButton.setGeometry(QtCore.QRect(600, 540, 75, 23))
        self.backButton.setFont(font)
        self.backButton.setText("Back")
        self.backButton.setObjectName("backButton")
        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setGeometry(QtCore.QRect(220, 540, 75, 23))
        self.saveButton.setFont(font)
        self.saveButton.setText("save")
        self.saveButton.setObjectName("saveButton")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 90, 981, 441))
        self.groupBox.setFont(font)
        self.groupBox.setTitle("PriceBox")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.line_6 = QtWidgets.QFrame(self.groupBox)
        self.line_6.setFont(font)
        self.line_6.setMidLineWidth(1)
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.gridLayout.addWidget(self.line_6, 13, 0, 1, 4)
        self.radioButton_4 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_4.setFont(font)
        self.radioButton_4.setText("sujjested price")
        self.radioButton_4.setObjectName("radioButton_4")
        self.radioButtonGroup = QtWidgets.QButtonGroup(MainWindow)
        self.radioButtonGroup.setObjectName("radioButtonGroup")
        self.radioButtonGroup.addButton(self.radioButton_4)
        self.gridLayout.addWidget(self.radioButton_4, 10, 3, 1, 1)
        self.radioButton_1 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_1.setFont(font)
        self.radioButton_1.setText("sujjested price")
        self.radioButton_1.setObjectName("radioButton_1")
        self.radioButtonGroup.addButton(self.radioButton_1)
        self.gridLayout.addWidget(self.radioButton_1, 3, 3, 1, 1)
        self.radioButton_5 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_5.setEnabled(True)
        self.radioButton_5.setFont(font)
        self.radioButton_5.setText("sujjested price")
        self.radioButton_5.setObjectName("radioButton_5")
        self.radioButtonGroup.addButton(self.radioButton_5)
        self.gridLayout.addWidget(self.radioButton_5, 12, 3, 1, 1)
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_2.setFont(font)
        self.radioButton_2.setText("sujjested price")
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButtonGroup.addButton(self.radioButton_2)
        self.gridLayout.addWidget(self.radioButton_2, 6, 3, 1, 1)
        self.radioButton_3 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_3.setFont(font)
        self.radioButton_3.setText("sujjested price")
        self.radioButton_3.setObjectName("radioButton_3")
        self.radioButtonGroup.addButton(self.radioButton_3)
        self.gridLayout.addWidget(self.radioButton_3, 8, 3, 1, 1)
        self.radioButton_0 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_0.setEnabled(True)
        self.radioButton_0.setFont(font)
        self.radioButton_0.setText("dont change price")
        self.radioButton_0.setCheckable(True)
        self.radioButton_0.setChecked(False)
        self.radioButton_0.setObjectName("radioButton_0")
        self.radioButtonGroup.addButton(self.radioButton_0)
        self.gridLayout.addWidget(self.radioButton_0, 0, 3, 1, 1)
        self.splitter = QtWidgets.QSplitter(self.groupBox)
        self.splitter.setFont(font)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.radioButton_6 = QtWidgets.QRadioButton(self.splitter)
        self.radioButton_6.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.radioButton_6.sizePolicy().hasHeightForWidth())
        self.radioButton_6.setSizePolicy(sizePolicy)
        self.radioButton_6.setMaximumSize(QtCore.QSize(16, 16))
        self.radioButton_6.setFont(font)
        self.radioButton_6.setText("")
        self.radioButton_6.setObjectName("radioButton_6")
        self.radioButtonGroup.addButton(self.radioButton_6)
        self.spinBox = QtWidgets.QSpinBox(self.splitter)
        self.spinBox.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox.sizePolicy().hasHeightForWidth())
        self.spinBox.setSizePolicy(sizePolicy)
        self.spinBox.setMinimumSize(QtCore.QSize(131, 20))
        self.spinBox.setMaximumSize(QtCore.QSize(131, 20))
        self.spinBox.setFont(font)
        self.spinBox.setMinimum(10000)
        self.spinBox.setMaximum(999999999)
        self.spinBox.setSingleStep(5000)
        self.spinBox.setObjectName("spinBox")
        self.gridLayout.addWidget(self.splitter, 14, 3, 1, 1)
        self.line_7 = QtWidgets.QFrame(self.groupBox)
        self.line_7.setFont(font)
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.gridLayout.addWidget(self.line_7, 4, 0, 1, 4)
        self.line_8 = QtWidgets.QFrame(self.groupBox)
        self.line_8.setFont(font)
        self.line_8.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.gridLayout.addWidget(self.line_8, 7, 0, 1, 4)
        self.line_9 = QtWidgets.QFrame(self.groupBox)
        self.line_9.setFont(font)
        self.line_9.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.gridLayout.addWidget(self.line_9, 11, 0, 1, 4)
        self.line_10 = QtWidgets.QFrame(self.groupBox)
        self.line_10.setFont(font)
        self.line_10.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_10.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_10.setObjectName("line_10")
        self.gridLayout.addWidget(self.line_10, 9, 0, 1, 4)
        self.line_11 = QtWidgets.QFrame(self.groupBox)
        self.line_11.setFont(font)
        self.line_11.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_11.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_11.setObjectName("line_11")
        self.gridLayout.addWidget(self.line_11, 2, 0, 1, 4)
        self.label_60 = QtWidgets.QLabel(self.groupBox)
        self.label_60.setFont(font)
        self.label_60.setText("custom price")
        self.label_60.setObjectName("label_60")
        self.gridLayout.addWidget(self.label_60, 14, 2, 1, 1)
        self.label_40 = QtWidgets.QLabel(self.groupBox)
        self.label_40.setFont(font)
        self.label_40.setText("base price")
        self.label_40.setObjectName("label_40")
        self.gridLayout.addWidget(self.label_40, 10, 2, 1, 1)
        self.label_30 = QtWidgets.QLabel(self.groupBox)
        self.label_30.setFont(font)
        self.label_30.setText("base price")
        self.label_30.setObjectName("label_30")
        self.gridLayout.addWidget(self.label_30, 8, 2, 1, 1)
        self.label_20 = QtWidgets.QLabel(self.groupBox)
        self.label_20.setFont(font)
        self.label_20.setText("base price")
        self.label_20.setObjectName("label_20")
        self.gridLayout.addWidget(self.label_20, 6, 2, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.groupBox)
        self.label_10.setFont(font)
        self.label_10.setText("base price")
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 3, 2, 1, 1)
        self.label_00 = QtWidgets.QLabel(self.groupBox)
        self.label_00.setFont(font)
        self.label_00.setText("old price")
        self.label_00.setObjectName("label_00")
        self.gridLayout.addWidget(self.label_00, 0, 2, 1, 1)
        self.label_50 = QtWidgets.QLabel(self.groupBox)
        self.label_50.setFont(font)
        self.label_50.setText("base price")
        self.label_50.setObjectName("label_50")
        self.gridLayout.addWidget(self.label_50, 12, 2, 1, 1)
        self.label_0 = QtWidgets.QLabel(self.groupBox)
        self.label_0.setFont(font)
        self.label_0.setText("(this may be first/middle/last line)if spark:null")
        self.label_0.setObjectName("label_0")
        self.gridLayout.addWidget(self.label_0, 0, 0, 1, 1)
        self.label_1 = QtWidgets.QLabel(self.groupBox)
        self.label_1.setFont(font)
        self.label_1.setText("(buy box) site name")
        self.label_1.setObjectName("label_1")
        self.gridLayout.addWidget(self.label_1, 3, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setFont(font)
        self.label_2.setText("site name")
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 6, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setFont(font)
        self.label_3.setText("site name")
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 8, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setFont(font)
        self.label_4.setText("site name")
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 10, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setFont(font)
        self.label_5.setText("site name")
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 12, 0, 1, 1)
        self.label_productCount = QtWidgets.QLabel(self.centralwidget)
        self.label_productCount.setGeometry(QtCore.QRect(650, 60, 201, 20))
        self.label_productCount.setFont(font)
        self.label_productCount.setText("1/100")
        self.label_productCount.setScaledContents(False)
        self.label_productCount.setObjectName("label_productCount")
        self.label_url = QtWidgets.QLabel(self.centralwidget)
        self.label_url.setGeometry(QtCore.QRect(50, 60, 581, 21))
        self.label_url.setText("<a href=\"https://example.com\">https://example.com</a>")
        self.label_url.setTextFormat(QtCore.Qt.RichText)
        self.label_url.setOpenExternalLinks(True)
        self.label_url.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard|QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextBrowserInteraction|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.label_url.setObjectName("label_url")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1010, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)



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
        self.local = QLocale()
        MainApp._instance = self 

    def __setup_connections(self):
        self.dataChanged.connect(self.update_table) 

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
            bg_color ="background-color: green;" if site.name == "اسپارک دیجی" else "background-color: red;" if site.badged  else "background-color: white;"
            if site.name == None :
                getattr(self, f"label_{i}").setText('')
                getattr(self, f"label_{i}0").setText('')
                getattr(self, f"radioButton_{i}").setText('')
                getattr(self, f"radioButton_{i}").setEnabled(False)
            else :
                getattr(self, f"label_{i}").setText(site.name)
                getattr(self, f"label_{i}0").setText(self.local.toString(site.price))
                if bg_color =="background-color: green;" :# "اسپارک دیجی" => suggested_price="dont change price" 
                    getattr(self, f"radioButton_{i}").setText(site.suggested_price)
                    dont_radio = i
                else :
                    getattr(self, f"radioButton_{i}").setText(self.local.toString(site.suggested_price))
                getattr(self, f"radioButton_{i}").setEnabled(True)
            getattr(self, f"label_{i}").setStyleSheet(bg_color)
            getattr(self, f"label_{i}0").setStyleSheet(bg_color)
            getattr(self, f"radioButton_{i}").setStyleSheet(bg_color)
        # must commit : bug fixed if sites[1 AND 0] both are unacceptbale

        try:
            self.spinBox.setValue(data.sites[0].suggested_price)
        except TypeError:
            try:
                self.spinBox.setValue(data.sites[1].suggested_price)
            except TypeError:
                pass
        self.__set_radio_checked(data,  dont_radio)
        logger.info(f"UI updated")

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