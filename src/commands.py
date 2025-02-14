#command parser based on spoken input
from src.gpt import *
from PyQt5.QtGui import QTextCursor

def handle_prompt(msg, ide):
    print("in prompt handler")
    output = gpt(msg)
    ide.preview_signal.emit(output)

def handle_literal(msg, ide):
    #literal interpretation to type function
    print(f"Literal Text: {msg}", flush=True)
    ide.preview_signal.emit(ide.preview_window.toPlainText() + " " + msg + " ") 

def handle_line(msg, ide):
    suffix = f"only change the line specified leave everything else the same"
    print(output := gpt(msg + suffix))
    ide.preview_signal.emit(output)

def handle_clear_history(msg, ide):
    clear_discourse()

def handle_up(msg, ide):
    print("Moving cursor up")  # Debug print
    ide.preview_window.setFocus()  # Ensure focus is set
    ide.preview_window.move_cursor("up")

def handle_down(msg, ide):
    ide.preview_window.setFocus()  # Ensure focus is set
    ide.preview_window.move_cursor("down")

def handle_left(msg, ide):
    ide.preview_window.setFocus()  # Ensure focus is set
    ide.preview_window.move_cursor("left")

def handle_right(msg, ide):
    ide.preview_window.setFocus()  # Ensure focus is set
    ide.preview_window.move_cursor("right")

def handle_save(msg, ide):
    try:
        content = ide.text_editor.toPlainText()
        with open("txt/ide.txt", "w") as f:
            print(f"Saving content: {content}")  # Verify content to save
            f.write(content)
    except Exception as e:
        print(f"Error saving file: {e}")

def handle_load(msg, ide):
    try:
        with open("txt/ide.txt", "r") as f:
            saved_text = f.read()
            print(f"Loaded text: {saved_text}")  # Verify loaded text
            ide.preview_signal.emit(saved_text)
    except FileNotFoundError:
        print("File not found. Nothing to load.")
    except Exception as e:
        print(f"Error loading file: {e}")

def handle_confirm(msg, ide):
    print("in confirm handler")
    ide.sync_window_signal.emit()

def handle_run(msg, ide):
   ide.run_code_signal.emit() 

def handle_add(msg, ide):
    #should append to previous code block without changing it majorly
    curr_code_block = ide.preview_window.toPlainText()
    msg = f"append new code to this code block to {msg} without major modifications to the original. Previous block: {curr_code_block}"
    output = gpt(msg)
    ide.preview_signal.emit(output)

def handle_revise(msg, ide):
    #designed to fix/edit a broken code block to change functionality
    curr_code_block = ide.preview_window.toPlainText()
    msg = f"Revise this code block to {msg}, modifying the original. Previous block: {curr_code_block}"
    output = gpt(msg)
    ide.preview_signal.emit(output)

def handle_call(msg, ide):
    curr_code_block = ide.preview_window.toPlainText()
    msg = f"Append to this codeblock calls to the created function with testcases for the following input (or inputs): {msg}. Previous block: {curr_code_block}"
    output = gpt(msg)
    ide.preview_signal.emit(output)

#dictionary mapping commands to function handlers
command_handler = {
    "prompt" : handle_prompt,
    "add" : handle_add,
    "call" : handle_call,
    "revise" : handle_revise,
    "literal" : handle_literal,
    "line" : handle_line,
    "run" : handle_run,
    "clear history" : handle_clear_history,
    "up" :  handle_up,
    "down" :  handle_down,
    "right" :  handle_right,
    "left" :  handle_left,
    "save" : handle_save,
    "load" : handle_load,
    "confirm" : handle_confirm,
}

def __main__():
    msg = "determine if a number is prime"
    output = command_handler["prompt"](msg)

if __name__ == "__main__":
    __main__()
