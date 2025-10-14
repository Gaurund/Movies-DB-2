from datetime import time, datetime
from typing import List

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    ForeignKey,
    String,
    Table,
    Text,
    Time,
    Integer,
)
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm import mapped_column, relationship


class Base(DeclarativeBase):
    pass


genres_movies_table = Table(
    "genres_movies_table",
    Base.metadata,
    Column("genre_id", ForeignKey("genre_table.id"), primary_key=True),
    Column("movie_id", ForeignKey("movie_table.id"), primary_key=True),
)

actors_movies_table = Table(
    "actors_movies_table",
    Base.metadata,
    Column("person_id", ForeignKey("person_table.id"), primary_key=True),
    Column("movie_id", ForeignKey("movie_table.id"), primary_key=True),
)

directors_movies_table = Table(
    "directors_movies_table",
    Base.metadata,
    Column("persons_id", ForeignKey("person_table.id"), primary_key=True),
    Column("movies_id", ForeignKey("movie_table.id"), primary_key=True),
)

class File(Base):
    """
    The table to store files.

    `file_name`: a full name of a file

    `disk_path`: an absolute path to a folder contains the file

    `st_ino`: a unique identifier of the file

    `last_modified`: a date time stamp

    `size`: the file's size in bytes

    `disk_id`: an ID of a disk has the file

    `disk`: an entity of the disk

    `movie_id`: an ID of a movie linked to the file

    `movie`: an entity of the movie
    """

    __tablename__ = "file_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    file_name: Mapped[str] = mapped_column(String(160))
    disk_path: Mapped[str] = mapped_column(Text)
    st_ino: Mapped[str] = mapped_column(String(28))
    last_modified: Mapped[datetime]
    size: Mapped[int] = mapped_column(BigInteger)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    disk_id: Mapped[int] = mapped_column(ForeignKey("disk_table.id"))
    disk: Mapped["Disk"] = relationship(back_populates="files")

    movie_id: Mapped[int] = mapped_column(ForeignKey("movie_table.id"), nullable=True)
    movie: Mapped["Movie"] = relationship(back_populates="files")


class Type(Base):
    """
    The table to store different types.

    type_name: a name of a type
    russian_type_name: a russian translation of the type's name
    movies: a list of movies with such type
    """

    __tablename__ = "type_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    type_name: Mapped[str] = mapped_column(String(32))
    russian_type_name: Mapped[str] = mapped_column(String(32), nullable=True)

    movies: Mapped[List["Movie"]] = relationship(back_populates="movie_type")


class Person(Base):
    """
    full_name: a full name of a person
    russian_name: a russian translation of the name
    imdb_link: URL to a web page of the person in IMDb

    type_id: a unique identifier of a type the person has

    movies_actors: a list of actors participated in the movie
    movies_directors: a list of directors of the movie
    """

    __tablename__ = "person_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(128))
    russian_name: Mapped[str] = mapped_column(String(128), nullable=True)
    imdb_link: Mapped[str] = mapped_column(String(128), nullable=True)

    type_id: Mapped[int] = mapped_column(ForeignKey("type_table.id"))

    movies_actors: Mapped[List["Movie"]] = relationship(
        secondary=actors_movies_table, back_populates="actors"
    )

    movies_directors: Mapped[List["Movie"]] = relationship(
        secondary=directors_movies_table, back_populates="directors"
    )


class Disk(Base):
    """
    The table to store devices.

    `disk_name`: a name of a disk

    `disk_image`: a URI to an image file of the disk

    `disk_capacity`: a capacity of the disk

    `disk_free`: the free space of the disk

    `st_dev`: a unique identifier of the disk

    `files`: list of files stored on the disk

    """

    __tablename__ = "disk_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    disk_name: Mapped[str] = mapped_column(String(30))
    disk_image: Mapped[str] = mapped_column(String(260), nullable=True)
    disk_capacity: Mapped[int] = mapped_column(BigInteger)
    disk_free: Mapped[int] = mapped_column(BigInteger)
    st_dev: Mapped[str] = mapped_column(String(32))

    files: Mapped[List[File]] = relationship(back_populates="disk")


class Genre(Base):
    """
    The table of genres.

    eng_genre: An english name of a genre
    rus_genre: A russian name of a genre

    movies: A list of movies have the genre
    """

    __tablename__ = "genre_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    eng_genre: Mapped[str] = mapped_column(String(64))
    rus_genre: Mapped[str] = mapped_column(String(64), nullable=True)

    movies: Mapped[List["Movie"]] = relationship(
        secondary=genres_movies_table, back_populates="genres"
    )

class Franchise(Base):
    """
    The franchises table.

    franchise: a name of a franchise
    movies: a list of movies linked to the franchise
    """
    __tablename__ = "franchise_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    franchise: Mapped[str] = mapped_column(String(64))
    
    movies: Mapped[List["Movie"]] = relationship(
        back_populates="franchise"
    )

class Movie(Base):
    """
    The table to store movies and TV shows.

    `name_original`: an original name of the movie.
    `name_russian`: a russian translation of the name.
    `duration`: the movie duration time.
    `premiere_date`: the realse year of the movie.
    `imdb_link`: a URL to IMDb page of the movie.
    `description`: some details one would like to write down.
    `active`: a boolean that answers is movie consider deleted from DB.
    `files`: a list of files linked to the movie.
    `genres`: a list of genres linked to the movie.
    """

    __tablename__ = "movie_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name_original: Mapped[str] = mapped_column(String(160), nullable=True)
    name_russian: Mapped[str] = mapped_column(String(160), nullable=True)
    duration: Mapped[time] = mapped_column(Time, nullable=True)
    premiere_date: Mapped[str] = mapped_column(String(16), nullable=True)
    imdb_link: Mapped[str] = mapped_column(String(128), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    files: Mapped[List[File]] = relationship(back_populates="movie")

    type_id: Mapped[int] = mapped_column(ForeignKey("type_table.id"), nullable=True)
    movie_type: Mapped["Type"] = relationship( back_populates="movies")

    franchise_id: Mapped[int] = mapped_column(ForeignKey("franchise_table.id"), nullable=True)
    franchise: Mapped["Franchise"] = relationship(back_populates="movies")
    franchise_part: Mapped[int] = mapped_column(Integer, nullable=True)

    genres: Mapped[List["Genre"]] = relationship(
        secondary=genres_movies_table, back_populates="movies"
    )

    actors: Mapped[List["Person"]] = relationship(
        secondary=actors_movies_table, back_populates="movies_actors"
    )

    directors: Mapped[List["Person"]] = relationship(
        secondary=directors_movies_table, back_populates="movies_directors"
    )

