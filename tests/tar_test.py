from src.bash_processor import BashProcessor


def test_base_tar_and_untar_work(tmp_path):
    bash_processor = BashProcessor(str(tmp_path))
    (tmp_path / "folder").mkdir()
    (tmp_path / "folder_2").mkdir()
    tarper = (tmp_path / "folder_2" / "tarper").open("w")
    tarper.write("t")
    assert bash_processor.command("tar folder_2 f2.tar") == ""
    assert bash_processor.command("untar f2.tar") == ""
    assert bash_processor.command("ls") == '.\nf2.tar\nfolder\nfolder_2\ntarper\n'


def test_error_tar_untar_permission(bash_processor):
    assert bash_processor.command("tar permitted permit.tar") == "ERROR: permission denied\n"
    assert bash_processor.command("untar permitted/secret") == "ERROR: permission denied\n"


def test_error_tar_not_enough_args(bash_processor):
    assert bash_processor.command("tar") == "ERROR: not enough arguments to tar command\n"


def test_error_tar_too_many_args(bash_processor):
    assert bash_processor.command("tar arg1 arg2 arg3++") == "ERROR: too many arguments to tar command\n"


def test_error_untar_not_enough_args(bash_processor):
    assert bash_processor.command("untar") == "ERROR: not enough arguments to untar command\n"


def test_error_untar_too_many_args(bash_processor):
    assert bash_processor.command("untar arg1 arg2 arg3++") == "ERROR: too many arguments to untar command\n"


def test_error_tar_and_untar_nonexistent_file(bash_processor):
    assert bash_processor.command("tar nonex no.tar") == "ERROR: no such file or directory\n"
    assert bash_processor.command("untar nonex") == "ERROR: no such file or directory\n"


def test_error_untar_given_dir(bash_processor):
    assert bash_processor.command("untar ls_folder") == "ERROR: given directory, not file\n"


def test_error_tar_given_file(bash_processor):
    assert bash_processor.command("tar 0.txt 0.txt") == "ERROR: not directory given\n"
