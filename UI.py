import os
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QSpinBox, \
    QFileDialog, QFrame, QSizePolicy, QSpacerItem
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyQt5.QtCore import Qt, QTimer


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.selected_folder_path = None
        self.first_image_name = None
        self.current_operation_type = None
        self.default_output_paths = {
            1: './output/samples',
            2: './dataset/Sea/annotations/validation',
            3: './output/samples',
            4: './HAT-main/results/HAT_SRx4_ImageNet-LR/visualization/custom'
        }

        self.setWindowTitle('海上舰艇的虚拟到真实转换')

        # 设置背景图片
        self.setAutoFillBackground(True)
        self.update_background()

        self.title = QLabel('海上舰艇的虚拟到真实转换')
        self.title.setStyleSheet('font-size: 50px; font-weight: bold; color: white;')
        self.title.setAlignment(Qt.AlignCenter)

        self.label1 = QLabel('请选择操作类型:')
        self.label1.setStyleSheet('font-size: 25px; font-weight: bold; color: white;')
        self.op_type_combo = QComboBox()
        self.op_type_combo.setStyleSheet('font-size: 22px; color: white; background-color: #333;')
        self.op_type_combo.addItems(['选择操作类型', '图像生成', '语义分割', '语义合成', '超分辨率化'])
        self.op_type_combo.currentIndexChanged.connect(self.on_operation_type_change)

        self.layout_op_type = QHBoxLayout()
        self.layout_op_type.addWidget(self.label1)
        self.layout_op_type.addWidget(self.op_type_combo)
        self.layout_op_type.addStretch(1)

        # 左边框架
        self.left_frame = QFrame()
        self.left_frame.setFrameShape(QFrame.Box)
        self.left_frame.setStyleSheet('QFrame {border: 2px solid white; border-radius: 10px;}')
        self.left_frame.setFixedSize(500, 400)

        self.image_count_label = QLabel('图像生成数量:')
        self.image_count_label.setStyleSheet('font-size: 25px; font-weight: bold; color: white;')
        self.image_count_spinbox = QSpinBox()
        self.image_count_spinbox.setStyleSheet('font-size: 22px; color: white; background-color: #333;')
        self.image_count_spinbox.setRange(1, 100)
        self.image_count_spinbox.setFixedWidth(120)

        self.layout_image_count = QHBoxLayout()
        self.layout_image_count.addWidget(self.image_count_label)
        self.layout_image_count.addWidget(self.image_count_spinbox)
        self.layout_image_count.addStretch(1)

        self.select_folder_button = QPushButton('选择文件夹')
        self.select_folder_button.setStyleSheet('font-size: 22px; color: white; background-color: #333;')
        self.select_folder_button.setFixedWidth(160)
        self.select_folder_button.clicked.connect(self.on_select_folder_button_click)
        self.select_folder_button.setDisabled(True)

        self.layout_folder_select = QHBoxLayout()
        self.layout_folder_select.addWidget(self.select_folder_button)

        self.execute_button = QPushButton('生成图像')
        self.execute_button.setStyleSheet('font-size: 40px; font-weight: bold; color: white; background-color: #444;')
        self.execute_button.clicked.connect(self.generate_button_click)
        self.execute_button.setDisabled(True)
        self.execute_button.setFixedSize(300, 50)

        self.layout_execute = QHBoxLayout()
        self.layout_execute.addWidget(self.execute_button)

        self.left_layout = QVBoxLayout()
        self.left_layout.addLayout(self.layout_image_count)
        self.left_layout.addLayout(self.layout_folder_select)
        self.left_layout.addStretch(1)
        self.left_layout.addLayout(self.layout_execute)
        self.left_layout.addStretch(1)

        self.left_frame.setLayout(self.left_layout)

        # 右边图片显示框架
        self.input_image_label = QLabel('输入图像')
        self.input_image_label.setStyleSheet('font-size: 25px; font-weight: bold; color: white;')
        self.input_image_label.setAlignment(Qt.AlignCenter)

        self.image_display_label_input = QLabel()
        self.image_display_label_input.setAlignment(Qt.AlignCenter)
        self.image_display_label_input.setFixedSize(200, 200)
        self.image_display_label_input.setStyleSheet('border: 2px solid white;')

        self.output_image_label = QLabel('输出图像')
        self.output_image_label.setStyleSheet('font-size: 25px; font-weight: bold; color: white;')
        self.output_image_label.setAlignment(Qt.AlignCenter)

        self.image_display_label_output = QLabel()
        self.image_display_label_output.setAlignment(Qt.AlignCenter)
        self.image_display_label_output.setFixedSize(200, 200)
        self.image_display_label_output.setStyleSheet('border: 2px solid white;')

        self.right_frame = QFrame()
        self.right_frame.setFrameShape(QFrame.Box)
        self.right_frame.setStyleSheet('QFrame {border: 2px solid white; border-radius: 10px;}')
        self.right_frame.setFixedSize(500, 400)

        # Create a horizontal layout for the images
        self.image_layout = QHBoxLayout()
        self.image_layout.addWidget(self.image_display_label_input)
        self.image_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum))  # 增加间隔
        self.image_layout.addWidget(self.image_display_label_output)
        self.image_layout.addStretch(1)

        # Create a vertical layout for the input image
        self.input_layout = QVBoxLayout()
        self.input_layout.addWidget(self.input_image_label)
        self.input_layout.addWidget(self.image_display_label_input)
        self.input_layout.addStretch(1)

        # Create a vertical layout for the output image
        self.output_layout = QVBoxLayout()
        self.output_layout.addWidget(self.output_image_label)
        self.output_layout.addWidget(self.image_display_label_output)
        self.output_layout.addStretch(1)

        # Create a horizontal layout for input and output layouts
        self.image_layout = QHBoxLayout()
        self.image_layout.addLayout(self.input_layout)
        self.image_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum))  # 增加间隔
        self.image_layout.addLayout(self.output_layout)
        self.image_layout.addStretch(1)

        # Create a vertical layout for centering
        self.right_layout = QVBoxLayout()
        self.right_layout.addStretch(1)
        self.right_layout.addLayout(self.image_layout)
        self.right_layout.addStretch(1)

        self.right_frame.setLayout(self.right_layout)

        self.layout = QHBoxLayout()
        self.layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum))
        self.layout.addWidget(self.left_frame)
        self.layout.addStretch(1)
        self.layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum))
        self.layout.addWidget(self.right_frame)
        self.layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum))

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.title)
        self.main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed))
        self.main_layout.addLayout(self.layout_op_type)
        self.main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))
        self.main_layout.addLayout(self.layout)

        self.setLayout(self.main_layout)

        # 手动更新背景图片
        self.update_background()

        # 清空默认输出路径中的文件
        self.clear_default_output_paths()

        # 设置定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_output_image)
        self.timer.start(1000)  # 每秒更新一次

    def clear_default_output_paths(self):
        for path in self.default_output_paths.values():
            if os.path.exists(path):
                for file_name in os.listdir(path):
                    file_path = os.path.join(path, file_name)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            os.rmdir(file_path)
                    except Exception as e:
                        print(f'Failed to delete {file_path}. Reason: {e}')

    def resizeEvent(self, event):
        self.update_background()
        super().resizeEvent(event)

    def update_background(self):
        palette = self.palette()
        background_image = QPixmap('Background/ship1.jpg')
        palette.setBrush(QPalette.Window,
                         QBrush(background_image.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
        self.setPalette(palette)

    def on_operation_type_change(self, index):
        self.image_display_label_output.clear()  # 重置输出图片显示
        self.first_image_name = None  # 重置输入图像名称
        self.current_operation_type = index

        if index == 0:
            self.select_folder_button.setDisabled(True)
            self.execute_button.setDisabled(True)
            self.image_display_label_input.clear()
        else:
            self.select_folder_button.setDisabled(False)
            self.execute_button.setDisabled(False)
            self.execute_button.setText(self.op_type_combo.currentText())
            self.show_default_output_image(index)

    def on_select_folder_button_click(self):
        folder_path = QFileDialog.getExistingDirectory(self, '选择文件夹')
        if folder_path:
            self.selected_folder_path = folder_path
            self.show_first_image(folder_path, self.image_display_label_input)
            self.show_default_output_image(self.op_type_combo.currentIndex())

    def show_first_image(self, folder_path, display_label):
        for file_name in os.listdir(folder_path):
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                self.first_image_name = os.path.splitext(file_name)[0]  # 仅获取文件名，不包括后缀
                image_path = os.path.join(folder_path, file_name)
                pixmap = QPixmap(image_path)
                display_label.setPixmap(pixmap.scaled(display_label.size(), Qt.KeepAspectRatio))
                break

    def show_default_output_image(self, operation_type):
        self.current_operation_type = operation_type
        default_output_path = self.default_output_paths.get(operation_type)
        if default_output_path and os.path.exists(default_output_path):
            self.show_matching_image(default_output_path, self.image_display_label_output)
        else:
            self.image_display_label_output.setText("No default output image")

    def show_matching_image(self, folder_path, display_label):
        if self.selected_folder_path and self.first_image_name:
            for file_name in os.listdir(folder_path):
                if self.first_image_name in os.path.splitext(file_name)[0]:  # 比较时放宽条件，包含即可
                    matching_image_path = os.path.join(folder_path, file_name)
                    if os.path.exists(matching_image_path):
                        pixmap = QPixmap(matching_image_path)
                        display_label.setPixmap(pixmap.scaled(display_label.size(), Qt.KeepAspectRatio))
                    else:
                        display_label.clear()
                    break

    def update_output_image(self):
        if self.selected_folder_path and self.current_operation_type:
            default_output_path = self.default_output_paths.get(self.current_operation_type)
            if default_output_path:
                self.show_matching_image(default_output_path, self.image_display_label_output)

    def generate_button_click(self):
        if self.selected_folder_path:
            current_index = self.op_type_combo.currentIndex()
            script_path = ''
            if current_index == 1:
                script_path = 'main.py'
                image_count = self.image_count_spinbox.value()
                subprocess.run(
                    ['python', script_path, '--virtual_image_path', self.selected_folder_path, '--num_samples',
                     str(image_count)])
            elif current_index == 2:
                script_path = 'SAM/predict.py'
                subprocess.run(['python', script_path, '--img_path', self.selected_folder_path])
            elif current_index == 3:
                num_samples = self.image_count_spinbox.value()
                script_path = 'SDM/image_sample.py'
                subprocess.run(['python', script_path, '--data_dir', self.selected_folder_path, '--dataset_mode',
                                'seas', '--attention_resolution', '32,16,8', '--diffusion_steps', '1000',
                                '--image_size', '256', '--learn_sigma', 'True', '--noise_schedule', 'linear',
                                '--num_channels', '256', '--num_head_channels', '64', '--num_res_blocks', '2',
                                '--resblock_updown', 'True', '--use_fp16', 'True', '--use_scale_shift_norm', 'True',
                                '--num_classes', '5', '--class_cond', 'True', '--no_instance', 'True', '--batch_size',
                                '1',
                                '--num_samples', str(num_samples - 1), '--model_path',
                                './SDM/OUTPUT/save/seas_256-300000-l1.pt',
                                '--results_path', './output', '--s', '1.5', ])
            elif current_index == 4:
                script_path = './HAT-main/hat/test.py'
                # Replace the path in the YAML file
                self.replace_yaml_path('./HAT-main/options/test/HAT_SRx4_ImageNet-LR.yml', self.selected_folder_path)
                subprocess.run(['python', script_path, '-opt', './HAT-main/options/test/HAT_SRx4_ImageNet-LR.yml'])

            self.show_default_output_image(current_index)  # 更新输出图像显示

    def replace_yaml_path(self, yaml_file, new_path):
        import yaml
        with open(yaml_file, 'r') as file:
            config = yaml.safe_load(file)

        # Replace the dataroot_lq path
        config['datasets']['test_1']['dataroot_lq'] = new_path

        with open(yaml_file, 'w') as file:
            yaml.safe_dump(config, file)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
