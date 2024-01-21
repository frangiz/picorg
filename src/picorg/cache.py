from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, Dict, Optional

from pydantic import BaseModel


@dataclass
class CachedImage:
    filepath: Path
    name: str
    exif_name: Optional[str]
    checksum: str


class PicorgCache(BaseModel):
    _self_root = Path(".")
    self_filename: ClassVar = ".picorg_cache"
    cached_images: Dict[str, CachedImage] = {}

    def add_file(self, file: CachedImage) -> None:
        self.cached_images[str(file.filepath)] = file

    def file_in_cache(self, path: Path) -> bool:
        return str(path) in self.cached_images

    @staticmethod
    def load(root: Path) -> "PicorgCache":
        if Path(root, PicorgCache.self_filename).exists():
            with open(Path(root, PicorgCache.self_filename), "r") as f:
                json_data = f.read()
            cache = PicorgCache.model_validate_json(json_data)
        else:
            cache = PicorgCache()
        cache._self_root = root
        return cache

    def save(self) -> None:
        with open(Path(self._self_root, self.self_filename), "w") as f:
            f.write(self.model_dump_json(indent=4))
