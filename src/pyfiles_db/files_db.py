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
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

from .errors import PathNotAvaibleError

BASE_PATH_STORAGE = Path(__file__).parent.parent.parent / "database"



@dataclass
class META:
    """Meta data for the database."""

    TABLES: str = "TABLES"
    ENCRYPTDB: str = "ENCRYPTDB"


class FilesDB:
    """FilesDB, manager for DB."""

    _instance: Self | None = None

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
        return cast("Self", cls._instance)

    def init(self,
             storage: Path | str | None = None,
             *,
             asyncbd: bool = False,
             meta_file: str = "meta.json",
             **meta: dict[str, Any],
            ) -> object:
        """Initinalize a new database.

        If database is already loaded - connection
        If database is not loaded - create new one

        PARAMS
        ------
        sorage: str | Path
          path to database location
        """
        self._meta_file = meta_file
        if storage is None:
            storage = BASE_PATH_STORAGE
        if self._check_storage(storage=storage):
            self._create_base_meta_information(storage, meta=meta)
        return self._connect(storage=storage, asyncbd=asyncbd)

    def _connect(self, storage: str | Path, *, asyncbd: bool = False) -> object:
        """Connect to database, load meta information.

        Parameters
        ----------
        storage : str | Path
            path to database location
        asyncbd : bool, optional
            async io database, by default False

        Returns
        -------
        object
            object of database loader
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



class _DBsync:
    def __init__(self, storage: str | Path, meta_file: str) -> None:
        self._storage = Path(storage)
        self._meta_file = meta_file
        self._load_meta()

    def _load_meta(self) -> None:
        with Path.open(self._storage / self._meta_file, "r") as f:
            self.meta = json.load(f)


class _DBasync:
    def __init__(self, storage: str | Path, meta_file: str) -> None:
        self._storage = storage
        self._meta_file = meta_file
