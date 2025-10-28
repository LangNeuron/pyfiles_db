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

"""Abstrct database manager."""

from abc import ABC, abstractmethod
from collections.abc import Coroutine
from pathlib import Path
from typing import Any


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
    def create_table(self, table_name: str,
                     columns: dict[str, str],
                     id_generator: str | int | None = None,
                     ) -> None | Coroutine[Any, Any, None]:
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
    def find(self, table_name: str, condition: str) -> list[dict[str, Any]]:
        """Find information in database.

        Parameters
        ----------
        table_name : str
            name of table
        condition : str
            maybe  is "id == 1"

        Returns
        -------
        list[dict[str, Any]]
            all data in table
        """

    @abstractmethod
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
            unical file name
        new_data : dict[str, Any]
            new data when need save
        """
    @abstractmethod
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

class _AsyncDB(ABC):
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
    async def create_table(self, table_name: str,
                     columns: dict[str, str],
                     id_generator: str | int | None = None,
                     ) -> None:
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
    async def new_data(self, table_name: str, data: dict[str, Any]) -> None:
        """Add new data to database.

        Parameters
        ----------
        tabel : str
            name of data table
        data : dict[str, Any]
            information when need save
        """

    @abstractmethod
    async def find(self,
                   table_name: str,
                   condition: str,
                   ) -> list[dict[str, Any]]:
        """Find information in database.

        Parameters
        ----------
        table_name : str
            name of table
        condition : str
            maybe  is "id == 1"

        Returns
        -------
        list[dict[str, Any]]
            all data in table
        """

    @abstractmethod
    async def update(self,
                     table_name: str,
                     file_id: str,
                     new_data: dict[str, Any],
                     ) -> None:
        """Update data with file_id.

        Get file_id from find method.

        Parameters
        ----------
        file_id : str
            unical file name
        new_data : dict[str, Any]
            new data when need save
        """

    @abstractmethod
    async def delete(self,
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
