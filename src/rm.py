from shutil import rmtree
from pathlib import Path
from src.constants import COMMANDS_AND_OPTIONS


def rm_func(*args):
    """
        Функция, реализующая работу команды rm (поддерживает опции -r и
        -y (специальная опция для автоматического подтверждения удаления директорий))
        :return: Возвращает результат работы команды (ошибки)
    """
    args_ = list(args)
    opt = COMMANDS_AND_OPTIONS["rm"]
    options = dict(zip(opt, [False] * len(opt)))
    while any(option in args_ for option in opt):
        for option in opt:
            if option in args_:
                options[option] = True
                args_.remove(option)
    try:
        if len(args_) == 0:
            return "ERROR: missing file operand\n"
        else:
            for path in args_:
                if path == Path("..").resolve():
                    return "ERROR: trying to remove parent directory\n"
                elif path == Path("/").resolve():
                    return "ERROR: trying to remove root directory\n"
                elif path == Path("C:\\").resolve():
                    return "ERROR: trying to remove root directory\n"
                elif options["-r"]:
                    if not options["-y"]:
                        permission = input(f"Вы хотите удалить директорию {path}? (y/n)").lower()
                        while not(permission == "y" or permission == "n"):
                            permission = input("Возможно вы не дочитали. " +
                                               f"Вы хотите удалить директорию {path}? (y/n)").lower()
                            print(permission)
                        if permission == "y":
                            rmtree(str(path))
                    else:
                        rmtree(str(path))
                else:
                    path.unlink()
    except FileNotFoundError:
        return "ERROR: no such file\n"
    except PermissionError:
        return "ERROR: permission denied\n"
    except IsADirectoryError:
        return "ERROR: trying to remove directory without -r\n"
    return ""
