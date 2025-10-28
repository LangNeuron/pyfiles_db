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


import pytest

from src.pyfiles_db import FilesDB

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
    {"id": 11, "first_name": "Michael", "last_name": "Taylor", "number": 9},
    {"id": 12, "first_name": "Sarah", "last_name": "Miller", "number": 15},
    {"id": 13, "first_name": "David", "last_name": "Lee", "number": 11},
    {"id": 14, "first_name": "Anna", "last_name": "Walker", "number": 8},
    {"id": 15, "first_name": "Robert", "last_name": "Hall", "number": 14},
    {"id": 16, "first_name": "Linda", "last_name": "Allen", "number": 8},
    {"id": 17, "first_name": "James", "last_name": "Young", "number": 9},
    {"id": 18, "first_name": "Karen", "last_name": "King", "number": 4},
    {"id": 19, "first_name": "Alex", "last_name": "Johnson", "number": 5},
    {"id": 20, "first_name": "Sophia", "last_name": "Scott", "number": 10},
    {"id": 21, "first_name": "Daniel", "last_name": "Green", "number": 7},
    {"id": 22, "first_name": "Emily", "last_name": "Brown", "number": 8},
    {"id": 23, "first_name": "Jane", "last_name": "Smith", "number": 12},
    {"id": 24, "first_name": "Lucas", "last_name": "Adams", "number": 3},
    {"id": 25, "first_name": "Olivia", "last_name": "Clark", "number": 6},
    {"id": 26, "first_name": "William", "last_name": "Lopez", "number": 9},
    {"id": 27, "first_name": "Isabella", "last_name": "Hill", "number": 10},
    {"id": 28, "first_name": "Mason", "last_name": "Baker", "number": 8},
    {"id": 29, "first_name": "Ava", "last_name": "Gonzalez", "number": 5},
    {"id": 30, "first_name": "Ethan", "last_name": "Nelson", "number": 7},
    {"id": 31, "first_name": "Mia", "last_name": "Carter", "number": 12},
    {"id": 32, "first_name": "John", "last_name": "Doe", "number": 8},
    {"id": 33, "first_name": "Charlotte", "last_name": "Mitchell", "number": 6},
    {"id": 34, "first_name": "Benjamin", "last_name": "Perez", "number": 14},
    {"id": 35, "first_name": "Lucas", "last_name": "Adams", "number": 3},
    {"id": 36, "first_name": "Harper", "last_name": "Roberts", "number": 9},
    {"id": 37, "first_name": "Elijah", "last_name": "Turner", "number": 5},
    {"id": 38, "first_name": "Amelia", "last_name": "Phillips", "number": 10},
    {"id": 39, "first_name": "Liam", "last_name": "Campbell", "number": 11},
    {"id": 40, "first_name": "Ella", "last_name": "Parker", "number": 8},
    {"id": 41, "first_name": "Noah", "last_name": "Evans", "number": 7},
    {"id": 42, "first_name": "Grace", "last_name": "Edwards", "number": 6},
    {"id": 43, "first_name": "John", "last_name": "Doe", "number": 15},
    {"id": 44, "first_name": "Zoey", "last_name": "Collins", "number": 5},
    {"id": 45, "first_name": "Logan", "last_name": "Stewart", "number": 8},
    {"id": 46, "first_name": "Layla", "last_name": "Sanchez", "number": 4},
    {"id": 47, "first_name": "Jack", "last_name": "Morris", "number": 8},
    {"id": 48, "first_name": "Ella", "last_name": "Parker", "number": 10},
    {"id": 49, "first_name": "Henry", "last_name": "Rogers", "number": 11},
    {"id": 50, "first_name": "Lily", "last_name": "Reed", "number": 9},
    {"id": 51, "first_name": "Wyatt", "last_name": "Cook", "number": 6},
    {"id": 52, "first_name": "Aiden", "last_name": "Morgan", "number": 5},
    {"id": 53, "first_name": "Evelyn", "last_name": "Bell", "number": 8},
    {"id": 54, "first_name": "Sebastian", "last_name": "Murphy", "number": 14},
    {"id": 55, "first_name": "John", "last_name": "Doe", "number": 8},
    {"id": 56, "first_name": "Victoria", "last_name": "Bailey", "number": 3},
    {"id": 57, "first_name": "Daniel", "last_name": "Green", "number": 7},
    {"id": 58, "first_name": "Zoe", "last_name": "Rivera", "number": 12},
    {"id": 59, "first_name": "Nathan", "last_name": "Cooper", "number": 9},
    {"id": 60, "first_name": "Scarlett", "last_name": "Richardson", "number": 8},
    {"id": 61, "first_name": "Ryan", "last_name": "Howard", "number": 10},
    {"id": 62, "first_name": "Sofia", "last_name": "Ward", "number": 11},
    {"id": 63, "first_name": "Hunter", "last_name": "Torres", "number": 6},
    {"id": 64, "first_name": "Hannah", "last_name": "Peterson", "number": 5},
    {"id": 65, "first_name": "Levi", "last_name": "Gray", "number": 9},
    {"id": 66, "first_name": "Chloe", "last_name": "Ramirez", "number": 7},
    {"id": 67, "first_name": "John", "last_name": "Doe", "number": 12},
    {"id": 68, "first_name": "Penelope", "last_name": "James", "number": 4},
    {"id": 69, "first_name": "Matthew", "last_name": "Watson", "number": 8},
    {"id": 70, "first_name": "Riley", "last_name": "Brooks", "number": 10},
    {"id": 71, "first_name": "Luke", "last_name": "Kelly", "number": 11},
    {"id": 72, "first_name": "Aria", "last_name": "Sanders", "number": 6},
    {"id": 73, "first_name": "Carter", "last_name": "Price", "number": 5},
    {"id": 74, "first_name": "Nora", "last_name": "Bennett", "number": 8},
    {"id": 75, "first_name": "Grayson", "last_name": "Wood", "number": 9},
    {"id": 76, "first_name": "Camila", "last_name": "Barnes", "number": 7},
    {"id": 77, "first_name": "Isaac", "last_name": "Ross", "number": 5},
    {"id": 78, "first_name": "Madison", "last_name": "Henderson", "number": 10},
    {"id": 79, "first_name": "Anthony", "last_name": "Coleman", "number": 8},
    {"id": 80, "first_name": "Grace", "last_name": "Edwards", "number": 6},
    {"id": 81, "first_name": "Luna", "last_name": "Jenkins", "number": 12},
    {"id": 82, "first_name": "Dylan", "last_name": "Perry", "number": 9},
    {"id": 83, "first_name": "Stella", "last_name": "Powell", "number": 11},
    {"id": 84, "first_name": "Jack", "last_name": "Morris", "number": 10},
    {"id": 85, "first_name": "Eleanor", "last_name": "Long", "number": 8},
    {"id": 86, "first_name": "John", "last_name": "Doe", "number": 8},
    {"id": 87, "first_name": "Hazel", "last_name": "Patterson", "number": 5},
    {"id": 88, "first_name": "Owen", "last_name": "Hughes", "number": 7},
    {"id": 89, "first_name": "Lila", "last_name": "Flores", "number": 6},
    {"id": 90, "first_name": "Gabriel", "last_name": "Washington", "number": 8},
    {"id": 91, "first_name": "Ellie", "last_name": "Butler", "number": 9},
    {"id": 92, "first_name": "John", "last_name": "Doe", "number": 15},
    {"id": 93, "first_name": "Paisley", "last_name": "Simmons", "number": 10},
    {"id": 94, "first_name": "Jayden", "last_name": "Foster", "number": 8},
    {"id": 95, "first_name": "Alice", "last_name": "Gonzalez", "number": 6},
    {"id": 96, "first_name": "Hudson", "last_name": "Bryant", "number": 5},
    {"id": 97, "first_name": "Avery", "last_name": "Alexander", "number": 9},
    {"id": 98, "first_name": "John", "last_name": "Doe", "number": 8},
    {"id": 99, "first_name": "Layla", "last_name": "Sanchez", "number": 7},
    {"id": 100, "first_name": "Ethan", "last_name": "Nelson", "number": 8},
]

test_cases = [
        ("number == 8", [d for d in data if d["number"] == 8]),  # noqa: PLR2004
        ("id == 1", [d for d in data if d["id"] == 1]),
        ("last_name == Wandack", [d for d in data if d["last_name"] == "Wandack"]),  # noqa: E501
    ]

def test_find_sync() -> None:
    """Test for sync find module."""
    db_name = "test_find_sync"
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

    for query, expected in test_cases:
        result = db.find(db_name, query)
        if result != expected:
            msg = (
            f"find() failed for query '{query}': "
            f"expected {expected}, got {result}"
        )
            raise ValueError(msg)


@pytest.mark.asyncio
async def test_find_async() -> None:
    """Test for async find module."""
    db_name = "test_find_async"
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

    for query, expected in test_cases:
        result = await db.find(db_name, query)
        if result != expected:
            msg = (
            f"find() failed for query '{query}': "
            f"expected {expected}, got {result}"
        )
            raise ValueError(msg)
