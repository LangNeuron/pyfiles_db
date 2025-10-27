# Copyright 2025 LangNeuron
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""FilesDB."""

from __future__ import annotations

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self  # noqa: UP035 for Python < 3.11


import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar

from .errors import (
    DataIsUncorrectError,
    NotFoundColumnError,
    NotFoundTableError,
    PathNotAvaibleError,
    TableAlredyAvaibleError,
    UnknownDataTypeError,
)

if TYPE_CHECKING:
    from collections.abc import Generator

BASE_PATH_STORAGE = Path(__file__).parent.parent.parent / "database"


def infinite_natural_numbers(start: int) -> Generator[Any, Any, Any]:
    """Generate numbers."""
    number = start
    while True:
        yield number
        number += 1

@dataclass
class META:
    """Meta data for the database."""

    TABLES: str = "TABLES"
    ENCRYPTDB: str = "ENCRYPTDB"
    COLUMNS: str = "COLUMNS"
    TABLE_PREFIX: str = "TABLE_PREFIX"
    GENERATOR: str = "GENERATOR"
    FILE_IDS: str = "FILE_IDS"


class FilesDB:
    """FilesDB, manager for DB."""

    _instance: ClassVar[Self | None] = None

    def __new__(cls: type[Self]) -> Self:
        """
        Create or return the existing singleton instance.

        Returns
        -------
        FilesDB
            The existing or newly created singleton instance.
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def init(self,
             storage: Path | str | None = None,
             *,
             asyncbd: bool = False,
             meta_file: str = "meta.json",
             meta: dict[str, Any] | None = None,
            ) -> _DB:
        """Initinalize a new database.

        If database is already loaded - connection
        If database is not loaded - create new one

        Parameters
        ----------
        storage : Path | str | None, optional
            path to databse location, by default None
        asyncbd : bool, optional
            use async io database, by default False
        meta_file : str, optional
            name of meta file, by default "meta.json"

        Returns
        -------
        _DB
            base database structure
        """
        if meta is None:
            meta = {}
        self._meta_file = meta_file
        if storage is None:
            storage = BASE_PATH_STORAGE
        if self._check_storage(storage=storage):
            self._create_base_meta_information(storage, meta=meta)
        return self._connect(storage=storage, asyncbd=asyncbd)

    def _connect(self, storage: str | Path, *, asyncbd: bool = False) -> _DB:
        """Connect to database, load meta information.

        Parameters
        ----------
        storage : str | Path
            path to database location
        asyncbd : bool, optional
            use async io database, by default False

        Returns
        -------
        _DB
            _DB instance of database loader
        """
        if asyncbd:
            return _DBasync(storage=storage, meta_file=self._meta_file)
        return _DBsync(storage=storage, meta_file=self._meta_file)

    def _base_meta(self) -> dict[str, Any]:
        """Return base meat information.

        Returns
        -------
        dict[str, Any]
            base meta information
        """
        return {
            META.TABLES: [],
            META.ENCRYPTDB: False,
            META.TABLE_PREFIX: "TABLE_",
        }

    def _valid_key_value(self, key: str, value: Any) -> None:  # noqa: ANN401
        """Validate data type for meta.

        Parameters
        ----------
        key : str
            key of meta information
        value : Any
            value of meta information

        Raises
        ------
        TypeError
            When data type is not valid
        """
        match(key):
            case META.TABLES:
                if not isinstance(value, list):
                    raise TypeError
            case META.ENCRYPTDB:
                if not isinstance(value, bool):
                    raise TypeError

    def _configure_meta(self, meta: dict[str, Any]) -> dict[str, Any]:
        """Configure meta information.

        Parameters
        ----------
        meta : dict[str, Any]
            raw meta information from user

        Returns
        -------
        dict[str, Any]
            meta information
        """
        new_meta = self._base_meta()
        for key, value in meta.items():
            self._valid_key_value(key, value)
            new_meta[key] = value
        return new_meta


    def _create_base_meta_information(self,
                                      storage: str | Path,
                                      meta: dict[str, Any]) -> None:
        """Create base meta structure files.

        Parameters
        ----------
        storage : str | Path
            path to database location
        meta : dict[str, Any]
           raw meta information from user
        """
        meta = self._configure_meta(meta)
        storage = Path(storage)
        with Path.open(storage / "meta.json", "w") as f:
            json.dump(meta, f)

    def _check_storage(self, storage: str | Path) -> bool:
        """Check storage for avaible.

        Parameters
        ----------
        storage : str | Path
            path  to database location

        Returns
        -------
        bool
            database alredy exist.
            False - if not exist.
            True - if esist meta file.

        Raises
        ------
        PathNotAvaibleError
            Exception for if path not avaible
        NotADirectoryError
            Exception when path not a dir
        """
        storage = Path(storage)
        storage.mkdir(parents=True, exist_ok=True)
        if not storage.exists():
            raise PathNotAvaibleError
        if not storage.is_dir():
            raise NotADirectoryError
        return not (storage / self._meta_file).exists()



