import hashlib
from pathlib import Path

from picorg.cache import CachedImage, PicorgCache
from picorg.timestamp_finder import get_timestamp


def create_unique_id(image_path):
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    return hashlib.sha256(image_data).hexdigest()


""" def create_unique_id(image_path):
    # Get the image's last modification time
    mod_time = os.path.getmtime(image_path)
    # Get the image's creation time
    create_time = os.path.getctime(image_path)
    # Create a string with the image's name, modification time, and creation time
    image_info = f"{os.path.basename(image_path)}{mod_time}{create_time}"
    # Return a hash of the image info
    return hashlib.sha256(image_info.encode()).hexdigest() """


def index_files(root: Path = Path()) -> None:
    """
    Index all .jpg files in the given root directory and its subdirectories.
    """
    cache = PicorgCache.load(root)
    for path in root.glob("**/*.jpg"):
        exif_name = get_timestamp(path)
        cache.add_file(
            CachedImage(
                filepath=path,
                name=path.name,
                exif_name=exif_name,
                checksum=create_unique_id(path),
            )
        )
    cache.save()
