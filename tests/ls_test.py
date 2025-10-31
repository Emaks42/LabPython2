def test_base_ls_work(bash_processor):
    assert bash_processor.command("ls ls_folder") == '/data/ls_folder\n0.txt\n1.txt\n2.txt\n'


def test_ls_work_with_multiple_args(bash_processor):
    assert bash_processor.command("ls . ls_folder") == '/data\n0.txt\n1.txt\n2.txt\n3.txt\n4.txt\n5.txt\n6.txt\n7.txt' \
                                                       '\n8.txt\n9.txt\nls_folder\npermitted\n' \
                                                       '/data/ls_folder\n0.txt\n1.txt\n2.txt\n'


def test_ls_without_args_work(bash_processor):
    assert bash_processor.command("ls") == '.\n0.txt\n1.txt\n2.txt\n3.txt\n4.txt\n5.txt\n6.txt\n7.txt' \
                                           '\n8.txt\n9.txt\nls_folder\npermitted\n'


def test_ls_error_is_a_file(bash_processor):
    assert bash_processor.command("ls 0.txt") == "ERROR: not a directory\n"


def test_ls_error_file_not_found(bash_processor):
    assert bash_processor.command("ls nonexistent") == "ERROR: no such file or directory\n"


def test_ls_error_permission_denied(bash_processor):
    assert bash_processor.command("ls permitted") == "ERROR: permission denied\n"
