from dataclasses import dataclass
from datetime import datetime
import mimetypes
from pathlib import Path
from typing import Iterator
from os.path import getsize


@dataclass
class RealFile:
    name: str
    path: str
    size: int
    last_mod: datetime
    stat_ino: str


@dataclass
class DeviceFiles:
    stat_dev: str
    files: list[RealFile]


class StoreFile:
    def __init__(self, root, file) -> None:
        self.root = root
        self.file = file

    def store(self) -> RealFile:
        full_path: Path = Path(self.root, self.file)
        return RealFile(
            name=self.file,
            path=str(self.root),
            size=getsize(full_path),
            last_mod=datetime.fromtimestamp(full_path.stat().st_mtime),
            stat_ino=str(full_path.stat().st_ino),
        )


class StoreDevFiles:
    def __init__(self, path, walked) -> None:
        self.path = path
        self.walked = walked

    def store(self) -> DeviceFiles:
        disk_files = DeviceFiles(
            stat_dev=str(Path(self.path).stat().st_dev), files=list()
        )
        for root, dirs, files in self.walked:
            for file in files:
                if (
                    "$RECYCLE.BIN" not in str(root)
                    and not mimetypes.guess_file_type(file)[0] == None
                    and mimetypes.guess_file_type(file)[0].startswith("video")
                ):
                    store_file = StoreFile(root=root, file=file)
                    disk_files.files.append(store_file.store())
        return disk_files


class ScanDev:
    def __init__(self, init_path: str) -> None:
        self.path: Path = Path(init_path)

    def walk_dirs(self) -> DeviceFiles:
        walked: Iterator[tuple[Path, list[str], list[str]]] = Path.walk(self.path)
        store_dev_files = StoreDevFiles(path=self.path, walked=walked)
        disk_files = store_dev_files.store()
        return disk_files
    
    
