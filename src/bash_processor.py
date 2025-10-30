from src.preprocessor import preprocess_command
from src.commands.ls import ls_func
from src.commands.cp import cp_func
from src.commands.rm import rm_func
from src.commands.grep import grep_func
from src.commands.cat import cat_func
from src.commands.zip_and_tar import zip_func, tar_func, untar_func, unzip_func
from os import chdir, getcwd
from os.path import abspath, expanduser, exists
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
            "ls": ls_func,
            "cd": self.cd,
            "cp": cp_func,
            "cat": cat_func,
            "rm": rm_func,
            "mv": self.mv,
            "zip": zip_func,
            "unzip": unzip_func,
            "tar": tar_func,
            "untar": untar_func,
            "grep": grep_func,
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
        if len(parsed_command) == 0:
            return ""
        if parsed_command[0] in self.available_commands.keys():
            logging.info(command)
            chdir(self.current_directory)
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
        rm_ = rm_func(*(list(args[:-1]) + ["-f"]))
        if len(rm_[0].replace("ERROR: no such file\n", "")) != 0:
            return rm_[0].replace("ERROR: no such file\n", ""), ""
        return "", ""

    def get_current_directory(self) -> str:
        """
            Функция, возвращающая текущую рабочую директорию
            :return: Возвращает текущую рабочую директорию
        """
        return self.current_directory
