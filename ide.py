# IDE source code template used from https://www.geeksforgeeks.org/creating-your-own-python-ide-in-python/

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget
from io import StringIO
import contextlib

class PythonIDE(QMainWindow):
    def __init__(self):
        super(PythonIDE, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Python IDE')
        self.setGeometry(100, 100, 800, 600)

        # Main central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Main vertical layout
        main_layout = QVBoxLayout()

        # Code Editor Section
        self.text_editor_label = QLabel('Code Editor:', self)
        self.text_editor = QTextEdit(self)
        main_layout.addWidget(self.text_editor_label)
        main_layout.addWidget(self.text_editor)

        # Preview Window Section
        self.preview_window_label = QLabel('Preview Window:', self)
        self.preview_window = QTextEdit(self)
        self.preview_window.setReadOnly(True)
        main_layout.addWidget(self.preview_window_label)
        main_layout.addWidget(self.preview_window)

        # Output Section
        self.output_widget_label = QLabel('Output:', self)
        self.output_widget = QTextEdit(self)
        self.output_widget.setReadOnly(True)
        main_layout.addWidget(self.output_widget_label)
        main_layout.addWidget(self.output_widget)

        # Run Button
        self.run_button = QPushButton('Run', self)
        self.run_button.clicked.connect(self.run_code)
        main_layout.addWidget(self.run_button)

        # Set layout to central widget
        central_widget.setLayout(main_layout)

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
