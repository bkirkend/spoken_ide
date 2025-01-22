# IDE source code template used from https://www.geeksforgeeks.org/creating-your-own-python-ide-in-python/

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget
from io import StringIO
import contextlib

class PythonIDE(QMainWindow):
    def __init__(self):
        super(PythonIDE, self).__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Python IDE')

        self.text_editor = QTextEdit(self)
        self.text_editor.setGeometry(10, 10, 780, 300)

        self.output_widget = QTextEdit(self)
        self.output_widget.setGeometry(10, 320, 780, 200)

        self.run_button = QPushButton('Run', self)
        self.run_button.setGeometry(10, 530, 780, 30)
        self.run_button.clicked.connect(self.run_code)

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
