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
from typing import cast

from .errors import PathNotAvaibleError

BASE_PATH_STORAGE = Path(__file__).parent.parent.parent / "database"


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
            ) -> object:
        """Initinalize a new database.

        If database is already loaded - connection
        If database is not loaded - create new one

        PARAMS
        ------
        sorage: str | Path
          Storage path
        """
        if storage is None:
            storage = BASE_PATH_STORAGE
        if self._check_storage(storage=storage):
            self._create_base_meta_information()
        return self._connect(storage=storage, asyncbd=asyncbd)

    def _connect(self, storage: str | Path, *, asyncbd: bool = False) -> object:
        # TODO: change connection with meta information
        if asyncbd:
            return _DBasync(storage=storage)
        return _DBsync(storage=storage)

    def _create_base_meta_information(self) -> None:
        """Create meta information."""

    def _check_storage(self, storage: str | Path) -> bool:
        """Check storage (path)."""
        storage = Path(storage)
        storage.mkdir(parents=True, exist_ok=True)
        if not storage.exists():
            raise PathNotAvaibleError
        if not storage.is_dir():
            raise NotADirectoryError
        return not (storage / "meta.json").exists()



class _DBsync:
    def __init__(self, storage: str | Path) -> None:
        self.storage = storage

class _DBasync:
    def __init__(self, storage: str | Path) -> None:
        self.storage = storage
