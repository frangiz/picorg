import shutil
import pathlib
from os import path, makedirs

import duplicates
import settings

BASE_PATH = "tests/test_data"
# Will be set to BASE_PATH/tmp2/<test_name>
TEST_DIR = ""


def setup_module(module):
    if path.exists(path.join(BASE_PATH, "tmp2")):
        shutil.rmtree(path.join(BASE_PATH, "tmp2"))


def setup_function(function):
    print("setup_function")
    global TEST_DIR
    TEST_DIR = path.join(BASE_PATH, "tmp2", function.__name__)
    makedirs(TEST_DIR)


def test_find_duplicates_one_root():
    pathlib.Path(TEST_DIR, "pic1.jpg").touch()
    pathlib.Path(TEST_DIR, "pic2.jpg").touch()
    pathlib.Path(TEST_DIR, "subfolder1").mkdir()
    pathlib.Path(TEST_DIR, "subfolder1", "pic1.png").touch()
    pathlib.Path(TEST_DIR, "subfolder1", "pic2.jpg").touch()

    settings.SETTINGS_DIR = pathlib.Path(TEST_DIR, ".picorg")
    settings.get("pic_paths", [str(pathlib.Path(TEST_DIR))])

    result = duplicates.find_duplicates()

    expected = {
        "pic2.jpg": [
            path.join(TEST_DIR, "pic2.jpg"),
            path.join(TEST_DIR, "subfolder1", "pic2.jpg"),
        ]
    }
    assert len(result) == len(expected)
    assert sorted(result) == sorted(expected)


def test_find_duplicates_multiple_roots():
    pathlib.Path(TEST_DIR, "root1").mkdir()
    pathlib.Path(TEST_DIR, "root1", "pic1.jpg").touch()
    pathlib.Path(TEST_DIR, "root1", "pic2.jpg").touch()
    pathlib.Path(TEST_DIR, "root1", "subfolder1").mkdir()
    pathlib.Path(TEST_DIR, "root1", "subfolder1", "pic1.png").touch()
    pathlib.Path(TEST_DIR, "root1", "subfolder1", "pic2.jpg").touch()

    pathlib.Path(TEST_DIR, "root2").mkdir()
    pathlib.Path(TEST_DIR, "root2", "pic2.jpg").touch()
    pathlib.Path(TEST_DIR, "root2", "subfolder1").mkdir()
    pathlib.Path(TEST_DIR, "root2", "subfolder1", "pic1.jpg").touch()
    pathlib.Path(TEST_DIR, "root2", "subfolder1", "pic1.png").touch()

    settings.SETTINGS_DIR = pathlib.Path(TEST_DIR, ".picorg")
    settings.get("pic_paths", [str(pathlib.Path(TEST_DIR))])

    result = duplicates.find_duplicates()

    print(result)
    expected = {
        "pic1.jpg": [
            path.join(TEST_DIR, "root1", "pic1.jpg"),
            path.join(TEST_DIR, "root2", "subfolder1", "pic1.jpg"),
        ],
        "pic2.jpg": [
            path.join(TEST_DIR, "root1", "pic2.jpg"),
            path.join(TEST_DIR, "root1", "subfolder1", "pic2.jpg"),
            path.join(TEST_DIR, "root2", "pic2.jpg"),
        ],
    }
    assert len(result) == len(expected)
    assert sorted(result) == sorted(expected)
