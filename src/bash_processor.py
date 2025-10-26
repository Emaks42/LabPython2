from src.preprocessor import preprocess_command
from src.ls import ls_func
from src.cp import cp_func
from os import chdir, getcwd
from os.path import abspath, expanduser, exists
from pathlib import PosixPath


class BashProcessor:
    def __init__(self, cur_dir: str = getcwd()):
        """
            Функция инициализирующая класс
            :param cur_dir: изначальная директория консоли (по умолчанию - директория запуска)
        """
        self.current_directory: str = abspath(expanduser(cur_dir))

    def command(self, command: str):
        """
            Функция, принимающая и исполняющая команду
            :param command: переданная команда
            :return: Возвращает результат работы команды
        """
        command = command.strip()
        chdir(self.current_directory)
        parsed_command = preprocess_command(command)
        if parsed_command[0] == "ls":
            return self.ls(*parsed_command[1:])
        elif parsed_command[0] == "cd":
            return self.cd(*parsed_command[1:])
        elif parsed_command[0] == "cat":
            return self.cat(*parsed_command[1:])
        elif parsed_command[0] == "cp":
            return self.cp(*parsed_command[1:])
        elif str(parsed_command[0])[:5] == "ERROR":
            return parsed_command[0]
        else:
            return "ERROR: undefined command\n"

    def ls(self, *args):
        """
            Функция, вызывающая функцию ls_func из другого фойла
            :return: Возвращает результат работы функции
        """
        chdir(self.current_directory)
        return ls_func(*args)

    def cd(self, *args) -> str:
        """
            Функция, реализующая работу команды cd
            (оставлена в осоновном файле из-за небольшого размера)
            :return: Возвращает результат работы команды (ошибки)
        """
        if len(args) > 1:
            return "ERROR: too many arguments for cd command\n"
        elif len(args) == 0:
            self.current_directory = expanduser("~")
        else:
            path_ = str(args[0])
            if exists(path_):
                self.current_directory = str(path_)
            else:
                return "ERROR: directory does not exist\n"
        return ""

    def cp(self, *args) -> str:
        """
            Функция, вызывающая функцию cp_func из другого фойла
            :return: Возвращает результат работы функции
        """
        chdir(self.current_directory)
        return cp_func(*args)

    def cat(self, *args) -> str:
        """
            Функция, реализующая работу команды cat
            (оставлена в осоновном файле из-за небольшого размера)
            :return: Возвращает результат работы команды
        """
        chdir(self.current_directory)
        answer = ""
        for path in args:
            if path is PosixPath:
                if not path.exists():
                    return "ERROR: file does not exist\n"
                elif path.is_dir():
                    return "ERROR: given directory not file\n"
                else:
                    try:
                        file = path.read_text(encoding="utf-8")
                        answer += file + "\n"
                    except PermissionError:
                        return "ERROR: permission denied\n"
        return ""

    def get_current_directory(self) -> str:
        """
            Функция, возвращающая текущую рабочую директорию
            :return: Возвращает текущую рабочую директорию
        """
        return self.current_directory
