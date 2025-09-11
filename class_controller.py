class Controller:

    def __init__(self, db_ops, file_ops, logger) -> None:
        self.log = logger
        self.db_ops = db_ops
        self.file_ops = file_ops

    def check_disk(self, path) -> bool:
        st_dev: int = self.file_ops.get_st_dev(path)
        disk_id: int = self.db_ops.check_disk(str(st_dev))
        if disk_id == None:
            return False
        return True

    def store_movies_from_path(self, path) -> None:
        """
        Accepts a path to scan.
        At this point all checking for the disk data in DB must be done.
        Updates the disk usage information in DB.
        Inserts files in DB.
        """
        disk_free_space: int = self.file_ops.get_disk_usage(path)["free"]
        movies: dict = self.scan_path(path)
        st_dev = movies["st_dev"]
        self.db_ops.update_disk_usage(st_dev=st_dev, free=disk_free_space)
        self.db_ops.insert_from_disk(movies)

    def scan_path(self, path) -> dict:
        movies: dict = self.file_ops.scan_path(path)
        if not movies["movies"]:
            self.log.logger.warning("The path has no movies.")
            raise ValueError("The path has no movies.")
        return movies

    def insert_disk(self, path: str, disk_name: str) -> None:
        disk_data: dict = self.file_ops.get_disk_usage(path)
        st_dev = str(self.file_ops.get_st_dev(path))
        self.db_ops.insert_disk(
            st_dev=st_dev,
            disk_name=disk_name,
            capacity=disk_data["total"],
            free_space=disk_data["free"],
        )

    def get_db_files(self) -> dict:
        files: dict = self.db_ops.get_db_files()
        return files