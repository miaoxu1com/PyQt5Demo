# coding=gb2312
__version__ = (2, 1, 2)

import ctypes

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")

import os
import sys

from PyQt5.QtGui import QIcon

if hasattr(sys, "frozen"):
    os.environ["PATH"] = sys._MEIPASS + ";" + os.environ["PATH"]
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog

from common.config import config
from ui.app import UiMainWindow, alert_yes
from ui.workers import Worker
from utils.io import files


class MainWindow(QMainWindow, UiMainWindow):
    input_files = []
    output_files = []

    def __init__(self, parent=None):

        super().__init__(parent)
        self.setWindowIcon(QIcon(r'D:\descrpypython\res\icons8-excel-48.svg'))
        self.setup_ui(self)
        self.setStyleSheet(files.read("config/style.qss"))
        self.worker = Worker()
        self.init_slots()

    def init_slots(self):
        """信号与槽"""
        self.output_format_field.currentIndexChanged.connect(self.output_format_selection_changed)
        for name, line_edit in self.fields.items():
            line_edit.textChanged.connect(self.text_changed)

        self.load_file_btn.clicked.connect(self.load_file)
        self.build_btn1.clicked.connect(self.on_build_started)
        self.build_btn2.clicked.connect(self.on_build_started)
        self.worker.sign_out.connect(self.on_build_finished)
        self.worker.exception_out.connect(self.on_exception_raised)
        self.worker.started.connect(self.on_started)
        self.worker.finished.connect(self.on_finished)

    def text_changed(self):
        line_edit = self.sender()
        label_text = self.form_layout.labelForField(line_edit).text()
        common_fields = config.get_item("common_fields")
        common_fields[label_text] = line_edit.text()
        config.save()

    def output_format_selection_changed(self):
        output_format = config.get_item("output_format")
        output_format["current_item"] = self.sender().currentText()
        config.save()

    def load_file(self):
        """选择文件"""
        self.browser.clear()
        selected_files, _ = QFileDialog.getOpenFileNames(self.widget, "选择思维导图文件", ".",
                                                         "思维导图 (*.mm; *.xmind)")
        self.input_files = selected_files
        for file in selected_files:
            self.browser.append(file)

    def on_started(self):
        """开始转换，按钮置灰"""
        self.build_btn1.setEnabled(False)
        self.build_btn2.setEnabled(False)

    def on_finished(self):
        """转换完毕，按钮恢复"""
        self.build_btn1.setEnabled(True)
        self.build_btn2.setEnabled(True)

    def on_build_started(self):
        """生成案例"""
        output_format = self.output_format_field.currentText()
        self.output.clear()
        self.output_files = []
        if self.input_files:
            self.worker.put_into(self.sender(), self.input_files, output_format)

    def on_build_finished(self, file):
        """输出结果"""
        if self.worker.sender in (self.build_btn1, self.build_btn2):
            self.output_files.append(file)
            self.output.append(file)

    def on_exception_raised(self, e, file):
        """子线程的异常处理"""
        if type(e) == PermissionError:
            alert_yes("错误提示", f"您已经打开与{file}同名文件，保存失败，请关闭后重试...    ")

    def closeEvent(self, event):
        config.save()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MainWindow()
    myWin.show()
    sys.exit(app.exec_())

# okay decompiling .\main.pyc
