'''
Original source: https://www.geeksforgeeks.org/creating-your-own-python-ide-in-python/?ref=ml_lbp
Some modifications made with assistance from ChatGPT
'''

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QSizePolicy, QPlainTextEdit
from PyQt5.QtCore import pyqtSignal, Qt, QRect, QTimer
from PyQt5.QtGui import QPainter, QTextFormat, QTextCursor, QPen
from io import StringIO
import contextlib


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return self.editor.line_number_area_size()

    def paintEvent(self, event):
        self.editor.line_number_area_paint(event)


class CodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.line_number_area = LineNumberArea(self)

        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)

        self.update_line_number_area_width()

    def keyPressEvent(self, event):
        pass

    def line_number_area_width(self):
        digits = len(str(max(1, self.blockCount())))
        return 10 + self.fontMetrics().horizontalAdvance('9') * digits

    def line_number_area_size(self):
        return self.line_number_area_width(), 0

    def update_line_number_area_width(self):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    def line_number_area_paint(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), Qt.lightGray)

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.drawText(0, int(top), self.line_number_area.width() - 5, int(self.fontMetrics().height()),
                                 Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1


class PreviewWindow(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.line_number_area = LineNumberArea(self)

        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)

        self.update_line_number_area_width()
        self.cursor_timer = QTimer(self)
        self.cursor_timer.timeout.connect(self.blink_cursor)
        self.cursor_visible = True
        self.cursor_timer.start(500)  

        self.setCursorWidth(2)  
        self.setFocusPolicy(Qt.StrongFocus)  
        self.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.cursor_position = self.textCursor()  

    def keyPressEvent(self, event):
        pass

    def move_cursor(self, direction):
        cursor = self.textCursor()  
        print(f"Current cursor position: {cursor.position()}")  # Debug print

        if direction == "up":
            cursor.movePosition(QTextCursor.Up, QTextCursor.MoveAnchor) 
        elif direction == "down":
            cursor.movePosition(QTextCursor.Down, QTextCursor.MoveAnchor)  
        elif direction == "left":
            cursor.movePosition(QTextCursor.StartOfBlock, QTextCursor.KeepAnchor)  
        elif direction == "right":
            cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor) 

        print(f"New cursor position: {cursor.position()}")  

        if not cursor.isNull():
            self.setTextCursor(cursor)
            self.ensureCursorVisible()  # Ensure the cursor is visible
            self.setFocus()  # Ensure the widget has focus
            self.viewport().update()  # Force a repaint

        print(f"new position: {cursor.blockNumber()} (line {cursor.positionInBlock()})")
    def update_cursor_position(self, position=None): 
        if position is None:
            self.cursor_position.movePosition(QTextCursor.End)
        else:
            self.cursor_position.setPosition(position)
        
        self.setTextCursor(self.cursor_position)  
        self.ensureCursorVisible()  
        self.viewport().update()  

    def blink_cursor(self): 
        self.cursor_visible = not self.cursor_visible
        self.viewport().update()

    def paintEvent(self, event):
        super().paintEvent(event)  
        if self.cursor_visible:
            painter = QPainter(self.viewport())
            pen = QPen(Qt.black, 2)  
            painter.setPen(pen)

            # Get the cursor rectangle
            rect = self.cursorRect(self.textCursor())
            painter.drawLine(rect.left(), rect.top(), rect.left(), rect.bottom())

    def setPlainText(self, text):
        super().setPlainText(text)
        self.update_cursor_position()

    def line_number_area_width(self):
        digits = len(str(max(1, self.blockCount())))
        return 10 + self.fontMetrics().horizontalAdvance('9') * digits

    def line_number_area_size(self):
        return self.line_number_area_width(), 0

    def update_line_number_area_width(self):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    def line_number_area_paint(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), Qt.lightGray)

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.drawText(0, int(top), self.line_number_area.width() - 5, int(self.fontMetrics().height()),
                                 Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1


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

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()

        top_layout = QHBoxLayout()

        # Code Editor with Line Numbers
        self.text_editor_label = QLabel('Code Editor:', self)
        self.text_editor = CodeEditor(self)
        self.text_editor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.text_editor.setReadOnly(False)
        editor_layout = QVBoxLayout()
        editor_layout.addWidget(self.text_editor_label)
        editor_layout.addWidget(self.text_editor)
        top_layout.addLayout(editor_layout, 3)

        # Preview Window with Line Numbers
        self.preview_window_label = QLabel('Preview Window:', self)
        self.preview_window = PreviewWindow(self)
        self.preview_window.setReadOnly(False)
        self.preview_window.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        preview_layout = QVBoxLayout()
        preview_layout.addWidget(self.preview_window_label)
        preview_layout.addWidget(self.preview_window)
        top_layout.addLayout(preview_layout, 3)

        main_layout.addLayout(top_layout, 5)

        bottom_layout = QVBoxLayout()
        self.output_widget_label = QLabel('Output:', self)
        self.output_widget = QTextEdit(self)
        self.output_widget.setReadOnly(True)
        self.output_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.output_widget.setMinimumHeight(100)
        bottom_layout.addWidget(self.output_widget_label)
        bottom_layout.addWidget(self.output_widget)

        main_layout.addLayout(bottom_layout, 1)

        central_widget.setLayout(main_layout)

    def update_preview(self, text=None):
        if text is None:
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
                exec(code, sys.modules)
            except Exception as e:
                print(e)

        output = output_stream.getvalue()
        self.output_widget.setPlainText(output)


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ide = PythonIDE()
#     ide.show()
#     sys.exit(app.exec_())
