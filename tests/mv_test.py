from src.bash_processor import BashProcessor


def test_mv_base_work(bash_processor):
    assert bash_processor.command("mv 3.txt ls_folder/3.txt") == ""
    assert bash_processor.command("ls") == '.\n0.txt\n1.txt\n2.txt\n4.txt\n5.txt\n6.txt\n7.txt' \
                                           '\n8.txt\n9.txt\nls_folder\npermitted\n'
    assert bash_processor.command("ls ls_folder") == '/data/ls_folder\n0.txt\n1.txt\n2.txt\n3.txt\n'


def test_mv_renaming(bash_processor):
    assert bash_processor.command("mv 3.txt 0b11.txt") == ""
    assert bash_processor.command("ls") == '.\n0.txt\n0b11.txt\n1.txt\n2.txt\n4.txt\n5.txt\n6.txt\n7.txt' \
                                           '\n8.txt\n9.txt\nls_folder\npermitted\n'


def test_mv_moving_dir(tmp_path):
    bash_processor = BashProcessor(str(tmp_path))
    (tmp_path / "mv_folder").mkdir()
    (tmp_path / "mv_folder_2").mkdir()
    assert bash_processor.command("mv -r mv_folder_2 mv_folder/mv_folder_2") == ""
    assert bash_processor.command("cd mv_folder") == ""
    assert bash_processor.command("ls") == ".\nmv_folder_2\n"


def test_mv_multiple_args(bash_processor):
    assert bash_processor.command("mv 3.txt 4.txt ls_folder/3.txt") == ""
    assert bash_processor.command("ls") == '.\n0.txt\n1.txt\n2.txt\n5.txt\n6.txt\n7.txt' \
                                           '\n8.txt\n9.txt\nls_folder\npermitted\n'
    assert bash_processor.command("ls ls_folder") == '/data/ls_folder\n0.txt\n1.txt\n2.txt\n3.txt\n'
    assert bash_processor.command("cat ls_folder/3.txt") == "4\n"


def test_mv_error_nonexistent_file(bash_processor):
    assert bash_processor.command("mv 10.txt 12.txt") == "ERROR: no such file\n"


def test_mv_error_permission(bash_processor):
    assert bash_processor.command("mv permitted/secret non_secret") == "ERROR: permission denied\n"
