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
                            format="[%(asctime)s %(name)s] %(message)s",
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
            return self.available_commands[str(parsed_command[0])](*parsed_command[1:])
        else:
            logging.error(str(parsed_command[0]))
            return str(parsed_command[0])

    def ls(self, *args) -> str:
        """
            Функция, вызывающая функцию ls_func из другого фойла
            :return: Возвращает результат работы функции
        """
        chdir(self.current_directory)
        ls_ = ls_func(*args)
        if ls_[:5] != "ERROR":
            logging.info("SUCCESS")
        else:
            logging.error(ls_[:-1])
        return ls_

    def cd(self, *args) -> str:
        """
            Функция, реализующая работу команды cd
            (оставлена в осоновном файле из-за небольшого размера)
            :return: Возвращает результат работы команды (ошибки)
        """
        if len(args) > 1:
            logging.error("ERROR: too many arguments for cd command")
            return "ERROR: too many arguments for cd command\n"
        elif len(args) == 0:
            self.current_directory = expanduser("~")
        else:
            path_ = str(args[0])
            if exists(path_):
                self.current_directory = str(path_)
            else:
                logging.error("ERROR: directory does not exist")
                return "ERROR: directory does not exist\n"
        logging.info("SUCCESS")
        return ""

    def cp(self, *args) -> str:
        """
            Функция, вызывающая функцию cp_func из другого фойла
            :return: Возвращает результат работы функции
        """
        chdir(self.current_directory)
        cp_ = cp_func(*args)
        if cp_[:5] != "ERROR":
            logging.info("SUCCESS")
        else:
            logging.error(cp_[:-1])
        return cp_

    def cat(self, *args) -> str:
        """
            Функция, реализующая работу команды cat
            (оставлена в осоновном файле из-за небольшого размера)
            :return: Возвращает результат работы команды
        """
        chdir(self.current_directory)
        answer = ""
        for path in args:
            if type(path) is PosixPath:
                if not path.exists():
                    logging.error("ERROR: file does not exist")
                    return "ERROR: file does not exist\n"
                elif path.is_dir():
                    logging.error("ERROR: given directory not file")
                    return "ERROR: given directory not file\n"
                else:
                    try:
                        file = path.read_text(encoding="utf-8")
                        answer += file + "\n"
                    except PermissionError:
                        logging.error("ERROR: permission denied")
                        return "ERROR: permission denied\n"
        logging.info("SUCCESS")
        return answer

    def rm(self, *args) -> str:
        """
            Функция, вызывающая функцию rm_func из другого фойла
            :return: Возвращает результат работы функции
        """
        chdir(self.current_directory)
        rm_ = rm_func(*args)
        if rm_[:5] != "ERROR":
            logging.info("SUCCESS")
        else:
            logging.error(rm_[:-1])
        return rm_

    def mv(self, *args) -> str:
        chdir(self.current_directory)
        cp_ = cp_func(*args)
        if cp_ != "":
            logging.error(cp_[:-1])
            return cp_
        rm_ = rm_func(*(list(args[:-1]) + ["-y"]))
        if rm_ != "" and rm_ != "ERROR: no such file\n":
            logging.error(rm_[:-1])
            return rm_
        logging.info("SUCCESS")
        return ""

    def get_current_directory(self) -> str:
        """
            Функция, возвращающая текущую рабочую директорию
            :return: Возвращает текущую рабочую директорию
        """
        return self.current_directory
