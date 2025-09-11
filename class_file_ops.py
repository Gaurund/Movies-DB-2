import datetime
import mimetypes
import os
import pathlib
from shutil import disk_usage


class FileOps:
    def __init__(self, logger) -> None:
        self.log = logger

    def get_st_dev(self, disk_path: str) -> int:
        return pathlib.Path(disk_path).stat().st_dev

    def get_disk_usage(self, disk_path: str) -> dict:
        total, used, free = disk_usage(disk_path)
        disk_data = {"total": total, "used": used, "free": free}
        return disk_data

    def scan_path(self, path: str) -> dict:
        if not os.path.exists(path):
            raise ValueError("The path is invalid.")
        movies = self.walk_dirs(path)
        self.log.logger.info(f"The path '{path}' has scanned")
        return movies

    def walk_dirs(self, init_path: str) -> dict:
        """
        Walks a dir tree and collects files details.
        Returns a dictionary.
        """
        path = pathlib.Path(init_path)  # Have to use a Path object. Not a mere string.
        walked = pathlib.Path.walk(path)

        disk_movies = {}
        disk_movies["st_dev"] = str(self.get_st_dev(init_path))
        disk_movies["movies"] = {}
        disk_movies_key = disk_movies["movies"]
        for root, dirs, files in walked:
            for file in files:
                if (
                    "$RECYCLE.BIN" not in str(root)
                    and not mimetypes.guess_file_type(file)[0] == None
                    and mimetypes.guess_file_type(file)[0].startswith("video")
                ):
                    full_path = pathlib.Path(root, file)
                    disk_movies_key[file] = {
                        "path": root,
                        "size": os.path.getsize(full_path),
                        "last_modified": datetime.datetime.fromtimestamp(
                            full_path.stat().st_mtime
                        ),
                        "st_ino": str(full_path.stat().st_ino),
                    }
        return disk_movies
