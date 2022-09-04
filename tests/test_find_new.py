import os
import pathlib
import shutil

from src import find_new
from tests import test_base

TEST_DIR = pathlib.Path()
PREV_WORKING_DIR = ""

PIC_PATH_1 = pathlib.Path()


def setup_module(module):
    test_base.setup_module(module)


def setup_function(function):
    global TEST_DIR
    TEST_DIR = test_base.get_test_folder(function.__name__)
    TEST_DIR.mkdir(parents=True)
    global PREV_WORKING_DIR
    PREV_WORKING_DIR = os.getcwd()
    os.chdir(TEST_DIR)

    global PIC_PATH_1
    PIC_PATH_1 = pathlib.Path("pick_path_1")
    PIC_PATH_1.mkdir()
    PIC_PATH_1 = PIC_PATH_1.absolute()


def teardown_function(function):
    os.chdir(PREV_WORKING_DIR)


def test_find_new_finds_a_new_file_if_name_is_unique(mocker):
    pathlib.Path(PIC_PATH_1, "20220916_000001.jpg").write_bytes(b"Some bytes here")

    pathlib.Path("work_dir").mkdir()
    os.chdir("work_dir")
    unique_img = pathlib.Path("20220916_000002.jpg")
    unique_img.write_bytes(b"Some different bytes here")
    mocker.patch("timestamp_finder.get_timestamp", return_value="20220916_000002")

    res = find_new.find_new(pic_paths=[PIC_PATH_1])

    assert res[0] == unique_img
    assert list(pathlib.Path("new_images").glob("**/*"))[0].name == unique_img.name


def test_find_new_finds_a_new_file_that_already_exists_with_same_content_and_exif_name(
    mocker,
):
    duplicated_image = pathlib.Path(PIC_PATH_1, "20220916_000001.jpg")
    duplicated_image.write_bytes(b"Some bytes here")

    pathlib.Path("work_dir").mkdir()
    shutil.copy2(duplicated_image, "work_dir")
    pathlib.Path("work_dir", duplicated_image.name).rename("pic1.jpg")
    os.chdir("work_dir")
    mocker.patch("timestamp_finder.get_timestamp", return_value="20220916_000001")

    res = find_new.find_new(pic_paths=[PIC_PATH_1])

    assert not len(res)
    assert not pathlib.Path("new_images").exists()


def test_find_new_does_not_find_a_new_file_if_name_and_size_in_cache():
    pathlib.Path("work_dir").mkdir()
    os.chdir("work_dir")
    cached_img = pathlib.Path("20220916_000001.jpg")
    cached_img.write_bytes(b"Some different bytes here")

    cache = find_new.LocalCache().load()
    cache.ignore_file(cached_img)
    cache.save()

    res = find_new.find_new(pic_paths=[PIC_PATH_1])

    assert not len(res)
    assert not pathlib.Path("new_images").exists()


def test_find_new_finds_a_new_file_if_only_name_in_cache(mocker):
    pathlib.Path("work_dir").mkdir()
    os.chdir("work_dir")
    not_cached_img = pathlib.Path("20220916_000001.jpg")
    not_cached_img.write_bytes(b"Some different bytes here")

    cache = find_new.LocalCache().load()
    cache.ignore_file(not_cached_img)
    cache.save()
    not_cached_img.write_bytes(b"Some other bytes here with different size")

    mocker.patch("timestamp_finder.get_timestamp", return_value="20220916_000001")

    res = find_new.find_new(pic_paths=[PIC_PATH_1])

    assert res[0] == not_cached_img
    assert list(pathlib.Path("new_images").glob("**/*"))[0].name == not_cached_img.name


# TODO:
# test name exists, but different contents
