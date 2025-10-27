from shutil import copy2, copytree, SameFileError
from src.constants import COMMANDS_AND_OPTIONS


def cp_func(*args) -> tuple[str, str]:
    """
        Функция, реализующая работу команды cp (поддерживает опцию -r)
        :return: Возвращает результат работы команды (ошибки)
    """
    ostream = ""
    estream = ""
    args_ = list(args)
    opt = COMMANDS_AND_OPTIONS["cp"]
    options = dict(zip(opt, [False] * len(opt)))
    while any(option in args_ for option in opt):
        for option in opt:
            if option in args_:
                options[option] = True
                args_.remove(option)
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
            if any(path.is_dir() for path in args_[:-1]):
                estream += "ERROR: trying to copy directory without -r\n"
    except IsADirectoryError:
        estream += "ERROR: trying to copy directory without -r\n"
    return estream, ostream
