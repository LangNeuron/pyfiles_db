# pyfiles_db  
Lightweight file-system database for Python projects

```
PRE RELISE FIRST VERSION OF PYFILES_D
```

## About  
`pyfiles_db` is a lightweight and fast library that allows using the file system as a database for Python projects. It is minimalistic, requires no full-fledged DBMS, and is ideal for small to medium projects where simplicity and speed are priorities, and when system resources are a concern. It is built on top of `aiofiles` which allows you to use the file system as a database without any server required. Also can with synchronous mode.

## Features  
- Store data directly in folders and files (no server required)
- Simple API — quick to start
- Supports basic CRUD operations: Create, Read, Update, Delete
- Minimal external dependencies
- Designed for easy integration and flexibility

## Installation  
```bash
pip install python-files-db
```


## Quick Start

```python
from pyfiles_db import FilesDB

file_db = FilesDB()

db = file_db.init_async()  # Or file_db.init_sync() for sync mode
# storage - path to database location, if is None use default path.

db.craeate_table(
    "users",
    columns={
        "id": "INT",
        "name": "TEXT",
        "age": "INT",
    },
    id_generator="id", # required unical value of table, if None use generator for auto increment.
)

db.new_data(table_name="usesr", data={
    "id": 1,
    "name": "Anton",
    "age": 17,
})

db.new_data(table_name="users", data={
    "id": 2,
    "name": "Alex",
    "age": 17,
})

user_id_1 = db.find("usesr", "id == 1")
# return [{"1": {"id": 1, "name": "Anton", "age": 17}}]

user_id_2 = db.find("usesr", "id == 2") 
# return [{"2": {"id": 2, "name": "Alex", "age": 17}}]

users_age_17 = db.find("users", "age == 17")
# return [
#     {"1": {"id": 1, "name": "Anton", "age": 17}},
#     {"2": {"id": 2, "name": "Alex", "age": 17},
# ]

```

## Use Cases
- Quick startups, prototypes, MVPs
- Lightweight web applications, scripts, utilities
- Projects not requiring a heavy DBMS
- Personal projects and data analysis tools
- low RAM and processor characteristics

## Best Practices & Limitations
- Not designed for high-load systems with thousands of requests per second
- Maintain folder structure carefully to avoid naming collisions
- As this uses the file system, consider transaction/concurrency limitations
- Regularly back up the path folder

## Contribution
Feedback, issues, and pull requests are welcome!
Follow the contribution guidelines if available.
Ensure your code is tested (tests in /tests/) and document changes.

## License
This project is licensed under the Apache-2.0 License. See [LICENSE](https://github.com/LangNeuron/pyfiles_db/blob/main/LICENSE) for details.

## Other

### [CODE_OF_CONDUCT](https://github.com/LangNeuron/pyfiles_db/blob/main/CODE_OF_CONDUCT.md)

### [CONTRIBUTING](https://github.com/LangNeuron/pyfiles_db/blob/main/CONTRIBUTING.md)
