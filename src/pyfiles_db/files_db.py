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


from pathlib import Path
from typing import Any, cast

from .errors import DbNotLoadedError

BASE_PATH_STORAGE = Path(__file__).parent.parent / "database"


class FilesDB:
    """FilesDB, manager for DB."""

    _instance: Self | None = None

    _db_loaded: dict[str | Path, tuple[object, dict[str, Any]]] | None = None

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

    def init(self, storage: Path | str | None = None) -> object:
        """Initinalize a new database or get new copy of existing one."""
        if storage is None:
            storage = BASE_PATH_STORAGE
        else:
            self._check_storage(storage=storage)
        if self._db_loaded is None:
            return self._new_db(storage=storage)
        if storage in self._db_loaded:
            return self._get_db(storage=storage)
        return self._new_db(storage=storage)

    def _new_db(self, storage: str | Path) -> object:
        return _DBsync(storage=storage)

    def _check_storage(self, storage: str | Path) -> None:
        """Check storage (path)."""
        # TODO: check path for avaible

    def _get_db(self, storage: str | Path) -> object:
        if self._db_loaded is None:
            raise DbNotLoadedError # TODO: ERROR specifical
        return self._db_loaded[storage][0]

class _DBsync:
    def __init__(self, storage: str | Path) -> None:
        self.storage = storage
