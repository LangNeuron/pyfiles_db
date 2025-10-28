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

"""Test deleate file."""

import pytest
from pyfiles_db.files_db import FilesDB

data = [
    {"id": 1, "first_name": "John", "last_name": "Doe", "number": 8},
    {"id": 2, "first_name": "Jane", "last_name": "Smith", "number": 12},
    {"id": 3, "first_name": "Alex", "last_name": "Johnson", "number": 5},
    {"id": 4, "first_name": "Emily", "last_name": "Brown", "number": 8},
    {"id": 5, "first_name": "Chris", "last_name": "Davis", "number": 15},
    {"id": 6, "first_name": "Sarah", "last_name": "Miller", "number": 8},
    {"id": 7, "first_name": "John", "last_name": "Doe", "number": 10},
    {"id": 8, "first_name": "Kate", "last_name": "Wilson", "number": 3},
    {"id": 9, "first_name": "Tom", "last_name": "Anderson", "number": 5},
    {"id": 10, "first_name": "Emily", "last_name": "Brown", "number": 7},
]

def test_sync_deleate() -> None:
    """Test sync update."""
    db_name = "test_deleate_sync"
    f = FilesDB()
    db = f.init_sync()
    db.create_table(
        db_name,
        columns={"id": "INT",
                 "first_name": "TEXT",
                 "last_name": "TEXT",
                 "number": "INT",
                },
        id_generator="id",
    )

    for d in data:
        db.new_data(table_name=db_name, data=d)

    db.deleate(db_name, "5")

    try:
        db.find(db_name, "id == 5")
    except FileNotFoundError:
        pass
    except Exception:
        raise

@pytest.mark.asyncio
async def test_async_deleate() -> None:
    """Test async update."""
    db_name = "test_deleate_async"
    f = FilesDB()
    db = f.init_async()
    await db.create_table(
        db_name,
        columns={"id": "INT",
                 "first_name": "TEXT",
                 "last_name": "TEXT",
                 "number": "INT",
                },
        id_generator="id",
    )

    for d in data:
        await db.new_data(table_name=db_name, data=d)

    await db.deleate(db_name, "5")

    try:
        await db.find(db_name, "id == 5")
    except FileNotFoundError:
        pass
    except Exception:
        raise
