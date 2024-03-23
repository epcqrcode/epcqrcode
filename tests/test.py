# Dependencies: pyzbar, pillow
import sys
import os
import subprocess
from pyzbar.pyzbar import decode
from PIL import Image

class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    END = '\033[0m'

def cprint(text: str, color: Color) -> None:
    print(color + text + Color.END)

def compare_lists(a, b) -> bool:
    if len(a) != len(b):
        return False
    for i, line in enumerate(a):
        if line != b[i]:
            return False
    return True


class Test:

    def __init__(self, path: str) -> None:
        self.path = path
        self.dir_path = os.path.dirname(path)
        self.file = os.path.basename(path)
        self.image = None
        self.expected_returncode = None
        self.expected_lines = []
        self.expected_error = None
        self.returncode = None
        self.lines = []
        self.errors = []
    
    def __eval__(self) -> None:
        if self.expected_returncode == 0:
            self.__decode_qr__()
            if compare_lists(self.expected_lines, self.lines):
                cprint(self.file, color=Color.GREEN)
            else:
                cprint(self.file, color=Color.RED)
                print(" Expected QR-Code:\n", self.expected_lines)
                print(" Got QR-Code:\n", self.lines, "\n")
        else:
            self.__parse_log__()
            if self.expected_error in self.errors:
                cprint(self.file, Color.GREEN)
            else:
                cprint(self.file, Color.RED)
                print(" Expected Error:", self.expected_error)
                print(" Got Error:", self.errors)

    def __parse_test__(self) -> None:
        with open(self.path, 'r') as f:
            lines = f.readlines()
            for index, line in enumerate(lines):
                if "%TEST" in line:
                    self.expected_returncode = int(line.split()[1])
                    if self.expected_returncode == 0:
                        for i in range(index + 1, index + 13):
                            self.expected_lines.append(lines[i][1:].replace("\n", ""))
                        while self.expected_lines[-1] == '':
                            self.expected_lines = self.expected_lines[:-1]
                    else:
                        self.expected_error = lines[index + 1][1:].replace("\n", "")
                    break
    
    def __decode_qr__(self) -> None:
        self.__convert__()
        qr = decode(Image.open(self.image))[0].data.decode('utf8')
        self.lines = qr.splitlines()

    def __parse_log__(self) -> None:
        log_file = self.file.replace(".tex", ".log")
        with open(log_file, 'r') as f:
            for line in f.readlines():
                if "Package epcqr Error" in line:
                    self.errors.append(line.split("Error: ", 1)[1][:-2])
                if "Package epcqr Warning" in line:
                    line = line.split(" on input line")[0]
                    self.errors.append(line.split("Warning: ", 1)[1])

    def __compile__(self) -> None:
        os.chdir(self.dir_path)
        args = ["latexmk", "--pdf", "-interaction=nonstopmode", "-Werror", self.file]
        result = subprocess.run(args, capture_output=True)
        self.returncode = result.returncode
    
    def __clean__(self) -> None:
        os.chdir(self.dir_path)
        args = ["latexmk", "-C", self.file]
        _ = subprocess.run(args, capture_output=True)
        if self.image != None: subprocess.run(["rm", self.image], capture_output=True)
    
    def __convert__(self, extension=".png") -> None:
        self.image = self.file.replace(".tex", extension)
        pdf_file = self.file.replace(".tex", ".pdf")
        args = ["convert", "-trim", "-density", "150", "-quality", "100", pdf_file, self.image]
        _ = subprocess.run(args, capture_output=True)

    def run(self) -> None:
        current_dir = os.getcwd()
        self.__parse_test__()
        self.__compile__()
        self.__eval__()
        self.__clean__()
        os.chdir(current_dir)

def main():
    if len(sys.argv) == 1: 
        print("Usage:", "test.py", "<directory>", "(filter name)")
        exit(1)
    directory = sys.argv[1]
    filter = sys.argv[2] if len(sys.argv) >= 3 else ""
    for dir, _, files in os.walk(directory):
        for file in files:
            if file.endswith("tex") and filter in file:
                abs_path = os.path.abspath(os.path.join(dir, file))
                Test(path=abs_path).run()

if __name__ == "__main__":
    main()