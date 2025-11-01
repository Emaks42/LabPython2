import tarfile
from zipfile import ZipFile
from os import getcwd


def zip_func(*args) -> tuple[str, str]:
    ostream = ""
    estream = ""
    if len(args) > 2:
        estream += "ERROR: too many arguments to zip command\n"
    elif len(args) < 2:
        estream += "ERROR: not enough arguments to zip command\n"
    else:
        try:
            folder = args[0]
            archive_path = args[1]
            with ZipFile(str(archive_path), "w") as zf:
                for file in folder.iterdir():
                    zf.write(file, arcname=file.name)
        except FileNotFoundError:
            estream += "ERROR: no such file or directory\n"
        except NotADirectoryError:
            estream += "ERROR: not directory given\n"
        except PermissionError:
            estream += "ERROR: permission denied\n"
    return estream, ostream


def unzip_func(*args) -> tuple[str, str]:
    ostream = ""
    estream = ""
    if len(args) > 1:
        estream += "ERROR: too many arguments to unzip command\n"
    elif len(args) < 1:
        estream += "ERROR: not enough arguments to unzip command\n"
    else:
        try:
            archive_path = args[0]
            with ZipFile(str(archive_path), "r") as zf:
                zf.extractall(getcwd())
        except FileNotFoundError:
            estream += "ERROR: no such file or directory\n"
        except IsADirectoryError:
            estream += "ERROR: given directory, not file\n"
        except PermissionError:
            estream += "ERROR: permission denied\n"
    return estream, ostream


def tar_func(*args) -> tuple[str, str]:
    ostream = ""
    estream = ""
    if len(args) > 2:
        estream += "ERROR: too many arguments to tar command\n"
    elif len(args) < 2:
        estream += "ERROR: not enough arguments to tar command\n"
    else:
        try:
            folder = args[0]
            archive_path = args[1]
            with tarfile.open(str(archive_path), "w:gz") as tar:
                for f in folder.iterdir():
                    tar.add(f, arcname=f.name)
        except FileNotFoundError:
            estream += "ERROR: no such file or directory\n"
        except NotADirectoryError:
            estream += "ERROR: not directory given\n"
        except PermissionError:
            estream += "ERROR: permission denied\n"
    return estream, ostream


def untar_func(*args) -> tuple[str, str]:
    ostream = ""
    estream = ""
    if len(args) > 1:
        estream += "ERROR: too many arguments to untar command\n"
    elif len(args) < 1:
        estream += "ERROR: not enough arguments to untar command\n"
    else:
        try:
            archive_path = args[0]
            with tarfile.open(str(archive_path), "r:gz") as tar:
                tar.extractall(path=getcwd())
        except FileNotFoundError:
            estream += "ERROR: no such file or directory\n"
        except IsADirectoryError:
            estream += "ERROR: given directory, not file\n"
        except PermissionError:
            estream += "ERROR: permission denied\n"
    return estream, ostream
