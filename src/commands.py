#command parser based on spoken input

from gpt import *

def handle_prompt(msg, ide):
    print("in prompt handler")
    output = gpt(msg)
    ide.preview_signal.emit(output)

def handle_literal(msg, ide):
    #literal interpretation to type function
    pass

def handle_line(msg, ide):
    suffix = f"only change the line specified leave everything else the same"
    print(output := gpt(msg + suffix))
    ide.preview_signal.emit(output)

def handle_clear_history(msg, ide):
    clear_discourse()

def handle_up(msg, ide):
    pass

def handle_down(msg, ide):
    pass

def handle_left(msg, ide):
    pass

def handle_right(msg, ide):
    pass

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

#dictionary mapping commands to function handlers
command_handler = {
    "prompt" : handle_prompt,
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
    "run" : handle_run
}

def __main__():
    msg = "determine if a number is prime"
    output = command_handler["prompt"](msg)

if __name__ == "__main__":
    __main__()
