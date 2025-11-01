import pytest


@pytest.mark.parametrize("command_,expected", [(f"cat {num}.txt", f"{num}\n") for num in range(10)])
def test_cat_base_work(bash_processor, command_, expected):
    assert bash_processor.command(command_) == expected


def test_cat_multiple_args(bash_processor):
    assert bash_processor.command("cat 0.txt 1.txt 0.txt") == "0\n1\n0\n"


def test_cat_error_none_args(bash_processor):
    assert bash_processor.command("cat") == "ERROR: file not given to command\n"


def test_cat_error_nonexistent_file(bash_processor):
    assert bash_processor.command("cat nonex") == "ERROR: file does not exist\n"


def test_cat_error_is_a_directory(bash_processor):
    assert bash_processor.command("cat ls_folder") == "ERROR: given directory not file\n"


def test_cat_error_permission(bash_processor):
    assert bash_processor.command("cat permitted/secret") == "ERROR: permission denied\n"


def test_cat_error_incorrect_encoding(bash_processor):
    bash_processor.command("zip ls_folder ls_folder.zip")
    path = "/data/ls_folder.zip"
    assert bash_processor.command("cat ls_folder.zip") == f"ERROR: incorrect encoding of file {path}\n"
