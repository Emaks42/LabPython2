from src.preprocessor import preprocess_command
from src.ls import ls_func
from os import chdir
from os import getcwd
from os.path import abspath, expanduser, exists


class BashProcessor:
    def __init__(self, cur_dir=getcwd()):
        self.current_directory: str = abspath(expanduser(cur_dir))

    def command(self, command: str):
        command = command.strip()
        chdir(self.current_directory)
        parsed_command = preprocess_command(command)
        if parsed_command[0] == "ls":
            print(self.ls(*parsed_command[1:]))
        elif parsed_command[0] == "cd":
            self.cd(*parsed_command[1:])
        elif parsed_command[0] == "cat":
            self.cat(*parsed_command[1:])
        elif str(parsed_command[0])[:5] == "ERROR":
            print(parsed_command[0])
        else:
            print("ERROR: undefined command")
        return parsed_command

    def ls(self, *args) -> str:
        chdir(self.current_directory)
        return ls_func(*args)

    def cd(self, *args) -> None:
        if len(args) > 1:
            print("ERROR: too many arguments for cd command")
        elif len(args) == 0:
            self.current_directory = expanduser("~")
        else:
            path_ = str(args[0])
            if exists(path_):
                self.current_directory = str(path_)
            else:
                print("ERROR: directory does not exist")

    def cat(self, *args):
        pass

    def get_current_directory(self) -> str:
        return self.current_directory
