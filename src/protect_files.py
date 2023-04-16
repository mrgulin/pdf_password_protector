import pandas as pd
import pikepdf
import os
import traceback


class FileProtector:
    def __init__(self, input_folder, output_folder, config_file_path, signal_update=None, signal_logger=None):
        self.config: pd.DataFrame = pd.read_excel(config_file_path)
        self.config.columns = ['name', 'password', 'search']
        self.input_folder = input_folder
        self.output_folder = output_folder

        self.signal_update = signal_update
        self.signal_logger = signal_logger


    def main(self):
        self.emit_logging_signal("Starting the script")
        if not os.path.isdir(self.input_folder):
            self.emit_logging_signal("ERROR: Input folder doesn't exists!")
        if not os.path.isdir(self.output_folder):
            self.emit_logging_signal("ERROR: Output folder doesn't exists!")

        input_files = os.listdir(self.input_folder)
        for file_id, one_file in enumerate(input_files):
            self.update_signal(file_id, len(input_files))
            file_extension = os.path.splitext(one_file)[1]
            if file_extension.lower() != ".pdf":
                self.emit_logging_signal(f" ERROR: {one_file} is not a pdf!")
                continue

            binary_filter = self.config['search'].apply(lambda x: x in one_file)
            if binary_filter.sum() == 0:
                self.emit_logging_signal(f" ERROR: {one_file} doesn't contain any pattern in config file!")
                continue
            elif binary_filter.sum() > 1:
                self.emit_logging_signal(f" ERROR: {one_file} matches with multiple patterns "
                                        f"({self.config.loc[binary_filter, 'name'].to_list()}).")
                continue

            person_info = self.config.loc[binary_filter, :].squeeze()

            try:
                with pikepdf.Pdf.open(os.path.join(self.input_folder, one_file)) as pdf:
                    pdf.save(os.path.join(self.output_folder, one_file),
                             encryption=pikepdf.Encryption(owner=person_info['password'], user=person_info['password']))

                self.emit_logging_signal(f"SUCCESS: {one_file} was transformed succesfully")
            except Exception as e:
                print(e)
                self.emit_logging_signal(f"ERROR: {onefile} threw an exception: \n" + traceback.format_exc())
        self.update_signal(1, 1)

    def update_signal(self, current_index, length):
        if self.signal_update is not None:
            self.signal_update.emit(int((current_index) / length * 100))

    def emit_logging_signal(self, string):
        if self.signal_logger is None:
            print(string)
        else:
            self.signal_logger.emit(string)


if __name__ == '__main__':
    print("TEST!")
    FileProtector('../debug/input1', '../debug/output1', '../password_config.xlsx').main()
