def test_preprocessor_error_nonexistent_command(bash_processor):
    assert bash_processor.command("hah") == "ERROR: undefined command\n"


def test_preprocessor_error_nonexistent_option(bash_processor):
    assert bash_processor.command("grep -goida") == "ERROR: unexpected option for command\n"


def test_preprocessor_unclosed_quote(bash_processor):
    assert bash_processor.command("grep 'quote") == "ERROR: unclosed quote\n"


def test_bash_processor_nothing_input(bash_processor):
    assert bash_processor.command("") == ""


def test_preprocessor_very_many_options(bash_processor):
    assert bash_processor.command("grep -ririririiririrri '0' 0.txt") == "1: 0\n"
