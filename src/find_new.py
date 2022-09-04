import filecmp
import itertools
import json
from pathlib import Path
from shutil import copy2
from typing import ClassVar, Dict, List

from pydantic import BaseModel

import timestamp_finder
from rename import _find_new_filename


class IgnoredFile(BaseModel):
    filesize: int


class LocalCache(BaseModel):
    self_filename: ClassVar = ".picorg_cache"
    ignored_files: Dict[str, IgnoredFile] = {}

    def file_in_cache(self, path: Path) -> bool:
        return (
            path.name in self.ignored_files
            and self.ignored_files[path.name].filesize == path.stat().st_size
        )

    def ignore_file(self, path: Path):
        self.ignored_files[path.name] = IgnoredFile(filesize=path.stat().st_size)

    @staticmethod
    def load() -> "LocalCache":
        return (
            LocalCache.parse_file(LocalCache.self_filename)
            if Path(LocalCache.self_filename).exists()
            else LocalCache()
        )

    def save(self) -> None:
        with open(self.self_filename, "w") as f:
            f.write(json.dumps(self.dict(), sort_keys=True, indent=4))


def find_new(pic_paths: List[Path]) -> List[Path]:
    extensions = [".jpg"]
    local_cache: LocalCache = LocalCache.load()

    new_img_candidates: Dict[str, Path] = {}
    for file_ext in extensions:
        for candidate in Path().glob(f"*{file_ext}"):
            if local_cache.file_in_cache(candidate):
                continue
            exif_name = timestamp_finder.get_timestamp(candidate)
            new_img_candidates[_find_new_filename(candidate, exif_name)] = candidate

    for path, file_ext in itertools.product(pic_paths, extensions):
        for filepath in path.glob(f"**/*{file_ext}"):
            if filepath.name not in new_img_candidates:
                continue
            busted_candidate = new_img_candidates[filepath.name]
            if filecmp.cmp(busted_candidate, filepath, shallow=False):
                local_cache.ignore_file(busted_candidate)
                del new_img_candidates[filepath.name]
            else:
                # TODO: handle this case where filename matches but not the
                # file contents.
                # copy to undecided folder?
                print(
                    f"Same filename, different size {filepath.absolute()}"
                    f" and {busted_candidate.absolute()}"
                )
    local_cache.save()

    if not new_img_candidates:
        print("No new images.")
    else:
        Path("new_images").mkdir(exist_ok=True)
        print("New images:")
        for new_img in new_img_candidates:
            copy2(new_img, "new_images/")
    return list(new_img_candidates.values())
