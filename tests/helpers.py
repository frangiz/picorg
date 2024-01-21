from datetime import datetime

import piexif
from piexif import ExifIFD
from PIL import Image


def assert_date_format(date: str):
    try:
        datetime.strptime(date, "%Y:%m:%d %H:%M:%S")
    except ValueError:
        raise AssertionError("date is not in the correct format")


def create_jpg_file(filepath: str, size: int, date: str, skipExifData=False) -> None:
    if date == "now":
        created = datetime.now().strftime("%Y:%m:%d %H:%M:%S")
    else:
        assert_date_format(date)
        created = date
    img = Image.new("RGB", (size, size))
    img.save(filepath, format="JPEG")

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
