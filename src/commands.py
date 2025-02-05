#command parser based on spoken input

from gpt import *

def parse_command(msg, ide):
    pass

def handle_prompt(msg, ide):
    print("in prompt handler")
    output = gpt(msg)
    ide.preview_signal.emit(output)
    return output

def handle_line(msg, line_num, ide):
    suffix = f"only change line {line_num}"
    print(output := gpt(msg + suffix))
    return output

def handle_clear_history(msg, ide):
    clear_discourse()

def handle_run(msg, ide):
    pass

def handle_up(msg, ide):
    pass

def handle_down(msg, ide):
    pass

def handle_left(msg, ide):
    pass

def handle_right(msg, ide):
    pass

def handle_save(msg, ide):
    pass

def handle_confirm(msg, ide):
    print("in confirm handler")
    ide.sync_window_signal.emit()

def handle_run(msg, ide):
   ide.run_code_signal.emit() 

#dictionary mapping commands to function handlers
command_handler = {
    "prompt" : handle_prompt,
    "line" : handle_line,
    "run" : handle_run,
    "clear history" : handle_clear_history,
    "up" :  handle_up,
    "down" :  handle_down,
    "right" :  handle_right,
    "left" :  handle_left,
    "save" : handle_save,
    "confirm" : handle_confirm,
    "run" : handle_run
}

def __main__():
    msg = "determine if a number is prime"
    output = command_handler["prompt"](msg)

if __name__ == "__main__":
    __main__()
