def test_cp_base_work(bash_processor):
    assert bash_processor.command("cp 0.txt 0.copy") == ""
    assert bash_processor.command("ls") == '.\n0.copy\n0.txt\n1.txt\n2.txt\n3.txt\n4.txt\n5.txt\n6.txt\n7.txt' \
                                           '\n8.txt\n9.txt\nls_folder\npermitted\n'


def test_cp_dir(bash_processor):
    assert bash_processor.command("cp -r ls_folder ls_copy") == ""
    assert bash_processor.command("ls ls_copy") == '/data/ls_copy\n0.txt\n1.txt\n2.txt\n'


def test_cp_multiple_dir(bash_processor):
    assert bash_processor.command("cp -r ls_folder ls_copy") == ""
    assert bash_processor.command("ls ls_copy") == '/data/ls_copy\n0.txt\n1.txt\n2.txt\n'
    assert bash_processor.command("cp -r ls_folder ls_copy ls_copy_copy") == ""
    assert bash_processor.command("ls ls_copy") == '/data/ls_copy\n0.txt\n1.txt\n2.txt\n'


def test_cp_self_copy(bash_processor):
    assert bash_processor.command("cp ls_folder ls_folder") == "ERROR: trying to copy directory without -r\n"
    assert bash_processor.command("cp -r ls_folder ls_folder") == ""
    assert bash_processor.command("cp 0.txt 0.txt") == ""


def test_cp_error_not_enough_args(bash_processor):
    assert bash_processor.command("cp ls_folder") == "ERROR: not specified directory to copy\n"


def test_cp_error_no_args(bash_processor):
    assert bash_processor.command("cp") == "ERROR: missing file operand\n"
    assert bash_processor.command("cp -r") == "ERROR: missing file operand\n"


def test_cp_error_copy_dir_without_r(bash_processor):
    assert bash_processor.command("cp ls_folder ls_copy") == "ERROR: trying to copy directory without -r\n"


def test_cp_error_permission(bash_processor):
    assert bash_processor.command("cp permitted not_permitted") == "ERROR: permission denied\n"


def test_cp_error_no_file(bash_processor):
    assert bash_processor.command("cp 10.txt 10.copy") == "ERROR: no such file\n"
