from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from db_classes import Base, Disk, File, Movie


class DbOps:
    def __init__(self, engine, logger) -> None:
        self.log = logger
        self.engine = create_engine(engine)
        Base.metadata.create_all(self.engine)

    def check_disk(self, st_dev: str) -> int | None:
        """
        Checking is the device already in DB
        and return device's id or None.
        """
        with Session(self.engine) as session:
            disk_id = session.scalars(
                select(Disk.id).where(Disk.st_dev == st_dev)
            ).one_or_none()
        return disk_id

    def insert_disk(
        self, st_dev: str, disk_name: str, capacity: int, free_space: int
    ) -> None:
        """
        Insert device values in DB.
        """
        with Session(self.engine) as session:
            session.add(
                Disk(
                    disk_name=disk_name,
                    disk_capacity=capacity,
                    disk_free=free_space,
                    st_dev=st_dev,
                )
            )
            session.commit()

    def update_disk_usage(self, st_dev, free) -> None:
        with Session(self.engine) as session:
            disk = session.scalars(select(Disk).where(Disk.st_dev == st_dev)).one()
            disk.disk_free = free
            session.commit()

    def insert_from_disk(self, files: dict) -> None:
        """
        Accepts a dictionary, checks if a file is already in DB.
        If it is not then write it in DB.
        """

        with Session(self.engine) as session:
            st_dev: str = files["st_dev"]
            disk_id: int = session.scalars(
                select(Disk.id).where(Disk.st_dev == st_dev)
            ).one()

            for file in files["movies"]:
                db_file = session.scalar(
                    select(File).where(File.st_ino == files["movies"][file]["st_ino"])
                )
                if db_file is None:
                    session.add(
                        File(
                            file_name=file,
                            disk_path=str(files["movies"][file]["path"]),
                            size=files["movies"][file]["size"],
                            disk_id=disk_id,
                            last_modified=files["movies"][file]["last_modified"],
                            st_ino=files["movies"][file]["st_ino"],
                        )
                    )
                else:
                    if not db_file.disk_path == str(files["movies"][file]["path"]):
                        db_file.disk_path = str(files["movies"][file]["path"])
                    if not db_file.file_name == file:
                        db_file.file_name = file

            session.commit()

    def get_db_files(self) -> dict:
        files = {}
        with Session(self.engine) as session:
            db_files = session.scalars(
                select(File).where(File.movie_id == None)
            ).all()

            # for disk in db_files:
            #     files[disk.id] = {
            #         "disk_name": disk.disk_name,
            #         "disk_image": disk.disk_image,
            #         "disk_capacity": disk.disk_capacity,
            #         "disk_free": disk.disk_free,
            #         "st_dev": disk.st_dev,
            #         "files": {},
            #     }

            #     for f in disk.files:
            #         files[disk.id]["files"][f.id] = {
            #             "file_name": f.file_name,
            #             "disk_path": f.disk_path,
            #             "st_ino": f.st_ino,
            #             "last_modified": f.last_modified,
            #             "size": f.size,
            #         }
            # session.commit()
        return files

    # def delete_dev(st_dev: str) -> None:
    #     """
    #     Удаление устройства из БД.
    #     """

    # def check_file(st_ino: str) -> bool:
    #     """
    #     Проверка, есть ли файл в БД.
    #     Возможно не понадобится.
    #     """
    #     return True

    # def get_file_by_st_ino(st_ino: str):
    #     """
    #     Запрашивает из БД файл по полю индентификатора.
    #     """
    #     return ""

    # def get_file_by_id(id: int):
    #     """
    #     Запрашивает данные о файле по ID.
    #     Возвращает объединённые данные
    # """
