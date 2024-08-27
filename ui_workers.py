from PyQt5.QtCore import QThread, pyqtSignal
from utils.converters import testcase
class Worker(QThread):
    sign_out = pyqtSignal(str)
    exception_out = pyqtSignal(Exception, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.sender = None
        self.files = []
        self.output_format = 0

    def __del__(self):
        self.wait()

    def put_into(self, sender, files, output_fmt=0):
        self.sender = sender
        self.files = files
        self.output_format = output_fmt
        self.start()

    def run(self):
        for file in self.files:
            button_text = self.sender.text()
            if button_text == "生成Excel案例":
                file_type = "excel"
            else:
                file_type = "csv"
            try:
                output_file = testcase.build(file, self.output_format, file_type)

            except PermissionError as e:
                self.exception_out.emit(e, file)
            except Exception as e:
                self.exception_out.emit(e, file)
            else:
                self.sign_out.emit(output_file)
