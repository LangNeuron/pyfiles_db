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

"""Sync database manager."""

import json
from pathlib import Path
from typing import TYPE_CHECKING, Any

from pyfiles_db.database_manager._db import _DB
from pyfiles_db.database_manager.meta import META
from pyfiles_db.errors import (
    DataIsUncorrectError,
    NotFoundColumnError,
    NotFoundTableError,
    TableAlreadyAvaibleError,
    UnknownDataTypeError,
)
from pyfiles_db.utils import infinite_natural_numbers

if TYPE_CHECKING:
    from collections.abc import Generator


class _DBsync(_DB):
    def __init__(self, storage: str | Path, meta_file: str) -> None:
        """Initialize the synchronous database manager.

        Parameters
        ----------
        storage : str | Path
            Path to the database location.
        meta_file : str
            Name of the meta file.
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
        """Create a table (sync).

        Parameters
        ----------
        table_name : str
            Name of the table.
        columns : dict[str, str]
            Columns mapping to their data types.
        id_generator : str | None
            Generator for file names. Default None.

        Raises
        ------
        TableAlreadyAvaibleError
            If the table already exists.
        """
        # Table. columns is maybe {"USER_ID": "INT", "NAME": "TEXT"}
        table = self._meta[META.TABLE_PREFIX] + table_name
        if table in self._meta[META.TABLES]:
            raise TableAlreadyAvaibleError
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
        """Create the on-disk folder and index file for a table.

        Parameters
        ----------
        table : str | Path
            Name of the table folder.
        """
        (self._storage / table).mkdir(parents=False, exist_ok=True)
        with Path.open(self._storage / table / ".json", mode="w") as f:
            json.dump({META.FILE_IDS: []}, f)

    def new_data(self, table_name: str, data: dict[str, Any]) -> None:
        """Save new data to the table.

        Parameters
        ----------
        table_name : str
            Name of the table.
        data : dict[str, Any]
            Record to save.
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
            data[META.FILE_IDS].append(str(file_name))
        with Path.open(self._storage / table_name / ".json", mode="w") as f:
            json.dump(data, f)

    def _check_table(self, table: str) -> bool:
        """Check whether a table exists.

        Parameters
        ----------
        table : str
            Name of the table.

        Returns
        -------
        bool
            True if the table exists.
        """
        return table in self._meta[META.TABLES]

    def _check_data(self, columns: dict[str, str],
                    data: dict[str, Any]) -> bool:
        """Validate data types for a record against table columns.

        Parameters
        ----------
        columns : dict[str, str]
            Column definitions for the table.
        data : dict[str, Any]
            Record to validate.

        Returns
        -------
        bool
            True if the record matches the declared column types.
        """
        for key, val in data.items():
            if (self._change_type(val, columns[key]) != val):
                return False
        return True

    def find(self,
             table_name: str,
             condition: str,
             ) -> list[dict[str, Any]]:
        """Find records in a table matching a simple condition.

        Parameters
        ----------
        table_name : str
            Name of the table.
        condition : str
            Condition string, e.g. "id == 5".

        Returns
        -------
        list[dict[str, Any]]
            Records that match the condition.

        Raises
        ------
        ValueError
            Table not found or column not found.
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
            try:
                with Path.open(
                    self._storage / table_name / f"{value}.json",
                    mode="r") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        return [{str(value): data}]
                    return []
            except FileNotFoundError:
                return []
        with Path.open(
            self._storage / table_name / ".json",mode="r") as f:
            data = json.load(f)
            names = data[META.FILE_IDS]
        result: list[dict[str, Any]] = []
        for name in names:
            with Path.open(
                    self._storage / table_name / f"{name}.json",
                    mode="r") as f:
                d = json.load(f)
                if d[column_name] == value and isinstance(d, dict):
                    result.append({str(name): d})
        return result

    def _check_column_in_table(self, table_name: str, column_name: str) -> bool:
        """Check column in table on exist.

        Parameters
        ----------
        table_name : str
            name of table
        column_name : str
            name of column

        Returns
        -------
        bool
            exist column
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


    def update(self,
               table_name: str,
               file_id: str,
               new_data: dict[str, Any],
               ) -> None:
        """Update data with file_id.

        Get file_id from find method.

        Parameters
        ----------
        file_id : str
            unique  file name
        new_data : dict[str, Any]
            new data when need save
        """
        table_name = self._meta[META.TABLE_PREFIX] + table_name
        with Path.open(
            self._storage / table_name / f"{file_id}.json",
            mode="w") as f:
            json.dump(new_data, f)

    def delete(self,
                table_name: str,
                file_id: str,
                ) -> None:
        """Delete data with file_id.

        Parameters
        ----------
        table_name : str
            name of table db
        file_id : str
            name of file in table
        """
        table_name = self._meta[META.TABLE_PREFIX] + table_name
        if not (self._storage / table_name / f"{file_id}.json").exists():
            raise FileNotFoundError
        (self._storage / table_name / f"{file_id}.json").unlink()
        with Path.open(self._storage / table_name / ".json") as f:
            data = json.load(f)
        data[META.FILE_IDS].remove(str(file_id))
        with Path.open(self._storage / table_name / ".json", "w") as f:
            json.dump(data, f)
