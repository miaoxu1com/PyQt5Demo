# 组件类
from PyQt5.QtWidgets import QWidget, QFrame, QMessageBox, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QLineEdit, QTextBrowser, QPushButton, QComboBox, QStatusBar
# Ui类
from PyQt5.QtGui import QFont
from common.config import config

class UiMainWindow(object):
    fields = {}
    merge_steps = False
    remove_seq_no = True

    def setup_ui(self, main_window):
        self.widget = QWidget(main_window)
        self.main_layout = QVBoxLayout(self.widget)
        self.main_layout.setContentsMargins(30, 20, 30, 20)
        self.set_title()
        self.add_hline(self.widget, self.main_layout)
        self.form_layout = QFormLayout()
        self.output_format_field = QComboBox(self.widget)
        self.output_format_field.setMinimumContentsLength(40)
        output_format = config.get_item("output_format")
        items = output_format["items"]
        current_item = output_format["current_item"]
        self.output_format_field.addItems([item for item in items])
        self.output_format_field.setCurrentText(current_item)
        self.form_layout.addRow("用例输出格式", self.output_format_field)
        fields = config.get_item("common_fields")
        for name, value in fields.items():
            line_edit = QLineEdit(value, self.widget)
            self.fields[name] = line_edit
            self.form_layout.addRow(name, line_edit)

        self.main_layout.addLayout(self.form_layout)
        self.add_hline(self.widget, self.main_layout)
        title_label = QLabel("已选择文件列表：")
        self.browser = QTextBrowser(self.widget)
        self.browser.setFixedHeight(100)
        self.load_file_btn = QPushButton("选择思维导图文件")
        for widget in (title_label, self.browser, self.load_file_btn):
            self.main_layout.addWidget(widget)

        self.add_hline(self.widget, self.main_layout)
        csv_layout = QHBoxLayout()
        self.build_btn1 = QPushButton("生成Excel案例")
        self.build_btn2 = QPushButton("生成CSV案例(utf8)")
        for widget in (self.build_btn1, self.build_btn2):
            csv_layout.addWidget(widget)

        self.main_layout.addLayout(csv_layout)
        self.add_hline(self.widget, self.main_layout)
        title_label = QLabel("已生成的案例列表：")
        self.output = QTextBrowser(self.widget)
        self.output.setFixedHeight(100)
        for widget in (title_label, self.output):
            self.main_layout.addWidget(widget)

        main_window.setWindowTitle("案例转换工具")
        main_window.setCentralWidget(self.widget)
        self.statusbar = QStatusBar(main_window)
        main_window.setStatusBar(self.statusbar)

    def set_title(self):
        title_label = QLabel("思维导图转换案例工具 v2.1.2")
        title_font = QFont()
        title_font.setFamily("微软雅黑")
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        self.main_layout.addWidget(title_label)

    def add_hline(self, widget, v_layout):
        """layout添加水平线"""
        line = QFrame(widget)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        v_layout.addWidget(line)


def alert_yes(title, text):
    msg_box = QMessageBox()
    msg_box.setWindowTitle(title)
    msg_box.setText(text)
    msg_box.addButton(QPushButton("确定"), QMessageBox.YesRole)
    msg_box.exec()
