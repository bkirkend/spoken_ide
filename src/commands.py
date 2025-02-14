#command parser based on spoken input
from src.gpt import *
from PyQt5.QtGui import QTextCursor
import os

def handle_prompt(msg, ide):
    gpt_msg = f"Create a function for {msg}, return only the function and no auxiliary calls or tescases"
    output = gpt(gpt_msg)
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
    print("Moving cursor up") 
    ide.preview_window.setFocus()  
    ide.preview_window.move_cursor("up")

def handle_down(msg, ide):
    ide.preview_window.setFocus() 
    ide.preview_window.move_cursor("down")

def handle_left(msg, ide):
    ide.preview_window.setFocus() 
    ide.preview_window.move_cursor("left")

def handle_right(msg, ide):
    ide.preview_window.setFocus() 
    ide.preview_window.move_cursor("up")

def handle_down(msg, ide):
    ide.preview_window.setFocus()
    ide.preview_window.move_cursor("down")

def handle_left(msg, ide):
    ide.preview_window.setFocus()
    ide.preview_window.move_cursor("left")

def handle_right(msg, ide):
    ide.preview_window.setFocus()
    ide.preview_window.move_cursor("right")

def select_left(msg, ide):
    ide.preview_window.setFocus()
    ide.preview_window.select_left()

def select_right(msg, ide):
    ide.preview_window.setFocus()
    ide.preview_window.select_right()

def handle_save(msg, ide):
    try:
        os.makedirs("txt", exist_ok=True)
        
        content = ide.text_editor.toPlainText()
        file_path = "txt/ide.txt"
        
        with open(file_path, "w") as f:
            print(f"Saving content: {content}")
            f.write(content)
    
    except Exception as e:
        print(f"Error saving file: {e}")

def handle_load(msg, ide):
    try:
        with open("txt/ide.txt", "r") as f:
            saved_text = f.read()
            print(f"Loaded text: {saved_text}") 
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

def handle_test(msg, ide):
    curr_code_block = ide.preview_window.toPlainText()
    msg = f"Append to this codeblock calls to the created function with a testcase in a print call for the following string input: {msg}. Do not place this in a __main__ block. Append a new test do not override existing testcases. Previous block: {curr_code_block}"
    output = gpt(msg)
    ide.preview_signal.emit(output)


#dictionary mapping commands to function handlers
command_handler = {
    "prompt" : handle_prompt,
    "add" : handle_add,
    "test" : handle_test,
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
    "submit" : handle_confirm,
    "left select" : select_left,
    "right select" : select_right, 
}

# def __main__():
#     msg = "determine if a number is prime"
#     output = command_handler["prompt"](msg)
#
# if __name__ == "__main__":
#     __main__()

