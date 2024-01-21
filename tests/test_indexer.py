from pathlib import Path

from helpers import create_jpg_file
from py.path import local

from picorg.cache import PicorgCache
from picorg.indexer import index_files


def test_index_files_will_add_found_files_to_cache(tmpdir: local):
    # arrange
    jpg_file = tmpdir.join("test.jpg")
    create_jpg_file(str(jpg_file), 2, "2024:01:20 22:10:00")

    tmpdir.mkdir("subfolder1")
    jpg_file_2 = tmpdir.join("subfolder1", "test2.jpg")
    create_jpg_file(str(jpg_file_2), 2, "now")

    # act
    index_files(Path(tmpdir))

    # assert
    cache = PicorgCache.load(tmpdir)
    assert len(cache.cached_images) == 2
    assert cache.file_in_cache(jpg_file)
    assert cache.file_in_cache(jpg_file_2)


def test_index_files_will_not_add_already_indexed_files_to_cache(tmpdir: local):
    # arrange
    jpg_file = tmpdir.join("test.jpg")
    create_jpg_file(str(jpg_file), 2, "2024:01:20 22:10:00")

    # act
    index_files(Path(tmpdir))
    index_files(Path(tmpdir))

    # assert
    cache = PicorgCache.load(tmpdir)
    assert len(cache.cached_images) == 1
    assert cache.file_in_cache(jpg_file)
