from shutil import copy2, copytree
from src.preprocessor import preprocess_options_for_command


def cp_func(*args) -> tuple[str, str]:
    """
        Функция, реализующая работу команды cp (поддерживает опцию -r)
        :return: Возвращает результат работы команды (ошибки)
    """
    ostream = ""
    estream = ""
    args_, options = preprocess_options_for_command("cp", *args)
    if len(args_) == 0:
        estream += "ERROR: missing file operand\n"
    elif len(args_) == 1:
        estream += "ERROR: not specified directory to copy\n"
    else:
        for path in args_[:-1]:
            try:
                if path == args_[-1]:
                    estream += "ERROR: copy object into same folder with original\n"
                    continue
                if options["-r"]:
                    copytree(path, args_[-1], dirs_exist_ok=True)
                else:
                    copy2(path, args_[-1])
            except FileNotFoundError:
                estream += "ERROR: no such file or directory\n"
            except FileExistsError:
                estream += "ERROR: try to copy directory into file\n"
            except PermissionError:
                estream += "ERROR: permission denied\n"
            except IsADirectoryError:
                estream += "ERROR: trying to copy directory without -r\n"
    return estream, ostream
