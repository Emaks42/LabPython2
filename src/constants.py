QUOTE_REQUIRED_SYMBOLS: str = " $/*?"
COMMANDS_AND_OPTIONS: dict[str, list[str]] = {
    "ls": ["-l"],
    "mv": [],
    "cat": [],
    "cd": [],
    "cp": ["-r"],
    "rm": ["-r", "-f"],
}
