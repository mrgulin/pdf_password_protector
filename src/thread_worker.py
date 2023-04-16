from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from src.protect_files import FileProtector

class WorkerThread(QThread):
    """WorkerThread class that runs a function in a separate thread."""
    # Define a custom signal to communicate with the main thread
    progress_signal = pyqtSignal(int)
    logger_signal = pyqtSignal(str)

    def __init__(self, input_folder, output_folder, config_file_path):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.config_file = config_file_path
        super().__init__()

    def run(self):
        """The function that will be run in a separate thread."""
        FileProtector(self.input_folder, self.output_folder, self.config_file, self.progress_signal,
                      self.logger_signal).main()