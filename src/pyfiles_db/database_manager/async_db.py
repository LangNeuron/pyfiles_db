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
from pyfiles_db.errors import TableAlredyAvaibleError
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

    async def find(self, table_name: str, condition: str) -> dict[str, Any]:
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

