import os
from pathlib import Path
from typing import List

from picorg import timestamp_finder

FILE_TYPES = [".jpg"]


def rename_files(root: str = ".") -> None:
    """
    Rename all files in the given root directory based on their EXIF timestamp.

    Args:
        root (str): The root directory to start the renaming process from.
        Defaults to the current directory.
    """
    files = _list_files(root)
    for file in files:
        rename_file(file)
    print(f"Processed {len(files)} files.")


def rename_file(file) -> None:
    """
    Rename a single file based on its EXIF timestamp.

    Args:
        file (str): The path to the file to rename.
    """
    exif_name = timestamp_finder.get_timestamp(file)
    if exif_name is None:
        _handle_no_exif_found(file)
    else:
        new_filename = find_new_filename(file, exif_name)
        if new_filename != file:
            os.rename(file, new_filename)


def _list_files(root: str) -> List[Path]:
    """
    List all files of the given types in the given root directory.

    Args:
        root (str): The root directory to start the search from.

    Returns:
        List[Path]: A list of paths to the files found.
    """
    result = []
    for filename in Path(root).glob("**/*"):
        if filename.suffix.lower() in FILE_TYPES:
            result.append(Path(filename))
    return result


def find_new_filename(file: str, exif_name: str) -> str:
    """
    Generate a new filename for a file based on its EXIF timestamp.

    Args:
        file (str): The path to the file to rename.
        exif_name (str): The EXIF timestamp of the file.

    Returns:
        str: The new filename for the file.
    """
    filepath = Path(file)
    if filepath.name.startswith(exif_name):
        return file
    suggested_path = Path(filepath.parent, exif_name + filepath.suffix.lower())
    if not suggested_path.is_file():
        return str(suggested_path)
    for suffix in range(1, 10**5):
        suggested_path = suggested_path.with_name(
            f"{exif_name}({str(suffix)}){filepath.suffix.lower()}"
        )

        if not suggested_path.is_file():
            return str(suggested_path)
    raise RuntimeError("This should never happen...")


def _handle_no_exif_found(file: str) -> None:
    """
    Handle a file that does not have an EXIF timestamp.

    Args:
        file (str): The path to the file without an EXIF timestamp.
    """
    filepath = Path(file)
    if filepath.parent.name == "NOK":
        return
    new_filepath = Path(filepath.parent, "NOK", filepath.name)
    new_filepath.parent.mkdir(exist_ok=True)
    filepath.rename(new_filepath)
    print(f"File NOK: {file}")


if __name__ == "__main__":
    rename_files()
