from dataclasses import dataclass
from datetime import datetime
import mimetypes
from pathlib import Path
from shutil import disk_usage
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
class Device:
    """
    Store a device data.

    `capacity`: int

    `free`: int

    `st_dev`: str
    """

    capacity: int = 0
    free: int = 0
    st_dev: str = ""


@dataclass
class DeviceFiles:
    """
    Store list of files and the device object.

    `device`: Device

    `files`: list[RealFile]
    """

    device: Device
    files: list[RealFile]


def get_dev_files(path_str) -> DeviceFiles:
    """
    Take a string with Windows' path and return the `DeviceFiles` object
    with all video files in it.
    """
    path: Path = Path(path_str)
    walked: Iterator[tuple[Path, list[str], list[str]]] = Path.walk(path)
    total, used, free = disk_usage(path)
    device = Device(capacity=total, free=free, st_dev=str(Path(path).stat().st_dev))
    dev_files = DeviceFiles(device=device, files=[])
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
