from src.preprocessor import preprocess_command
from src.ls import ls_func
from src.cp import cp_func
from src.rm import rm_func
from os import chdir, getcwd
from os.path import abspath, expanduser, exists
from pathlib import PosixPath
import logging


class BashProcessor:
    def __init__(self, cur_dir: str = getcwd()) -> None:
        """
            Функция инициализирующая класс,также отвечает за инициализацию логирования
            :param cur_dir: изначальная директория консоли (по умолчанию - директория запуска)
        """
        logging.basicConfig(filename="shell.log",
                            level=logging.INFO,
                            format="[%(asctime)s] %(message)s",
                            filemode="w")
        self.current_directory: str = abspath(expanduser(cur_dir))
        self.available_commands = {
            "ls": self.ls,
            "cd": self.cd,
            "cp": self.cp,
            "cat": self.cat,
            "rm": self.rm,
            "mv": self.mv,
        }

    def command(self, command: str) -> str:
        """
            Функция, принимающая и исполняющая команду
            :param command: переданная команда
            :return: Возвращает результат работы команды
        """
        command = command.strip()
        chdir(self.current_directory)
        parsed_command = preprocess_command(command)
        if parsed_command[0] in self.available_commands.keys():
            logging.info(command)
            command_result = self.available_commands[str(parsed_command[0])](*parsed_command[1:])
            if len(command_result[0]) != 0:
                for err in command_result[0][:-1].split("\n"):
                    logging.error(err)
            else:
                logging.info("SUCCESS")
            return command_result[0] + command_result[1]
        else:
            logging.error(str(parsed_command[0])[:-1])
            return str(parsed_command[0])

    def ls(self, *args) -> tuple[str, str]:
        """
            Функция, вызывающая функцию ls_func из другого фойла
            :return: Возвращает результат работы функции
        """
        chdir(self.current_directory)
        return ls_func(*args)

    def cd(self, *args) -> tuple[str, str]:
        """
            Функция, реализующая работу команды cd
            (оставлена в осоновном файле из-за небольшого размера)
            :return: Возвращает результат работы команды (ошибки)
        """
        ostream = ""
        estream = ""
        if len(args) > 1:
            estream += "ERROR: too many arguments for cd command\n"
        elif len(args) == 0:
            self.current_directory = expanduser("~")
        else:
            path_ = str(args[0])
            if exists(path_):
                self.current_directory = str(path_)
            else:
                estream += "ERROR: directory does not exist\n"
        return estream, ostream

    def cp(self, *args) -> tuple[str, str]:
        """
            Функция, вызывающая функцию cp_func из другого фойла
            :return: Возвращает результат работы функции
        """
        chdir(self.current_directory)
        return cp_func(*args)

    def cat(self, *args) -> tuple[str, str]:
        """
            Функция, реализующая работу команды cat
            (оставлена в осоновном файле из-за небольшого размера)
            :return: Возвращает результат работы команды
        """
        chdir(self.current_directory)
        ostream = ""
        estream = ""
        for path in args:
            if type(path) is PosixPath:
                if not path.exists():
                    estream += "ERROR: file does not exist\n"
                elif path.is_dir():
                    estream += "ERROR: given directory not file\n"
                else:
                    try:
                        file = path.read_text(encoding="utf-8")
                        ostream += file + "\n"
                    except PermissionError:
                        estream += "ERROR: permission denied\n"
        return estream, ostream

    def rm(self, *args) -> tuple[str, str]:
        """
            Функция, вызывающая функцию rm_func из другого фойла
            :return: Возвращает результат работы функции
        """
        chdir(self.current_directory)
        return rm_func(*args)

    def mv(self, *args) -> tuple[str, str]:
        """
            Функция, реализующая работу команды mv как композицию команд rm и cp
            (оставлена в осоновном файле из-за небольшого размера)
            :return: Возвращает результат работы команды
        """
        chdir(self.current_directory)
        cp_ = cp_func(*args)
        if len(cp_[0]) != 0:
            return cp_
        rm_ = rm_func(*(list(args[:-1]) + ["-y"]))
        if len(rm_[0].replace("ERROR: no such file\n", "")) != 0:
            return rm_[0].replace("ERROR: no such file\n", ""), ""
        return "", ""

    def get_current_directory(self) -> str:
        """
            Функция, возвращающая текущую рабочую директорию
            :return: Возвращает текущую рабочую директорию
        """
        return self.current_directory
