from shutil import copy2, copytree, SameFileError


def cp_func(*args) -> str:
    """
        Функция, реализующая работу команды cp (поддерживает опцию -r)
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
        elif len(args_) == 1:
            return "ERROR: not specified directory to copy\n"
        elif len(args_) == 2:
            if is_r:
                copytree(args[0], args[1], dirs_exist_ok=True)
            else:
                copy2(args[0], args[1])
        else:
            for path in args[:-1]:
                if is_r:
                    copytree(path, args[-1], dirs_exist_ok=True)
                else:
                    copy2(path, args[-1])
    except FileNotFoundError:
        return "ERROR: no such file\n"
    except PermissionError:
        return "ERROR: permission denied\n"
    except SameFileError:
        if not is_r:
            if any(path.is_dir() for path in args_[:-1]):
                return "ERROR: trying to copy directory without -r\n"
    except IsADirectoryError:
        return "ERROR: trying to copy directory without -r\n"
    return ""
