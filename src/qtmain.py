import os.path
import logging


from src.layout import Ui_MainWindow
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QFileDialog
from src.thread_worker import WorkerThread

PASSWORD_CONFIG_DEFAULT_PATH = "password_config.xlsx"
logging.basicConfig(level=logging.DEBUG, filename='log.log')
class UiMainWindow(Ui_MainWindow):
    def __init__(self, main_window: QtWidgets.QMainWindow):
        super(UiMainWindow, self).__init__()
        self.setupUi(main_window)
        self.connect_signals()

        if os.path.isfile(PASSWORD_CONFIG_DEFAULT_PATH):
            self.config_file.setText(os.path.abspath(PASSWORD_CONFIG_DEFAULT_PATH))


    def connect_signals(self):
        self.select_input_folder.pressed.connect(
            lambda: self.select_folder_name(self.input_folder, "Input folder", True))
        self.select_output_folder.pressed.connect(
            lambda: self.select_folder_name(self.output_folder, "Output folder", True))
        self.select_file_with_config.pressed.connect(
            lambda: self.select_folder_name(self.config_file, "Config file", False))

        # Connect the button to the slot
        self.submit.clicked.connect(self.start_task)

    def select_folder_name(self, line_edit: QtWidgets.QLineEdit, caption: str, is_folder=True):
        if is_folder:
            input1 = QFileDialog.getExistingDirectory(caption=f"Select {caption}")
        else:
            input1 = QFileDialog.getOpenFileName(caption=f"Select {caption}")[0]
        line_edit.setText(input1)

    def start_task(self):
        """Slot to start the task in a separate thread."""
        # Disable the button to prevent multiple clicks
        self.submit.setEnabled(False)

        # Create and start the worker thread
        self.worker_thread = WorkerThread(self.input_folder.text(),
                                          self.output_folder.text(),
                                          self.config_file.text())
        self.worker_thread.progress_signal.connect(self.update_progress)
        self.worker_thread.logger_signal.connect(self.update_logger)
        self.worker_thread.start()

    def update_logger(self, text):
        old_text = self.log_label.toPlainText()
        if len(old_text) > 0:
            old_text += "\n"
        new_text = old_text + text
        self.log_label.setText(new_text)
        logging.log(10, text)

    def update_progress(self, value):
        """Slot to update the progress in the UI."""
        # Update the progress in the UI
        self.submit.setText(f"Progress: {value}%")
        if value == 100:
            self.submit.setEnabled(True)  # Enable the button after task completion
