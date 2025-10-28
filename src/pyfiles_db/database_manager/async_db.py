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

"""Async database manager."""

import json
from pathlib import Path
from typing import TYPE_CHECKING, Any

import aiofiles

from pyfiles_db.database_manager._db import _AsyncDB
from pyfiles_db.database_manager.meta import META
from pyfiles_db.errors import (
    DataIsUncorrectError,
    NotFoundColumnError,
    NotFoundTableError,
    TableAlredyAvaibleError,
    UnknownDataTypeError,
)
from pyfiles_db.utils import infinite_natural_numbers

if TYPE_CHECKING:
    from collections.abc import Generator


class _DBasync(_AsyncDB):
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
        self._id_generators: dict[str, Generator[Any, Any, Any]] = {}
        self._load_meta()

    def _load_meta(self) -> None:
        """Load meta information from file."""
        with Path.open(self._storage / self._meta_file, "r") as f:
            self._meta = json.load(f)

    async def create_table(
            self, table_name: str,
            columns: dict[str, Any],
            id_generator: str | int | None = None,
            ) -> None:
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
        await self._mkdir_for_table(table)
        self._meta[META.TABLES].append(table)
        self._meta[table] = {
            META.COLUMNS: columns,
            META.GENERATOR: id_generator}
        await self._update_meta()

    async def _update_meta(self) -> None:
        """Update meta file."""
        async with aiofiles.open(
                self._storage / self._meta_file,
                mode="w",
                                ) as f:
            await f.write(json.dumps(self._meta))

    async def _mkdir_for_table(self, table: str | Path) -> None:
        """Make table foleder.

        Parameters
        ----------
        table : str | Path
            name of table folder
        """
        (self._storage / table).mkdir(parents=False, exist_ok=True)
        async with aiofiles.open(
            self._storage / table / ".json",
            mode="w",
            ) as f:
            await f.write(json.dumps({META.FILE_IDS: []}))


    async def new_data(self, table_name: str, data: dict[str, Any]) -> None:
        """Add new data to database.

        Parameters
        ----------
        table : str
            name of data table
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
            await self._update_meta()
        else:
            file_name = data[self._meta[table_name][META.GENERATOR]]
        async with aiofiles.open(
                self._storage / table_name / f"{file_name}.json",
                mode="w") as f:
            await f.write(json.dumps(data))
        async with aiofiles.open(
            self._storage / table_name / ".json") as f:
            content = await f.read()
            data = json.loads(content)
            data[META.FILE_IDS].append(file_name)
        async with aiofiles.open(
            self._storage / table_name / ".json", mode="w") as f:
            await f.write(json.dumps(data))

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


    async def find(self,
                   table_name: str,
                   condition: str,
                   ) -> list[dict[str, Any]]:
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
            async with aiofiles.open(
                    self._storage / table_name / f"{value}.json") as f:
                content = await f.read()
                data = json.loads(content)
                if isinstance(data, dict):
                    return [data]
                return []
        async with aiofiles.open(
            self._storage / table_name / ".json") as f:
            content = await f.read()
            data = json.loads(content)
            names = data[META.FILE_IDS]
        result: list[dict[str, Any]] = []
        for name in names:
            async with aiofiles.open(
                    self._storage / table_name / f"{name}.json") as f:
                content = await f.read()
                d = json.loads(content)
                if d[column_name] == value and isinstance(d, dict):
                    result.append(d)
        return result

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
