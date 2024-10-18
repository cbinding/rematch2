from datetime import datetime as DT

class LogFile:

    def __init__(self, file_name: str = "", clear_previous: bool = True):        

        if len(file_name.strip()) > 0:
            self.file_path = file_name.strip()
        else:
            datestamp = DT.now().strftime('%Y%m%d')
            self.file_path = f"log-{datestamp}.txt"
        
        if (clear_previous):
            self.clear()

    def clear(self):
        with open(self.file_path, "w") as f:
            f.write("")

    def write(self, msg: str, print_to_screen: bool = True):
        timestamp = DT.now().strftime('%Y%m%dT%H%M%S')
        s = f"\n{timestamp} " + msg
        with open(self.file_path, "a") as f:
            f.write(s)
        if (print_to_screen):
            print(s)