class _DB(ABC):
    @abstractmethod
    def __init__(self, storage: str | Path, meta_file: str) -> None:
        """Init databs.

        Parameters
        ----------
        storage : str | Path
            path to db location
        meta_file : str
           name of meta file
        """

    @abstractmethod
    def create_table(self, table_name: str, columns: dict[str, str],
                     id_generator: str | None = None) -> None:
        """Craete a new table.

        Parameters
        ----------
        table_name : str
            name of table
        columns : dict[str, str]
            columns with data type
        id_generator : str, None
            default None
            str is name of column data when need use how nameing of file
            None use simple id generator (increment, not recominded)
        """

    @abstractmethod
    def new_data(self, table_name: str, data: dict[str, Any]) -> None:
        """Add new data to database.

        Parameters
        ----------
        tabel : str
            name of data table
        data : dict[str, Any]
            information when need save
        """

    @abstractmethod
    def find(self, table_name: str, condition: str) -> dict[str, Any]:
        """Find information in database.

        Parameters
        ----------
        table_name : str
            name of table
        condition : str
            maybe  is "id == 1"

        Returns
        -------
        dict[str, Any]
            all data in table
        """

class _DBsync(_DB):
    def __init__(self, storage: str | Path, meta_file: str) -> None:
        """Init databs.

        Parameters
        ----------
        storage : str | Path
            path to db location
        meta_file : str
           name of meta file
        """
        self._storage = Path(storage)
        self._meta_file = meta_file
        self._load_meta()
        self._id_generators: dict[str, Generator[Any, Any, Any]] = {}

    def _load_meta(self) -> None:
        """Load meta information from file."""
        with Path.open(self._storage / self._meta_file, "r") as f:
            self._meta = json.load(f)

    def create_table(self, table_name: str, columns: dict[str, str],
                     id_generator: str | int | None = None) -> None:
        """Create table.

        Parameters
        ----------
        table_name : str
            name of table
        columns : dict[str, str]
            columns with data type
        id_generator : str | None
           generator for name of file. Default None

        Raises
        ------
        TableAlredyAvaibleError
            if table alredy avaible
        """
        # Table. columns is maybe {"USER_ID": "INT", "NAME": "TEXT"}
        table = self._meta[META.TABLE_PREFIX] + table_name
        if table in self._meta[META.TABLES]:
            raise TableAlredyAvaibleError
        if id_generator is None:
            id_generator = 0
            self._id_generators[table] = infinite_natural_numbers(id_generator)
        self._mkdir_for_table(table)
        self._meta[META.TABLES].append(table)
        self._meta[table] = {
            META.COLUMNS: columns,
            META.GENERATOR: id_generator}
        self._update_meta()

    def _update_meta(self) -> None:
        """Update meta file."""
        with Path.open(self._storage / self._meta_file, mode="w") as f:
            json.dump(self._meta, f)

    def _mkdir_for_table(self, table: str | Path) -> None:
        """Make table foleder.

        Parameters
        ----------
        table : str | Path
            name of table folder
        """
        (self._storage / table).mkdir(parents=False, exist_ok=True)
        with Path.open(self._storage / table / ".json", mode="w") as f:
            json.dump({META.FILE_IDS: []}, f)

    def new_data(self, table_name: str, data: dict[str, Any]) -> None:
        """Save new data to table.

        Parameters
        ----------
        table_name : str
            name of need table
        data : dict[str, Any]
            information when need save
        """
        table_name = self._meta[META.TABLE_PREFIX] + table_name
        if not self._check_table(table_name):
            raise NotFoundTableError(table_name=table_name)
        if not self._check_data(self._meta[table_name][META.COLUMNS], data):
            raise DataIsUncorrectError(data=data)
        file_name = ""
        if (self._meta[table_name][META.GENERATOR] is None or
         isinstance(self._meta[table_name][META.GENERATOR], int)):
            if self._id_generators.get(table_name) is None:
                self._id_generators[table_name] = infinite_natural_numbers(
                    self._meta[table_name][META.GENERATOR])
            file_name = next(self._id_generators[table_name])
            self._meta[table_name][META.GENERATOR] += 1
            self._update_meta()
        else:
            file_name = data[self._meta[table_name][META.GENERATOR]]
        with Path.open(
                self._storage / table_name / f"{file_name}.json",
                mode="w") as f:
            json.dump(data, f)
        with Path.open(self._storage / table_name / ".json", mode="r") as f:
            data = json.load(f)
            data[META.FILE_IDS].append(file_name)
        with Path.open(self._storage / table_name / ".json", mode="w") as f:
            json.dump(data, f)

    def _check_table(self, table: str) -> bool:
        """Check table for exists.

        Parameters
        ----------
        table : str
            name of table

        Returns
        -------
        bool
            exist table
        """
        return table in self._meta[META.TABLES]

    def _check_data(self, columns: dict[str, str],
                    data: dict[str, Any]) -> bool:
        """Check type data.

        Parameters
        ----------
        columns : dict[str, str]
            col of table
        data : dict[str, Any]
            new information

        Returns
        -------
        bool
            Data is correct
        """
        for key, val in data.items():
            if (self._change_type(val, columns[key]) != val):
                return False
        return True

    def find(self, table_name: str, condition: str) -> dict[str, Any]:
        """Find information in table.

        Parameters
        ----------
        table_name : str
            name of table
        condition : str
            condition, maybe "id == 5"

        Returns
        -------
        dict[str, Any]
            all data when find condition

        Raises
        ------
        ValueError
            Table not found error
        ValueError
            Column not found error
        """
        table_name = self._meta[META.TABLE_PREFIX] + table_name
        if not self._check_table(table_name):
            raise NotFoundTableError(table_name=table_name)
        column_name, value = condition.replace(" ", "").split("==")
        if not self._check_column_in_table(table_name, column_name):
            raise NotFoundColumnError(column_name=column_name,
                                      table_name=table_name)
        value = self._change_type(value,
                                  self._meta[table_name][META.COLUMNS][column_name])
        if self._meta[table_name][META.GENERATOR] == column_name:
            with Path.open(
                    self._storage / table_name / f"{value}.json",
                    mode="r") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
                return {}
        with Path.open(
            self._storage / table_name / ".json",mode="r") as f:
            data = json.load(f)
            names = data[META.FILE_IDS]
        for name in names:
            with Path.open(
                    self._storage / table_name / f"{name}.json",
                    mode="r") as f:
                data = json.load(f)
                if data[column_name] == value and isinstance(data, dict):
                    return data
        return {column_name: value}

    def _check_column_in_table(self, table_name: str, column_name: str) -> bool:
        """Chech column in table on exist.

        Parameters
        ----------
        table_name : str
            name of table
        column_name : str
            name of column

        Returns
        -------
        bool
            esist column
        """
        return column_name in self._meta[table_name][META.COLUMNS]

    def _change_type(self, value: str, column_type: str) -> Any:  # noqa: ANN401
        """Change data type.

        Parameters
        ----------
        value : str
            value
        column_type : str
            data type

        Returns
        -------
        Any
            correct data type

        Raises
        ------
        ValueError
            if column_type is unknown
        """
        match column_type:
            case "INT":
                return int(value)
            case "TEXT":
                return str(value)
            case _:
                raise UnknownDataTypeError

class _DBasync(_DB):
    def __init__(self, storage: str | Path, meta_file: str) -> None:
        """Init databs.

        Parameters
        ----------
        storage : str | Path
            path to db location
        meta_file : str
           name of meta file
        """
        self._storage = storage
        self._meta_file = meta_file

    def create_table(self, table_name: str, columns: dict[str, Any],
                     id_generator: str | None = None) -> None:
        """Create table.

        Parameters
        ----------
        table_name : str
            name of table
        columns : dict[str, Any]
            columns with data type
        """

    def new_data(self, table_name: str, data: dict[str, Any]) -> None:
        """Add new data to database.

        Parameters
        ----------
        table : str
            name of data table
        data : dict[str, Any]
            information when need save
        """

    def find(self, table_name: str, condition: str) -> dict[str, Any]:
        """Find information in database.

        Parameters
        ----------
        table_name : str
            name of table
        condition : str
            maybe  is "id == 1"

        Returns
        -------
        dict[str, Any]
            all data in table
        """
        return {table_name: condition}
