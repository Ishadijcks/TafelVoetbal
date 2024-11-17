from typing import Callable

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QSlider


class SliderInputWindow(QMainWindow):
    GRANULARITY = 256

    def __init__(self, initial_translation, on_translation: Callable, initial_rotation, on_rotation: Callable):
        super().__init__()
        self.on_translation = on_translation
        self.on_rotation = on_rotation

        self.setWindowTitle("Tafelvoetbal")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.button = QPushButton("Calibrate!")
        self.button.clicked.connect(self.on_button_click)
        layout.addWidget(self.button)

        self.translate_slider = QSlider(Qt.Horizontal)
        self.translate_slider.setMinimum(0)
        self.translate_slider.setMaximum(self.GRANULARITY)
        self.translate_slider.setTracking(True)
        self.translate_slider.setValue(int(initial_rotation * self.GRANULARITY))
        self.translate_slider.valueChanged.connect(self.on_translation_changed)
        layout.addWidget(self.translate_slider)

        self.rotate_slider = QSlider(Qt.Horizontal)
        self.rotate_slider.setMinimum(0)
        self.rotate_slider.setMaximum(self.GRANULARITY)
        self.rotate_slider.setTracking(True)
        self.rotate_slider.setValue(int(initial_translation * self.GRANULARITY))
        self.rotate_slider.valueChanged.connect(self.on_rotation_changed)
        layout.addWidget(self.rotate_slider)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def on_button_click(self):
        print("TODO implement calibrate!")

    def on_translation_changed(self, x: float):
        self.on_translation(x / self.GRANULARITY)

    def on_rotation_changed(self, x: float):
        self.on_rotation(x / self.GRANULARITY)
