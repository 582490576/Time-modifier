import os
import sys
from PyQt6 import QtWidgets
from date import UiForm  # 确保这个导入路径与你的文件结构相匹配
from PyQt6.QtWidgets import QMessageBox, QFileDialog
from PyQt6.QtCore import QFileInfo
from datetime import datetime
import win32file
import win32con


class MyApp(QtWidgets.QWidget, UiForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.file_path = None
        self.setFixedSize(500, 450)


    def file_data(self):
        self.file_path = self.lineEdit.text()
        if not os.path.isfile(self.file_path):
            QMessageBox.warning(self, "文件不存在", "请选择一个存在的文件。")
            self.file_path = None
        else:
            file_info = QFileInfo(self.file_path)
            creation_time = file_info.birthTime().toString()
            modification_time = file_info.lastModified().toString()
            creation_time = datetime.strptime(creation_time, '%a %b %d %H:%M:%S %Y').strftime('%Y-%m-%d %H:%M:%S')
            modification_time = datetime.strptime(modification_time, '%a %b %d %H:%M:%S %Y').strftime(
                '%Y-%m-%d %H:%M:%S')
            self.label_5.setText(creation_time)
            self.label_6.setText(modification_time)

    def change(self):
        if self.file_path:
            creation_time = self.dateTimeEdit.dateTime().toSecsSinceEpoch()
            modification_time = self.dateTimeEdit_2.dateTime().toSecsSinceEpoch()

            try:
                # 获取文件句柄
                handle = win32file.CreateFile(
                    self.file_path,
                    win32con.GENERIC_WRITE,
                    0,  # 不共享
                    None,  # 默认安全设置
                    win32con.OPEN_EXISTING,
                    0,  # 非重叠（同步）
                    None
                )

                # 将时间转换为datetime对象
                creation_datetime = datetime.fromtimestamp(creation_time)
                modification_datetime = datetime.fromtimestamp(modification_time)

                # 设置文件时间
                win32file.SetFileTime(handle, creation_datetime, None, modification_datetime)

                # 关闭句柄
                win32file.CloseHandle(handle)
                # 显示成功消息
                QMessageBox.information(self, "成功", "文件时间已成功修改。")
            except Exception as e:
                # 显示错误消息
                QMessageBox.critical(self, "错误", f"修改文件时间失败：{e}")
        else:
            QMessageBox.critical(self, "错误", "请先获取文件信息。")

    def select_file(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                None,  # 不传递父窗口
                "选择文件",
                "/",
                "所有文件 (*.*);;文本文件 (*.txt);;PDF文件 (*.pdf)"
            )
            if file_path:
                self.lineEdit.setText(file_path)
        except Exception as e:
            QMessageBox.critical(self, "错误", "获取失败")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myApp = MyApp()
    myApp.show()
    sys.exit(app.exec())
