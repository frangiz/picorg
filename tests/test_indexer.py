from pathlib import Path
from py.path import local
from PIL import Image
import piexif
from piexif import ExifIFD

from picorg.indexer import index_files
from picorg.cache import PicorgCache
from datetime import datetime

from unittest.mock import patch


def assert_date_format(date: str):
    try:
        datetime.strptime(date, '%Y:%m:%d %H:%M:%S')
    except ValueError:
        raise AssertionError("date is not in the correct format")


def create_jpg_file(filepath: Path, size: int, date: str, skipExifData = False) -> None:
    if date == "now":
        created = datetime.now().strftime("%Y:%m:%d %H:%M:%S")
    else:
        assert_date_format(date)
        created = date
    img = Image.new('RGB', (size, size))
    img.save(filepath, format='JPEG')

    if skipExifData:
        return
    exif_dict = {
        "0th": {},
        "Exif": {ExifIFD.DateTimeOriginal: created},
        "GPS": {},
        "1st": {},
        "thumbnail": None,
    }
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, filepath)


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


def test_index_files_will_not_add_files_with_no_exif_data_to_cache(tmpdir: local):
    # arrange
    jpg_file = tmpdir.join("test.jpg")
    create_jpg_file(str(jpg_file), 2, "now", skipExifData=True)

    # act
    with patch('builtins.print') as mock_print:
        index_files(Path(tmpdir))
    
    # assert
    cache = PicorgCache.load(tmpdir)
    assert len(cache.cached_images) == 0
    mock_print.assert_called_with(f"Skipping {jpg_file} because it has no exif data")


def test_index_files_will_not_add_files_with_no_exif_date_to_cache(tmpdir: local):
    # arrange
    jpg_file = tmpdir.join("test.jpg")
    create_jpg_file(str(jpg_file), 2, "now")
    exif_dict = piexif.load(str(jpg_file))
    del exif_dict["Exif"][ExifIFD.DateTimeOriginal]
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, str(jpg_file))

    # act
    with patch('builtins.print') as mock_print:
        index_files(Path(tmpdir))
    
    # assert
    cache = PicorgCache.load(tmpdir)
    assert len(cache.cached_images) == 0
    mock_print.assert_called_with(f"Skipping {jpg_file} because it has no exif data")

def test_index_files_will_not_add_files_with_invalid_exif_date_to_cache(tmpdir: local):
    # arrange
    jpg_file = tmpdir.join("test.jpg")
    create_jpg_file(str(jpg_file), 2, "now")
    exif_dict = piexif.load(str(jpg_file))
    exif_dict["Exif"][ExifIFD.DateTimeOriginal] = "2024_01_20 22_10_00"
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, str(jpg_file))

    # act
    with patch('builtins.print') as mock_print:
        index_files(Path(tmpdir))
    
    # assert
    cache = PicorgCache.load(tmpdir)
    assert len(cache.cached_images) == 0
    mock_print.assert_called_with(f"Skipping {jpg_file} because it has no exif data")