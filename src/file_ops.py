from dataclasses import dataclass
from datetime import datetime
import mimetypes
from pathlib import Path
from typing import Iterator
from os.path import getsize


@dataclass
class RealFile:
    """
    Store

    `name`: str

    `path`: str

    `size`: int

    `last_mod`: datetime

    `stat_ino`: str
    """
    name: str
    path: str
    size: int
    last_mod: datetime
    stat_ino: str


@dataclass
class DeviceFiles:
    """
    Store list of files and the unique ID of the device.

    `stat_dev`: str
    
    `files`: list[RealFile]
    """
    stat_dev: str
    files: list[RealFile]


def get_dev_files(path_str) -> DeviceFiles:
    """
    Take a string with Windows' path and return the `DeviceFiles` object
    with all video files in it.
    """
    path: Path = Path(path_str)
    walked: Iterator[tuple[Path, list[str], list[str]]] = Path.walk(path)
    dev_files = DeviceFiles(stat_dev=str(Path(path).stat().st_dev), files=list())
    for root, dirs, files in walked:
        for file in files:
            if (
                "$RECYCLE.BIN" not in str(root)
                and not mimetypes.guess_file_type(file)[0] == None
                and mimetypes.guess_file_type(file)[0].startswith("video")
            ):
                full_path: Path = Path(root, file)
                dev_files.files.append(
                    RealFile(
                        name=file,
                        path=str(root),
                        size=getsize(full_path),
                        last_mod=datetime.fromtimestamp(full_path.stat().st_mtime),
                        stat_ino=str(full_path.stat().st_ino),
                    )
                )
    return dev_files
