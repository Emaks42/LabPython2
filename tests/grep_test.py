def test_grep_base_work(bash_processor):
    assert bash_processor.command("grep '0' 0.txt") == "1: 0\n"


def test_grep_dir_work(bash_processor):
    assert bash_processor.command("grep -r [0-9] .") == ('ERROR: permission denied\n'
                                                            '/data/0.txt 1: 0\n'
                                                            '/data/1.txt 1: 1\n'
                                                            '/data/2.txt 1: 2\n'
                                                            '/data/3.txt 1: 3\n'
                                                            '/data/4.txt 1: 4\n'
                                                            '/data/5.txt 1: 5\n'
                                                            '/data/6.txt 1: 6\n'
                                                            '/data/7.txt 1: 7\n'
                                                            '/data/8.txt 1: 8\n'
                                                            '/data/9.txt 1: 9\n'
                                                            '/data/ls_folder/0.txt 1: 0\n'
                                                            '/data/ls_folder/1.txt 1: 1\n'
                                                            '/data/ls_folder/2.txt 1: 2\n')


def test_grep_i_option(bash_processor):
    assert bash_processor.command("grep -r -i [0-9] .") == ('ERROR: permission denied\n'
                                                         '/data/0.txt 1: 0\n'
                                                         '/data/1.txt 1: 1\n'
                                                         '/data/2.txt 1: 2\n'
                                                         '/data/3.txt 1: 3\n'
                                                         '/data/4.txt 1: 4\n'
                                                         '/data/5.txt 1: 5\n'
                                                         '/data/6.txt 1: 6\n'
                                                         '/data/7.txt 1: 7\n'
                                                         '/data/8.txt 1: 8\n'
                                                         '/data/9.txt 1: 9\n'
                                                         '/data/ls_folder/0.txt 1: 0\n'
                                                         '/data/ls_folder/1.txt 1: 1\n'
                                                         '/data/ls_folder/2.txt 1: 2\n')
    assert bash_processor.command("grep -i '0' 0.txt") == "1: 0\n"


def test_grep_error_not_enough_args(bash_processor):
    assert bash_processor.command("grep") == "ERROR: missing pattern operand\n"
    assert bash_processor.command("grep b") == "ERROR: not specified file or directory to search\n"


def test_grep_error_permission(bash_processor):
    assert bash_processor.command("grep 'something interesting' permitted/secret") == "ERROR: permission denied\n"
    assert bash_processor.command("grep -r 'something interesting' permitted") == "ERROR: permission denied\n"


def test_grep_error_search_in_dir_without(bash_processor):
    assert bash_processor.command("grep 'f' ls_folder") == "ERROR: trying to search in directory without -r\n"


def test_grep_error_nonexistent(bash_processor):
    assert bash_processor.command("grep f nonex") == "ERROR: no such file or directory\n"


def test_grep_error_too_many_args(bash_processor):
    assert bash_processor.command("grep arg1 arg2 arg3") == "ERROR: too many arguments to grep command\n"


def test_grep_error_encoding(bash_processor):
    bash_processor.command("zip ls_folder ls_folder.zip")
    path = "/data/ls_folder.zip"
    assert bash_processor.command("grep -r [0-9] .") == ('ERROR: permission denied\n'
                                                         f"ERROR: incorrect file format in file {path}\n"
                                                            '/data/0.txt 1: 0\n'
                                                            '/data/1.txt 1: 1\n'
                                                            '/data/2.txt 1: 2\n'
                                                            '/data/3.txt 1: 3\n'
                                                            '/data/4.txt 1: 4\n'
                                                            '/data/5.txt 1: 5\n'
                                                            '/data/6.txt 1: 6\n'
                                                            '/data/7.txt 1: 7\n'
                                                            '/data/8.txt 1: 8\n'
                                                            '/data/9.txt 1: 9\n'
                                                            '/data/ls_folder/0.txt 1: 0\n'
                                                            '/data/ls_folder/1.txt 1: 1\n'
                                                            '/data/ls_folder/2.txt 1: 2\n')
    assert bash_processor.command("grep '0' ls_folder.zip") == "ERROR: incorrect file format\n"
