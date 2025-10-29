from re import findall
from src.constants import COMMANDS_AND_OPTIONS


def grep_func(*args) -> tuple[str, str]:
    ostream = ""
    estream = ""
    args_ = list(args)
    opt = COMMANDS_AND_OPTIONS["grep"]
    options = dict(zip(opt, [False] * len(opt)))
    while any(option in args_ for option in opt):
        for option in opt:
            if option in args_:
                options[option] = True
                args_.remove(option)
    if len(args_) == 0:
        estream += "ERROR: missing pattern operand\n"
        return estream, ostream
    elif len(args_) == 1:
        estream += "ERROR: not specified file or directory to search\n"
        return estream, ostream
    elif len(args_) > 2:
        estream += "ERROR: too many arguments to grep command\n"
        return estream, ostream
    pattern = args_[0]
    path = args_[1]
    if path.is_dir() and not options["-r"]:
        estream += "ERROR: trying to search in directory without -r\n"
        return estream, ostream
    if path.is_dir():
        for inner_path in path.iterdir():
            try:
                if inner_path.is_dir():
                    estream_, ostream_ = grep_func(pattern, inner_path,
                                                   *[opt if options[opt] else "-r" for opt in options.keys()])
                    estream += estream_
                    ostream += ostream_
                else:
                    analyze_text = str(inner_path.read_text(encoding="utf-8")).split("\n")
                    for line in range(len(analyze_text)):
                        if findall(str(pattern), analyze_text[line]):
                            ostream += str(inner_path) + " " + str(line + 1) + " " + analyze_text[line].strip() + '\n'
            except PermissionError:
                estream += "ERROR: permission denied\n"
            except UnicodeDecodeError:
                estream += f"ERROR: incorrect file format in file {inner_path}\n"
    else:
        try:
            analyze_text = str(path.read_text(encoding="utf-8")).split("\n")
            for line in range(len(analyze_text)):
                if findall(str(pattern), analyze_text[line]):
                    ostream += str(line + 1) + " " + analyze_text[line].strip() + '\n'
        except PermissionError:
            estream += "ERROR: permission denied\n"
        except UnicodeDecodeError:
            estream += "ERROR: incorrect file format\n"
    return estream, ostream
