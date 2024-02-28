class LogFile:

    def __init__(self, file_name: str = "", clear_previous: bool = True):
        self.file_path = "results.txt"

        if len(file_name.strip()) > 0:
            self.file_path = file_name.strip()
        if (clear_previous):
            self.clear()

    def clear(self):
        with open(self.file_path, "w") as f:
            f.write("")

    def append(self, s: str, print_to_screen: bool = True):
        with open(self.file_path, "a") as f:
            f.write("\n" + s)
        if (print_to_screen):
            print("\n" + s)