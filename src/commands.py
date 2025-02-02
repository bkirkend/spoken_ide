#command parser based on spoken input

from gpt import *

def parse_command(msg):
    pass

def handle_prompt(msg):
    print(output := gpt(msg))
    return output

def handle_line(msg, line_num):
    suffix = f"only change line {line_num}"
    print(output := gpt(msg + suffix))
    return output

def handle_clear_history(msg):
    clear_discourse()

def handle_run(msg):
    pass

def handle_up(msg):
    pass

def handle_down(msg):
    pass

def handle_left(msg):
    pass

def handle_right(msg):
    pass

def handle_save(msg):
    pass

def handle_confirm(msg):
    pass

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
}

def __main__():
    msg = "determine if a number is prime"
    output = command_handler["prompt"](msg)

if __name__ == "__main__":
    __main__()
