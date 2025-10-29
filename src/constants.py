QUOTE_REQUIRED_SYMBOLS: str = " $/*?"
COMMANDS_AND_OPTIONS: dict[str, list[str]] = {
    "ls": ["-l"],
    "mv": [],
    "cat": [],
    "cd": [],
    "cp": ["-r"],
    "zip": [],
    "unzip": [],
    "tar": [],
    "untar": [],
    "rm": ["-r", "-f"],
    "grep": ["-r", "-i"],
}
COMMANDS_REQUIRES_TEXT_ARGS: dict[str, int] = {
    "grep": 1,
}
