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


"""test create table."""

import json
from pathlib import Path

from src.pyfiles_db import FilesDB
from src.pyfiles_db.files_db import META


def test_sync_create_table() -> None:
    """Test for async database create table."""
    table_prefix = "TABLE_TEST_PREFIX_"
    table_name = "test_craete_table_async_database"
    storage_path = Path("database")
    meta_file = "metf.json"
    file_db = FilesDB()
    db = file_db.init(asyncbd=False, meta={META.TABLE_PREFIX: table_prefix},
                      meta_file=meta_file)
    db.create_table(table_name=table_name, columns={"id": "INT",
                                                     "first_name": "TEXT",
                                                     "last_name": "TEXT",
                                                     "number": "INT"},
                         id_generator="id")

    with Path.open(f"{storage_path / meta_file}") as f:
        data = json.load(f)

    if data[META.TABLE_PREFIX] != table_prefix:
        raise ValueError

    with Path.open(
        f"{storage_path / (table_prefix + table_name) / '.json'}",
                   ) as f:
        data = json.load(f)


def test_files_name_generator() -> None:
    """Test files name genearator. id's generator."""
    table_prefix = "TABLE_"
    fisrt_len = 10
    second_len = 20
    storage_path = Path("database")
    table_name = "test_files_name_generator"
    test_data = {
        "ID": 0,
        "NAME": "JDH",
        "NUMBER": 0,
    }
    file_db = FilesDB()
    db = file_db.init(meta={META.TABLE_PREFIX: table_prefix})
    db.create_table(table_name=table_name, columns={
        "ID": "INT",
        "NAME": "TEXT",
        "NUMBER": "INT",
    })

    for i in range(fisrt_len):
        test_data["NUMBER"] = i
        db.new_data(table_name=table_name, data=test_data)

    # check data ids.

    n = check_storage(storage_path / (table_prefix + table_name), "NUMBER")
    if n != fisrt_len:
        raise AssertionError(n)

    new_db = file_db.init()

    for i in range(fisrt_len, second_len):
        test_data["NUMBER"] = i
        new_db.new_data(table_name=table_name, data=test_data)

    # check data ids.

    n = check_storage(storage_path / (table_prefix + table_name), "NUMBER")
    if n != second_len:
        raise AssertionError(n)

def check_storage(storage: Path, key: str) -> int:
    """Check storage file for correct data."""
    correct_data = 0
    for file_path in storage.glob("*.json"):
        if file_path.name == ".json":
            continue
        file_name_without_ext = file_path.stem
        with Path.open(file_path, mode="r") as f:
            data = json.load(f)
        value_from_json = data[key]
        if str(file_name_without_ext) == str(value_from_json):
            correct_data += 1
    return correct_data

def test_async_create_table() -> None:
    """Test for async database create table."""
    table_prefix = "TABLE_TEST_PREFIX_"
    table_name = "test_craete_table_async_database"
    storage_path = Path("database")
    meta_file = "metf.json"
    file_db = FilesDB()
    db = file_db.init(asyncbd=True, meta={META.TABLE_PREFIX: table_prefix},
                      meta_file=meta_file)
    db.create_table(table_name=table_name, columns={"id": "INT",
                                                     "first_name": "TEXT",
                                                     "last_name": "TEXT",
                                                     "number": "INT"},
                         id_generator="id")

    with Path.open(f"{storage_path / file_db.meta_file}") as f:
        data = json.load(f)

    if data[META.TABLE_PREFIX] != table_prefix:
        raise ValueError

    with Path.open(
        f"{storage_path / (table_prefix + table_name) / '.json'}",
                   ) as f:
        data = json.load(f)
