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
        try:
            if not path.exists():
                estream += "ERROR: file does not exist\n"
            elif path.is_dir():
                estream += "ERROR: given directory not file\n"
            else:
                file = path.read_text(encoding="utf-8")
                ostream += file + "\n"
        except Exception:
            estream += "ERROR: something gone wrong....\n"
    return estream, ostream
