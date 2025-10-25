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

from src.pyfiles_db import FilesDB


def test_create_table() -> None:
    """Test for create table."""
    file_db = FilesDB()
    db = file_db.init()
    db.create_table(table_name="test_craete_table", columns={"id": "INT",
                                                     "first_name": "TEXT",
                                                     "last_name": "TEXT",
                                                     "number": "INT"},
                         id_generator="id")
