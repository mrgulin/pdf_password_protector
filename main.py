import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from src.qtmain import UiMainWindow
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
MainWindow.setWindowTitle("PDF password protector")
ui = UiMainWindow(MainWindow)

MainWindow.show()
sys.exit(app.exec())