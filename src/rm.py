from shutil import rmtree
from pathlib import Path


def rm_func(*args):
    """
        Функция, реализующая работу команды rm (поддерживает опцию -r)
        :return: Возвращает результат работы команды (ошибки)
    """
    args_ = list(args)
    is_r: bool
    if "-r" in args_:
        is_r = True
        while "-r" in args_:
            args_.remove("-r")
    else:
        is_r = False
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
                elif is_r:
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
