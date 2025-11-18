from dataclasses import dataclass
from datetime import time
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from src.db_classes import Base, Disk, File, Movie
from src.file_ops import Device, DeviceFiles, RealFile


@dataclass
class DBDev:
    id: int
    name: str
    image: str
    capacity: int
    free_space: int
    st_dev: str


@dataclass
class DBMovie:
    id: int
    name_original: str
    name_russian: str
    duration: time
    premiere_date: str
    imdb_link: str
    description: str
    is_active: bool
    files: list
    type_id: int
    movie_type: str
    franchise_id: int
    franchise: str
    franchise_part: int


class RetrieveDBDev:
    def __init__(self, disk) -> None:
        self.disk = disk

    def retrieve(self):
        return DBDev(
            id=self.disk.id,
            name=self.disk.disk_name,
            image=self.disk.disk_image,
            capacity=self.disk.disk_capacity,
            free_space=self.disk.disk_free,
            st_dev=self.disk.st_dev,
        )


class DB_connection:
    def __init__(self, engine: str) -> None:
        self.engine = create_engine(engine)
        Base.metadata.create_all(self.engine)

    def get_disk_by_stat(self, st_dev: str) -> int | None:
        """
        Checks if the device already exists in the database
        and returns the device ID or None.
        """
        with Session(self.engine) as session:
            disk_id = session.scalars(
                select(Disk.id).where(Disk.st_dev == st_dev)
            ).one_or_none()
        return disk_id

    def get_disk_by_name(self, name: str) -> int | None:
        with Session(self.engine) as session:
            disk_id = session.scalars(
                select(Disk.id).where(Disk.disk_name == name)
            ).one_or_none()
        return disk_id

    def get_empties(self):
        with Session(self.engine) as session:
            empties = session.scalars(select(File).where(File.movie_id == None)).all()
        return empties

    def get_all_movies(self):
        with Session(self.engine) as session:
            movies = session.scalars(select(Movie)).all()
        return movies

    def get_all_files(self):
        with Session(self.engine) as session:
            files = session.scalars(select(File)).all()
        return files

    def get_all_disks(self):
        with Session(self.engine) as session:
            disks = session.scalars(select(Disk)).all()
        return disks

    def collect_tree_data(self):
        tree_data = {}
        with Session(self.engine) as session:
            disks = session.scalars(select(Disk)).all()

            for d in disks:
                tree_data[d.disk_name] = []
                files = session.scalars(select(File).where(Disk.id == d.id)).all()
                for f in files:
                    if f.movie_id is None:
                        tree_data[d.disk_name].append(f.file_name)
                    else:
                        movie = session.scalars(select(Movie).where(Movie.id == f.movie_id)).one()
                        if movie.name_russian is not None:
                            movie_name = movie.name_russian
                        else:
                            movie_name = movie.name_original
                        if movie_name not in tree_data[d.disk_name]:
                            tree_data[d.disk_name].append(f"{movie_name} - название фильма")

        return tree_data

    def is_dev_name_exists(self, name: str) -> bool:
        return self.get_disk_by_name(name) is not None

    # def get_disks(self) -> list:
    #     """
    #     Return dictionary of storage devices.
    #     """
    #     disks = list()
    #     with Session(self.engine) as session:
    #         db_disks = session.scalars(select(Disk)).all()
    #         for d in db_disks:
    #             getter = RetrieveDBDev(d)
    #             disks.append(getter.retrieve())
    #     return disks

    ###################
    # Insert operations
    ###################
    def insert_disk(self, name: str, capacity: int, free: int, st_dev: str) -> None:
        with Session(self.engine) as session:
            session.add(
                Disk(
                    disk_name=name,
                    disk_capacity=capacity,
                    disk_free=free,
                    st_dev=st_dev,
                )
            )
            session.commit()

    def insert_files(self, dev_files: DeviceFiles) -> DeviceFiles:
        """
        Accept `DeviceFiles` object and return such object with
        files already registred in the DB.
        """
        already_in_db = DeviceFiles(device=dev_files.device, files=[])
        self.update_disk_usage(device=dev_files.device)
        with Session(self.engine) as session:
            disk_id = session.scalars(
                select(Disk.id).where(Disk.st_dev == dev_files.device.st_dev)
            ).one()
            for file in dev_files.files:
                file_from_db = session.scalars(
                    select(File)
                    .where(File.file_name == file.name)
                    .where(File.disk_id == disk_id)
                ).all()
                if len(file_from_db) == 0:
                    session.add(
                        File(
                            file_name=file.name,
                            disk_path=file.path,
                            st_ino=file.stat_ino,
                            last_modified=file.last_mod,
                            size=file.size,
                            disk_id=disk_id,
                        )
                    )
                else:
                    already_in_db.files.append(file)
            session.commit()
        return already_in_db

    def update_disk_usage(self, device: Device) -> None:
        with Session(self.engine) as session:
            session.query(Disk).filter(Disk.st_dev == device.st_dev).update(
                {Disk.disk_free: device.free}
            )
            session.commit()
