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

"""Eror DataIsUncorrectError."""

from typing import Any


class DataIsUncorrectError(Exception):
    """Error DataIsUncorrectError.

    Parameters
    ----------
    Exception : _type_
        Base exception
    """

    def __init__(self, data: dict[str, Any]) -> None:
        """Init.

        Parameters
        ----------
        table_name : str
            name of table, when noot found
        """
        self.data = data
        super().__init__(f"Data is uncorrect, data: '{data}'.")

    def __str__(self) -> str:
        """Print Exception.

        Returns
        -------
        str
            String info message
        """
        return f"Error: Data is uncorrect {self.data}"
