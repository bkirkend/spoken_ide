import threading
from src.commands import *
from src.ide import *
from src.speech_to_text import *
from src.gpt import *

ide = None

def run_ide():
    global ide
    app = QApplication(sys.argv)
    ide = PythonIDE()
    ide.show()
    sys.exit(app.exec_())

def run_listener():
    while ide is None:  # Ensure ide is initialized before starting the listener
        time.sleep(0.1)  # Wait until ide is ready

    start(ide)  # Pass ide into the listener thread
    while not done:
        time.sleep(1)
    stop()

def __main__():
    listen_thread = threading.Thread(target=run_listener, daemon=True)
    listen_thread.start()
    run_ide()

if __name__ == "__main__":
    __main__()
