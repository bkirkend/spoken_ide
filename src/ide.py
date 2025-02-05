#adopted from geeksforgeeks and modified through chatgpt to create gui window

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QSizePolicy
from PyQt5.QtCore import pyqtSignal, QObject
from io import StringIO
import contextlib

class PythonIDE(QMainWindow):
    preview_signal = pyqtSignal(str)
    code_editor_signal = pyqtSignal(str)
    sync_window_signal = pyqtSignal()
    run_code_signal = pyqtSignal()

    def __init__(self):
        super(PythonIDE, self).__init__()
        self.initUI()
        self.preview_signal.connect(self.update_preview)
        self.code_editor_signal.connect(self.update_code_editor)
        self.sync_window_signal.connect(self.sync_editor)
        self.run_code_signal.connect(self.run_code)

    def initUI(self):
        self.setWindowTitle('Python IDE')
        self.setGeometry(100, 100, 800, 600)

        # Main central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Main vertical layout (Overall structure)
        main_layout = QVBoxLayout()

        # Top Layout for Code Editor & Preview Window
        top_layout = QHBoxLayout()

        # Code Editor Section
        self.text_editor_label = QLabel('Code Editor:', self)
        self.text_editor = QTextEdit(self)
        self.text_editor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Allow expansion
        editor_layout = QVBoxLayout()
        editor_layout.addWidget(self.text_editor_label)
        editor_layout.addWidget(self.text_editor)
        top_layout.addLayout(editor_layout, 3)  # Assign more space (Stretch Factor: 3)

        # Preview Window Section
        self.preview_window_label = QLabel('Preview Window:', self)
        self.preview_window = QTextEdit(self)
        self.preview_window.setReadOnly(True)
        self.preview_window.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        preview_layout = QVBoxLayout()
        preview_layout.addWidget(self.preview_window_label)
        preview_layout.addWidget(self.preview_window)
        top_layout.addLayout(preview_layout, 3)  # Assign more space (Stretch Factor: 3)

        # Add the top layout (Code Editor & Preview) to the main layout
        main_layout.addLayout(top_layout, 5)  # More space for code & preview (Stretch Factor: 5)

        # Bottom Layout for Output Window & Run Button
        bottom_layout = QVBoxLayout()
        self.output_widget_label = QLabel('Output:', self)
        self.output_widget = QTextEdit(self)
        self.output_widget.setReadOnly(True)
        self.output_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)  # Limit height
        self.output_widget.setMinimumHeight(100)  # 🔹 Restrict output size
        bottom_layout.addWidget(self.output_widget_label)
        bottom_layout.addWidget(self.output_widget)

        # Run Button
        self.run_button = QPushButton('Run', self)
        self.run_button.clicked.connect(self.run_code)
        bottom_layout.addWidget(self.run_button)

        # Add bottom layout (Output & Run) to main layout
        main_layout.addLayout(bottom_layout, 1)  # 🔹 Less space for Output (Stretch Factor: 1)

        # Set the main vertical layout to the central widget
        central_widget.setLayout(main_layout)

    def update_preview(self, text=None):
        if text is None:  # If no argument is passed, use the text from the editor
            text = self.text_editor.toPlainText()
        self.preview_window.setPlainText(text)

    def update_code_editor(self, text=None):
        if text is None:
            text = self.text_editor.toPlainText()
        self.text_editor.setPlainText(text)

    def sync_editor(self):
        text = self.preview_window.toPlainText()
        self.text_editor.setPlainText(text)

    def run_code(self):
        code = self.text_editor.toPlainText()
        output_stream = StringIO()
        
        with contextlib.redirect_stdout(output_stream):
            try:
                exec(code)
            except Exception as e:
                print(e)

        output = output_stream.getvalue()
        self.output_widget.setPlainText(output)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ide = PythonIDE()
    ide.show()
    sys.exit(app.exec_())
