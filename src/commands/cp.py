from shutil import copy2, copytree
from pathlib import Path
from src.preprocessor import preprocess_options_for_command


def cp_func(*args) -> tuple[str, str]:
    """
        Функция, реализующая работу команды cp (поддерживает опцию -r)
        :return: Возвращает результат работы команды (ошибки)
    """
    ostream = ""
    estream = ""
    args_, options = preprocess_options_for_command("cp", *args)
    try:
        if len(args_) == 0:
            estream += "ERROR: missing file operand\n"
        elif len(args_) == 1:
            estream += "ERROR: not specified directory to copy\n"
        else:
            for path in args_[:-1]:
                if options["-r"]:
                    if path != args_[-1]:
                        copytree(path, args_[-1], dirs_exist_ok=True)
                else:
                    if path != args_[-1]:
                        copy2(path, args_[-1])
                    if Path(path).is_dir() or Path(args_[-1]).is_dir():
                        estream += "ERROR: trying to copy directory without -r\n"
    except FileNotFoundError:
        estream += "ERROR: no such file\n"
    except PermissionError:
        estream += "ERROR: permission denied\n"
    except IsADirectoryError:
        estream += "ERROR: trying to copy directory without -r\n"
    return estream, ostream
