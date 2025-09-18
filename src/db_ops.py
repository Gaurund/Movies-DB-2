from dataclasses import dataclass
from datetime import time
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from db_classes import Base, Disk, File, Movie


@dataclass
class DBDev:
    id: int
    name: str
    image: str
    capacity: int
    free_space: int
    stat_dev: str

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
            stat_dev=self.disk.st_dev,
        )


class ConnectDB:
    def __init__(self, engine: str) -> None:
        self.engine = create_engine(engine)
        Base.metadata.create_all(self.engine)


class DBReader:
    def __init__(self, conn: ConnectDB) -> None:
        self.conn = conn

    def get_disk_by_stat(self, stat_dev: str) -> int | None:
        """
        Checking is the device already in DB
        and return device's id or None.
        """
        with Session(self.conn.engine) as session:
            disk_id = session.scalars(
                select(Disk.id).where(Disk.st_dev == stat_dev)
            ).one_or_none()
        return disk_id

    def get_disks(self) -> list:
        """
        Return dictionary of storage devices.
        """
        disks = list()
        with Session(self.conn.engine) as session:
            db_disks = session.scalars(select(Disk)).all()
            for d in db_disks:
                getter = RetrieveDBDev(d)
                disks.append(getter.retrieve())
        return disks


if __name__ == "__main__":
    engine: str = "sqlite:///movie.db"
    conn = ConnectDB(engine=engine)
    db_reader = DBReader(conn=conn)
    disks = db_reader.get_disks()
    [print(f"id:{d.id}\tname:{d.name}\tcapacity:{d.capacity}") for d in disks]
