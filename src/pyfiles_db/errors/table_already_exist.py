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

"""Errors for table already exists condition."""

class TableAlreadyAvaibleError(Exception):
    """Raised when trying to create a table that already exists.

    Note: class name preserves historical spelling for backward
    compatibility with existing code and tests.
    """

    def __str__(self) -> str:
        """Return a readable message for this exception."""
        return "Table already available"
