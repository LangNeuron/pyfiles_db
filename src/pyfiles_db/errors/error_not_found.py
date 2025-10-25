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

"""Eror DbNotLoadedError."""

class NotFoundTableError(Exception):
    """Error NotFoundError.

    Parameters
    ----------
    Exception : _type_
        Base exception
    """

    def __init__(self, table_name: str) -> None:
        """Init.

        Parameters
        ----------
        table_name : str
            name of table, when noot found
        """
        self.table_name = table_name
        super().__init__(f"Table '{table_name}' not found.")

    def __str__(self) -> str:
        """Print Exception.

        Returns
        -------
        str
            String info message
        """
        return f"ERROR: TABLE **'{self.table_name}'** not found"

class NotFoundColumnError(Exception):
    """Error NotFoundError.

    Parameters
    ----------
    Exception : _type_
        Base exception
    """

    def __init__(self, column_name: str, table_name: str) -> None:
        """Init.

        Parameters
        ----------
        table_name : str
            name of table, when noot found
        """
        self.column_name = column_name
        self.table_name = table_name
        super().__init__(f"Column '{column_name}' not found in {table_name}.")

    def __str__(self) -> str:
        """Print Exception.

        Returns
        -------
        str
            String info message
        """
        return f"Column '{self.column_name}' not found in {self.table_name}."
