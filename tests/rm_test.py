from src.bash_processor import BashProcessor


def test_rm_base_work(bash_processor):
    assert bash_processor.command("rm 0.txt") == ""
    assert bash_processor.command("ls") == '.\n1.txt\n2.txt\n3.txt\n4.txt\n5.txt\n6.txt\n7.txt' \
                                           '\n8.txt\n9.txt\nls_folder\npermitted\n'


def test_rm_multiple_args(bash_processor):
    assert bash_processor.command("rm 0.txt 2.txt 4.txt 6.txt 8.txt") == ""
    assert bash_processor.command("ls") == '.\n1.txt\n3.txt\n5.txt\n7.txt' \
                                           '\n9.txt\nls_folder\npermitted\n'


def test_rm_dirs(tmp_path, monkeypatch):
    bash_processor = BashProcessor(str(tmp_path))
    (tmp_path / "ls_folder").mkdir()
    monkeypatch.setattr('builtins.input', absolute_input)
    assert bash_processor.command("rm -r ls_folder") == ""
    assert bash_processor.command("ls") == ".\n\n"


def test_rm_dirs_f(tmp_path):
    bash_processor = BashProcessor(str(tmp_path))
    (tmp_path / "ls_folder").mkdir()
    assert bash_processor.command("rm -rf ls_folder") == ""
    assert bash_processor.command("ls") == ".\n\n"


def absolute_input(s: str):
    if s[:28] == "Вы хотите удалить директорию":
        return "pass"
    else:
        return "y"


def test_rm_error_no_args(bash_processor):
    assert bash_processor.command("rm") == "ERROR: missing file operand\n"


def test_rm_error_root_dir_remove(bash_processor):
    bash_processor.command("cd ls_folder")
    assert bash_processor.command("rm /") == "ERROR: trying to remove root directory\n"


def test_rm_error_parent_dir_remove(bash_processor):
    assert bash_processor.command("rm ..") == "ERROR: trying to remove parent directory\n"


def test_rm_error_no_such_file(bash_processor):
    assert bash_processor.command("rm nonex") == "ERROR: no such file\n"


def test_rm_error_permission(bash_processor):
    assert bash_processor.command("rm permitted") == "ERROR: permission denied\n"


def test_rm_error_remove_dir_without_r(bash_processor):
    assert bash_processor.command("rm ls_folder") == "ERROR: trying to remove directory without -r\n"
