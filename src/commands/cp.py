from shutil import copy2, copytree, SameFileError
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
            for path in args[:-1]:
                if options["-r"]:
                    copytree(path, args[-1], dirs_exist_ok=True)
                else:
                    copy2(path, args[-1])
    except FileNotFoundError:
        estream += "ERROR: no such file\n"
    except PermissionError:
        estream += "ERROR: permission denied\n"
    except SameFileError:
        if not options["-r"]:
            if any(Path(path).is_dir() for path in args_[:-1]):
                estream += "ERROR: trying to copy directory without -r\n"
    except IsADirectoryError:
        estream += "ERROR: trying to copy directory without -r\n"
    return estream, ostream
