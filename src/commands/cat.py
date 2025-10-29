from pathlib import PosixPath


def cat_func(*args) -> tuple[str, str]:
    """
        Функция, реализующая работу команды cat
        :return: Возвращает результат работы команды
    """
    ostream = ""
    estream = ""
    if len(args) == 0:
        estream += "ERROR: file not given to command\n"
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
                except UnicodeDecodeError:
                    estream += f"ERROR: incorrect encoding of file {path}\n"
    return estream, ostream
