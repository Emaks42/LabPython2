import pytest
from src.bash_processor import BashProcessor
from pyfakefs.fake_filesystem import FakeFilesystem
import os.path
from os import chmod


@pytest.fixture
def bash_processor(fs: FakeFilesystem):
    fs.create_dir("data")
    for num in range(10):
        fs.create_file(os.path.join("data", f"{num}.txt"), contents=f"{num}")
    fs.create_dir(os.path.join("data", "ls_folder"))
    ls_fold_path = os.path.join("data", "ls_folder")
    for num in range(3):
        fs.create_file(os.path.join(ls_fold_path, f"{num}.txt"), contents=f"{num}")
    fs.create_dir(os.path.join("data", "permitted"))
    perm_dir = os.path.join("data", "permitted")
    fs.create_file(os.path.join(perm_dir, "secret"))
    chmod(perm_dir, 0)
    return BashProcessor("data")
