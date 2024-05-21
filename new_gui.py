import subprocess
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QCheckBox, QHBoxLayout, QVBoxLayout, QFileDialog, \
    QRadioButton, QPushButton, QSpinBox
from PyQt5.QtGui import QPixmap, QPalette, QColor, QBrush, QPainter


class MyPyQtApp(QWidget):
    def __init__(self):
        super().__init__()
        self.flag = None
        self.initUI()

    def initUI(self):
        # 第一行：请选择生成模式
        self.label1 = QLabel('  请选择生成模式：')
        self.label1.setStyleSheet('font-size: 25px; font-weight: bold;color:white')

        # 创建两个复选框：单图输入和批量输入
        self.single_checkbox = QCheckBox('单图输入')
        self.batch_checkbox = QCheckBox('批量输入')

        # 设置复选框的样式
        self.single_checkbox.setStyleSheet('font-size: 25px;color:white')
        self.batch_checkbox.setStyleSheet('font-size: 25px;color:white')

        # 创建一个水平布局，并将文本标签和复选框布局添加到布局中
        self.layout1 = QHBoxLayout()
        self.layout1.addWidget(self.label1)
        self.layout1.addWidget(self.single_checkbox)
        self.layout1.addWidget(self.batch_checkbox)

        # 设置复选框的点击事件处理函数
        self.single_checkbox.clicked.connect(self.on_single_checkbox_click)
        self.batch_checkbox.clicked.connect(self.on_batch_checkbox_click)

        # 第二行：请选择输入图片（单图模式）
        self.label2 = QLabel('  请选择输入图片(单图模式):')
        self.label2.setStyleSheet('font-size: 25px; font-weight: bold;color: white')

        # 创建选择图片按钮
        self.select_image_button = QPushButton('选择图片')
        self.select_image_button.setStyleSheet('font-size: 22px; ')
        self.select_image_button.setFixedWidth(186)
        self.select_image_button.clicked.connect(self.on_select_image_button_click)

        # 创建一个水平布局，并将文本标签和按钮布局添加到布局中
        self.layout2 = QHBoxLayout()
        self.layout2.addWidget(self.label2)
        self.layout2.addWidget(self.select_image_button)
        self.layout2.addStretch(1)

        # 第三行：请选择图片文件夹（批量生成模式）
        self.label3 = QLabel('  请选择图片文件夹(批量模式):')
        self.label3.setStyleSheet('font-size: 25px; font-weight: bold;color:white')

        # 创建选择文件夹按钮
        self.select_folder_button = QPushButton('选择文件夹')
        self.select_folder_button.setStyleSheet('font-size: 22px;')
        self.select_folder_button.setFixedWidth(160)
        self.select_folder_button.clicked.connect(self.on_select_folder_button_click)

        # 创建一个水平布局，并将文本标签和按钮布局添加到布局中
        self.layout3 = QHBoxLayout()
        self.layout3.addWidget(self.label3)
        self.layout3.addWidget(self.select_folder_button)
        self.layout3.addStretch(1)

        # 第四行：请选择生成路径
        self.label4 = QLabel('  请选择生成路径：')
        self.label4.setStyleSheet('font-size: 25px; font-weight: bold;color:white')

        # 创建两个单选按钮：在原路径和指定路径
        self.original_path_radio = QRadioButton('在原路径')
        self.specified_path_radio = QRadioButton('生成在指定路径')

        # 设置单选按钮的样式
        self.original_path_radio.setStyleSheet('font-size: 22px;color:white')
        self.specified_path_radio.setStyleSheet('font-size: 22px;color:white')

        # 创建一个水平布局，并将文本标签和单选按钮布局添加到布局中
        self.layout4 = QHBoxLayout()
        self.layout4.addWidget(self.label4)
        self.layout4.addWidget(self.original_path_radio)
        self.layout4.addWidget(self.specified_path_radio)
        self.layout4.addStretch(1)

        # 设置单选按钮的点击事件处理函数
        self.original_path_radio.clicked.connect(self.on_original_path_radio_click)
        self.specified_path_radio.clicked.connect(self.on_specified_path_radio_click)

        # 第五行：请选择指定路径
        self.label5 = QLabel('  请选择指定路径：')
        self.label5.setStyleSheet('font-size: 25px; font-weight: bold;color:white')

        # 创建选择文件夹按钮（用于指定路径）
        self.select_specified_folder_button = QPushButton('选择文件夹')
        self.select_specified_folder_button.setStyleSheet('font-size: 22px;')
        self.select_specified_folder_button.setFixedWidth(305)
        self.select_specified_folder_button.clicked.connect(self.on_select_specified_folder_button_click)
        self.select_specified_folder_button.setDisabled(True)

        # 创建一个水平布局，并将文本标签和按钮布局添加到布局中
        self.layout5 = QHBoxLayout()
        self.layout5.addWidget(self.label5)
        self.layout5.addWidget(self.select_specified_folder_button)
        self.layout5.addStretch(1)

        # 第六行：真实图片生成数量
        self.label6 = QLabel('  真实图片生成数量：')
        self.label6.setStyleSheet('font-size: 25px; font-weight: bold;color:white')

        # 创建一个滚轮选择器（QSpinBox）
        self.image_count_spinbox = QSpinBox()
        self.image_count_spinbox.setStyleSheet('font-size: 22px; font-weight: bold;font-family:Tahoma ')
        self.image_count_spinbox.setMinimum(1)
        self.image_count_spinbox.setMaximum(20)
        self.image_count_spinbox.setValue(5)  # 设置默认值为5
        self.image_count_spinbox.setFixedWidth(290)

        # 创建一个水平布局，并将文本标签和滚轮布局添加到布局中
        self.layout6 = QHBoxLayout()
        self.layout6.addWidget(self.label6)
        self.layout6.addWidget(self.image_count_spinbox)
        self.layout6.addStretch(1)

        # 第七行：执行按钮
        self.execute_button = QPushButton('开始生成')
        self.execute_button.setStyleSheet('font-size: 40px; font-weight: bold;')
        self.execute_button.clicked.connect(self.on_execute_button_click)
        self.execute_button.setDisabled(True)

        # 创建一个水平布局，并将按钮布局添加到布局中
        self.layout7 = QHBoxLayout()
        self.layout7.addWidget(self.execute_button)

        # 创建一个垂直布局，并将所有水平布局添加到布局中
        self.main_layout = QVBoxLayout()
        self.main_layout.addStretch(1)  # Add a stretch factor for empty space at the top
        # self.main_layout.addStretch(1)
        # self.main_layout.addStretch(1)
        # self.main_layout.addStretch(1)
        self.main_layout.addStretch(1)
        self.main_layout.addStretch(1)
        self.main_layout.addStretch(1)
        self.main_layout.addStretch(1)
        self.main_layout.addLayout(self.layout1)
        self.main_layout.addStretch(1)
        self.main_layout.addLayout(self.layout2)
        self.main_layout.addStretch(1)
        self.main_layout.addLayout(self.layout3)
        self.main_layout.addStretch(1)
        self.main_layout.addLayout(self.layout4)
        self.main_layout.addStretch(1)
        self.main_layout.addLayout(self.layout5)
        self.main_layout.addStretch(1)
        self.main_layout.addStretch(1)
        self.main_layout.addLayout(self.layout6)
        self.main_layout.addStretch(1)
        self.main_layout.addLayout(self.layout7)
        self.main_layout.addStretch(1)  # 底部伸缩因子，添加空白空间

        # 设置窗口的主布局
        self.setLayout(self.main_layout)

        # 设置窗口的标题和初始大小
        self.setWindowTitle('VTR')

        # 设置窗口背景图片
        background_image = QPixmap('background(2).jpg')
        self.setFixedSize(background_image.width(), background_image.height())
        palette = self.palette()
        brush = QBrush(background_image.scaled(self.size()))
        palette.setBrush(QPalette.Background, brush)
        self.setPalette(palette)

    def on_single_checkbox_click(self):
        # 单图输入复选框点击事件处理
        self.batch_checkbox.setChecked(not self.single_checkbox.isChecked())
        self.select_folder_button.setDisabled(self.single_checkbox.isChecked())
        self.select_image_button.setDisabled(not self.single_checkbox.isChecked())
        self.update_execute_button()

    def on_batch_checkbox_click(self):
        # 批量输入复选框点击事件处理函数
        self.single_checkbox.setChecked(not self.batch_checkbox.isChecked())
        self.select_image_button.setDisabled(self.batch_checkbox.isChecked())
        self.select_folder_button.setDisabled(not self.batch_checkbox.isChecked())
        self.update_execute_button()

    def on_original_path_radio_click(self):
        # 在原路径单选按钮点击事件处理函数
        self.specified_path_radio.setChecked(not self.original_path_radio.isChecked())
        self.select_specified_folder_button.setDisabled(self.original_path_radio.isChecked())
        self.update_execute_button()

    def on_specified_path_radio_click(self):
        # 生成在指定路径单选按钮点击事件处理函数
        self.original_path_radio.setChecked(not self.specified_path_radio.isChecked())
        self.select_specified_folder_button.setDisabled(not self.specified_path_radio.isChecked())
        self.update_execute_button()

    def on_select_image_button_click(self):
        # 选择图片按钮点击事件处理函数
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "选择图片", "", "Images (*.png *.jpg *.bmp);;All Files (*)",
                                                   options=options)
        if file_name:
            print(f"选择的图片文件：{file_name}")
            self.update_execute_button()

    def on_select_folder_button_click(self):
        # 选择文件夹按钮点击事件处理函数
        options = QFileDialog.Options()
        folder_name = QFileDialog.getExistingDirectory(self, "选择文件夹", options=options)
        if folder_name:
            print(f"选择的文件夹：{folder_name}")
            self.update_execute_button()

    def on_select_specified_folder_button_click(self):
        # 选择指定路径文件夹按钮点击事件处理函数
        options = QFileDialog.Options()
        folder_name = QFileDialog.getExistingDirectory(self, "选择文件夹", options=options)
        if folder_name:
            print(f"选择的指定路径文件夹：{folder_name}")
            self.flag = True
            self.update_execute_button()

    def update_execute_button(self):
        # 更新执行按钮状态
        if self.single_checkbox.isChecked() and not self.select_image_button.isEnabled():
            self.execute_button.setEnabled(True)
        elif self.batch_checkbox.isChecked() and not self.select_folder_button.isEnabled():
            self.execute_button.setEnabled(True)
        elif self.original_path_radio.isChecked() and not self.select_specified_folder_button.isEnabled():
            self.execute_button.setEnabled(True)
        elif self.specified_path_radio.isChecked() and self.flag:
            self.execute_button.setEnabled(True)
        else:
            self.execute_button.setDisabled(True)

    def on_execute_button_click(self):
        # 开始生成按钮点击事件处理函数
        print("开始生成图片！")
        try:
            subprocess.run(["python", "main.py"], check=True, cwd=".")
        except subprocess.CalledProcessError as e:
            print(f"运行main.py时发生错误：{e}")


if __name__ == '__main__':
    # 在创建应用程序对象之前设置全局字体样式表
    font_style = "font-size: 32px; font-weight: bold;"
    app = QApplication(sys.argv)
    app.setStyleSheet(f"* {{ {font_style} }}")

    # 创建一个PyQt5窗口对象
    window = MyPyQtApp()

    # 显示窗口
    window.show()

    # 运行应用程序的主循环
    sys.exit(app.exec_())