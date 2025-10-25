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


"""test database find."""

from src.pyfiles_db import FilesDB

d1 = {"id": 1, "first_name": "John", "last_name": "Doe", "number": 8}
d2 = {"id": 2, "first_name": "Alex", "last_name": "Wandack", "number": 101}
db_name = "test_finder"

def test_find() -> None:
    """Test for find module."""
    f = FilesDB()
    bd = f.init()
    bd.create_table(db_name, columns={"id": "INT",
                                            "first_name": "TEXT",
                                            "last_name": "TEXT",
                                            "number": "INT"}, id_generator="id")
    bd.new_data(db_name, d1)
    bd.new_data(db_name, d2)
    if not (bd.find(db_name, "number == 8") == d1):
        raise ValueError
    if not (bd.find(db_name, "id==1") == d1):
        raise ValueError
    if not (bd.find(db_name, "last_name == Wandack") == d2):
        raise ValueError
