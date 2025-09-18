from dataclasses import dataclass
from datetime import datetime
import mimetypes
from pathlib import Path
from typing import Iterator
from os.path import getsize


@dataclass
class File:
    name: str
    path: str
    size: int
    last_mod: datetime
    stat_ino: str


@dataclass
class DeviceFiles:
    stat_dev: str
    files: list[File]


class StoreFile:
    def store(self, root, file):
        full_path: Path = Path(root, file)
        return File(
            name=file,
            path=str(root),
            size=getsize(full_path),
            last_mod=datetime.fromtimestamp(full_path.stat().st_mtime),
            stat_ino=str(full_path.stat().st_ino),
        )


class StoreDevFiles:
    def store(self, path, walked):
        disk_files = DeviceFiles(stat_dev=str(Path(path).stat().st_dev), files=list())
        for root, dirs, files in walked:
            for file in files:
                if (
                    "$RECYCLE.BIN" not in str(root)
                    and not mimetypes.guess_file_type(file)[0] == None
                    and mimetypes.guess_file_type(file)[0].startswith("video")
                ):
                    disk_files.files.append(
                        StoreFile.store(StoreFile(), root=root, file=file)
                    )
        return disk_files


class ScanDev:
    def walk_dirs(self, init_path: str):
        path: Path = Path(init_path)
        walked: Iterator[tuple[Path, list[str], list[str]]] = Path.walk(path)
        disk_files = StoreDevFiles.store(StoreDevFiles(), path=path, walked=walked)
        return disk_files


if __name__ == "__main__":
    ScanDev.walk_dirs(ScanDev(), "d:/temp/Странный видео диск/")
    print("Смотрим")
