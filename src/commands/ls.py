from os import listdir, stat
from os.path import exists
from time import ctime
from src.constants import QUOTE_REQUIRED_SYMBOLS
from src.preprocessor import preprocess_options_for_command


def get_readable_permissions(perm: int) -> str:
    """
        Функция, переводящая записанные в десятичном виде права доступа в читаемый
        человеком вид (как в обычной команде ls -l)
        :param perm: десятичная запись прав доступа к файлу (директории)
        (плюс некоторая дополнительная информация)
        :return: Возвращает читаемую человеком запись прав доступа
    """
    perm_bits = f"{perm: b}"[-9:]
    mask = "rwx" * 3
    return "".join([mask[i] if perm_bits[i] == '1' else "-" for i in range(9)])


def ls_func(*args) -> tuple[str, str]:
    """
        Функция, реализующая работу команды ls (поддерживает опцию -l)
        :return: Возвращает результат работы команды
    """
    ostream = ""
    estream = ""
    args_, options = preprocess_options_for_command("ls", *args)
    if len(args_) == 0:
        args_.append(".")
    for path in args_:
        try:
            if not options["-l"]:
                if exists(str(path)):
                    ostream += str(path) + "\n"
                ls_raw_result = sorted(listdir(str(path)))
                ls_correct_result = []
                for obj in ls_raw_result:
                    if any(symbol in obj for symbol in QUOTE_REQUIRED_SYMBOLS):
                        if "'" not in obj:
                            ls_correct_result.append("'" + obj + "'")
                        else:
                            ls_correct_result.append('"' + obj + '"')
                    else:
                        ls_correct_result.append(obj)
                ostream += "\n".join(ls_correct_result) + "\n"
            else:
                if exists(str(path)):
                    ostream += str(path) + "\n"
                ls_raw_result = sorted(listdir(str(path)))
                ls_correct_result = []
                for obj in ls_raw_result:
                    line = ""
                    if any(symbol in obj for symbol in QUOTE_REQUIRED_SYMBOLS):
                        if "'" not in obj:
                            line += "'" + obj + "'"
                        else:
                            line += '"' + obj + '"'
                    else:
                        line += obj
                    line += " "
                    line += str(stat(str(path) + "/" + obj).st_size) + " "
                    line += str(ctime(stat(str(path) + "/" + obj).st_mtime)) + " "
                    line += get_readable_permissions(stat(str(path) + "/" + obj).st_mode)
                    ls_correct_result.append(line + "\n")
                ostream += "".join(ls_correct_result) + "\n"
        except FileNotFoundError:
            estream += "ERROR: no such file or directory\n"
        except PermissionError:
            estream += "ERROR: permission denied\n"
    return estream, ostream
