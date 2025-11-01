from os.path import expanduser


def test_base_cd_work(bash_processor):
    assert bash_processor.command("cd ls_folder") == ""
    assert bash_processor.get_current_directory() == "/data/ls_folder"


def test_cd_work_without_args(bash_processor):
    assert bash_processor.command("cd") == ""
    assert bash_processor.get_current_directory() == expanduser("~")


def test_cd_error_too_many_args(bash_processor):
    assert bash_processor.command("cd ar1 ar2 r ar4") == "ERROR: too many arguments for cd command\n"


def test_cd_error_nonexistent_dir(bash_processor):
    assert bash_processor.command("cd nonexist") == "ERROR: directory does not exist\n"


def test_cd_error_file(bash_processor):
    assert bash_processor.command("cd 0.txt") == "ERROR: trying to cd into file\n"


def test_cd_error_permission(bash_processor):
    assert bash_processor.command("cd permitted") == "ERROR: permission denied\n"
