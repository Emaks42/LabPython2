from src.bash_processor import BashProcessor


def test_base_zip_and_unzip_work(tmp_path):
    bash_processor = BashProcessor(str(tmp_path))
    (tmp_path / "folder").mkdir()
    (tmp_path / "folder_2").mkdir()
    zipper = (tmp_path / "folder_2" / "zipper").open("w")
    zipper.write("t")
    assert bash_processor.command("zip folder_2 f2.zip") == ""
    assert bash_processor.command("unzip f2.zip") == ""
    assert bash_processor.command("ls") == '.\nf2.zip\nfolder\nfolder_2\nzipper\n'


def test_error_zip_unzip_permission(bash_processor):
    assert bash_processor.command("zip permitted permit.zip") == "ERROR: permission denied\n"
    assert bash_processor.command("unzip permitted/secret") == "ERROR: permission denied\n"


def test_error_zip_not_enough_args(bash_processor):
    assert bash_processor.command("zip") == "ERROR: not enough arguments to zip command\n"


def test_error_zip_too_many_args(bash_processor):
    assert bash_processor.command("zip arg1 arg2 arg3++") == "ERROR: too many arguments to zip command\n"


def test_error_unzip_not_enough_args(bash_processor):
    assert bash_processor.command("unzip") == "ERROR: not enough arguments to unzip command\n"


def test_error_unzip_too_many_args(bash_processor):
    assert bash_processor.command("unzip arg1 arg2 arg3++") == "ERROR: too many arguments to unzip command\n"


def test_error_zip_and_unzip_nonexistent_file(bash_processor):
    assert bash_processor.command("zip nonex no.zip") == "ERROR: no such file or directory\n"
    assert bash_processor.command("unzip nonex") == "ERROR: no such file or directory\n"


def test_error_unzip_given_dir(bash_processor):
    assert bash_processor.command("unzip ls_folder") == "ERROR: given directory, not file\n"


def test_error_zip_given_file(bash_processor):
    assert bash_processor.command("zip 0.txt 0.txt") == "ERROR: not directory given\n"
