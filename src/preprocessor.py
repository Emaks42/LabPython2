from pathlib import Path


def preprocess_command(s: str) -> list[str | Path]:
    """
        Функция, разделяющая полученную строку (команду) на название команды
        и её аргументы, также нормализует все пути в аргументах
        :param s:  строка с полученной командой
        :return: Возвращает предобработанную команду
    """

    parsed_command_and_args: list[str] = []
    current_position = 0
    buffer = ""
    quoted = ""
    screened = False
    while current_position < len(s):
        if len(quoted) == 0 and s[current_position] == " " and not screened:
            parsed_command_and_args.append(buffer)
            buffer = ""
        elif (s[current_position] == "'" or s[current_position] == '"') and not screened:
            if quoted == s[current_position]:
                quoted = ""
            else:
                if len(quoted) == 0:
                    quoted = s[current_position]
                else:
                    buffer += s[current_position]
        elif s[current_position] == "\\" and not screened:
            screened = True
        else:
            buffer += s[current_position]
            screened = False
        current_position += 1
    if len(buffer) != 0:
        parsed_command_and_args.append(buffer)
    if len(quoted) != 0:
        return ["ERROR: unclosed quote"]

    command_and_correct_paths: list[str | Path] = [parsed_command_and_args[0]]
    if len(parsed_command_and_args) > 1:
        for arg in parsed_command_and_args[1:]:
            if arg[0] == "-" and len(arg) > 1:
                command_and_correct_paths.append(arg)
                continue
            else:
                command_and_correct_paths.append(Path(arg).expanduser().resolve())

    return command_and_correct_paths
