from pathlib import Path


def preprocess_command(s: str) -> list[str | Path]:
    """
        Функция, разделяющая полученную строку (команду) на название команды
        и её аргументы, также нормализует все пути в аргументах
        :param s:  строка с полученной командой
        :return: Возвращает предобработанную команду
    """

    parsed_command_and_args: list[tuple[str, str]] = []
    current_position = 0
    buffer = ""
    quoted = ""
    screened = False
    buffer_data_type = "OPTION"
    while current_position < len(s):
        if len(quoted) == 0 and s[current_position] == " " and not screened:
            if buffer[0] != "-" and len(buffer) > 1:
                buffer_data_type = "PATH"
            parsed_command_and_args.append((buffer, buffer_data_type))
            buffer = ""
            buffer_data_type = "OPTION"
        elif (s[current_position] == "'" or s[current_position] == '"') and not screened:
            buffer_data_type = "PATH"
            if quoted == s[current_position]:
                quoted = ""
            else:
                if len(quoted) == 0:
                    quoted = s[current_position]
                else:
                    buffer += s[current_position]
        elif s[current_position] == "\\" and not screened:
            buffer_data_type = "PATH"
            screened = True
        else:
            buffer += s[current_position]
            screened = False
        current_position += 1
    if len(buffer) != 0:
        if buffer[0] != "-" and len(buffer) > 1:
            buffer_data_type = "PATH"
        parsed_command_and_args.append((buffer, buffer_data_type))
    if len(quoted) != 0:
        return ["ERROR: unclosed quote"]

    command_and_correct_paths: list[str | Path] = [parsed_command_and_args[0][0]]
    if len(parsed_command_and_args) > 1:
        for arg in parsed_command_and_args[1:]:
            if arg[1] == "OPTION":
                command_and_correct_paths.extend(["-" + option for option in arg[0][1:]])
                continue
            else:
                command_and_correct_paths.append(Path(arg[0]).expanduser().resolve())

    return command_and_correct_paths
