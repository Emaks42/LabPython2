from pathlib import Path
from src.constants import COMMANDS_AND_OPTIONS, COMMANDS_REQUIRES_TEXT_ARGS


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
    text_arg_required = 0
    while current_position < len(s):
        if len(quoted) == 0 and s[current_position] == " " and not screened:
            if (buffer[0] != "-" and buffer_data_type == "OPTION") or buffer == "-":
                buffer_data_type = "PATH"
            if buffer_data_type == "PATH" and text_arg_required > 0:
                buffer_data_type = "TEXT"
                text_arg_required -= 1
            parsed_command_and_args.append((buffer, buffer_data_type))
            buffer = ""
            buffer_data_type = "OPTION"
            if len(parsed_command_and_args) == 1:
                if parsed_command_and_args[0][0] in COMMANDS_REQUIRES_TEXT_ARGS.keys():
                    text_arg_required = COMMANDS_REQUIRES_TEXT_ARGS[parsed_command_and_args[0][0]]
        elif (s[current_position] == "'" or s[current_position] == '"') and not screened:
            buffer_data_type = "PATH"
            buffer += s[current_position]
            if quoted == s[current_position]:
                quoted = ""
            else:
                if len(quoted) == 0:
                    quoted = s[current_position]
                else:
                    buffer += s[current_position]
        elif s[current_position] == "\\" and not screened:
            buffer_data_type = "PATH"
            buffer += s[current_position]
            screened = True
        else:
            buffer += s[current_position]
            screened = False
        current_position += 1
    if len(buffer) != 0:
        if (buffer[0] != "-" and buffer_data_type == "OPTION") or buffer == "-":
            buffer_data_type = "PATH"
        if buffer_data_type == "PATH" and text_arg_required > 0:
            buffer_data_type = "TEXT"
            text_arg_required -= 1
        parsed_command_and_args.append((buffer, buffer_data_type))
    if len(quoted) != 0:
        return ["ERROR: unclosed quote\n"]

    if len(parsed_command_and_args) > 0:
        command_and_correct_paths: list[str | Path] = [parsed_command_and_args[0][0]]
    else:
        return []
    if parsed_command_and_args[0][0] not in COMMANDS_AND_OPTIONS.keys():
        return ["ERROR: undefined command\n"]
    if len(parsed_command_and_args) > 1:
        for arg in parsed_command_and_args[1:]:
            if arg[1] == "OPTION":
                extended_options = ["-" + option for option in arg[0][1:]]
                if any(option not in COMMANDS_AND_OPTIONS[str(parsed_command_and_args[0][0])]
                        for option in extended_options):
                    return ["ERROR: unexpected option for command\n"]
                command_and_correct_paths.extend(extended_options)
                continue
            elif arg[1] == "TEXT":
                command_and_correct_paths.append(arg[0])
            else:
                command_and_correct_paths.append(Path(arg[0]).expanduser().resolve())
    return command_and_correct_paths
