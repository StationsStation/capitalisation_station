# ------------------------------------------------------------------------------
#
#   Copyright 2021-2023 Valory AG
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""This module contains all the storing operations of the behaviours."""

import json
import os.path
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Any, Union, TypeVar, cast
from collections.abc import Callable

from packages.eightballer.skills.abstract_round_abci.io_.paths import create_pathdirs


StoredJSONType = Union[dict, list]
NativelySupportedSingleObjectType = StoredJSONType
NativelySupportedMultipleObjectsType = dict[str, NativelySupportedSingleObjectType]
NativelySupportedObjectType = Union[NativelySupportedSingleObjectType, NativelySupportedMultipleObjectsType]
NativelySupportedStorerType = Callable[[str, NativelySupportedObjectType, Any], None]
CustomObjectType = TypeVar("CustomObjectType")
CustomStorerType = Callable[[str, CustomObjectType, Any], None]
SupportedSingleObjectType = Union[NativelySupportedObjectType, CustomObjectType]
SupportedMultipleObjectsType = dict[str, SupportedSingleObjectType]
SupportedObjectType = Union[SupportedSingleObjectType, SupportedMultipleObjectsType]
SupportedStorerType = Union[NativelySupportedStorerType, CustomStorerType]
NativelySupportedJSONStorerType = Callable[[str, StoredJSONType | dict[str, StoredJSONType], Any], None]


class SupportedFiletype(Enum):
    """Enum for the supported filetypes of the IPFS interacting methods."""

    JSON = auto()


class AbstractStorer(ABC):
    """An abstract `Storer` class."""

    def __init__(self, path: str):
        """Initialize an abstract storer."""
        self._path = path
        # Create the dirs of the path if it does not exist.
        create_pathdirs(path)

    @abstractmethod
    def serialize_object(self, filename: str, obj: SupportedSingleObjectType, **kwargs: Any) -> dict[str, str]:
        """Store a single file."""

    def store(self, obj: SupportedObjectType, multiple: bool, **kwargs: Any) -> dict[str, str]:
        """Serialize one or multiple objects."""
        serialized_files: dict[str, str] = {}
        if multiple:
            if not isinstance(obj, dict):  # pragma: no cover
                msg = (
                    f"Cannot store multiple files of type {type(obj)}!"
                    f"Should be a dictionary of filenames mapped to their objects."
                )
                raise ValueError(msg)
            for filename, single_obj in obj.items():
                filename = os.path.join(self._path, filename)
                serialized_file = self.serialize_object(filename, single_obj, **kwargs)
                serialized_files.update(**serialized_file)
        else:
            serialized_file = self.serialize_object(self._path, obj, **kwargs)
            serialized_files.update(**serialized_file)
        return serialized_files


class JSONStorer(AbstractStorer):
    """A JSON file storer."""

    def serialize_object(self, filename: str, obj: NativelySupportedSingleObjectType, **kwargs: Any) -> dict[str, str]:
        """Serialize an object to JSON.

        :param filename: under which name the provided object should be serialized. Note that it will appear in IPFS with this name.
        :param obj: the object to store.
        :returns: a dict mapping the name to the serialized object.
        """
        if not any(isinstance(obj, type_) for type_ in (dict, list)):
            msg = f"`JSONStorer` cannot be used with a {type(obj)}! Only with a {StoredJSONType}"
            raise ValueError(  # pragma: no cover
                msg
            )
        try:
            serialized_object = json.dumps(obj, ensure_ascii=False, indent=4)
            return {filename: serialized_object}
        except (TypeError, OSError) as e:  # pragma: no cover
            raise OSError(str(e)) from e


class Storer(AbstractStorer):
    """Class which serializes objects."""

    def __init__(
        self,
        filetype: Any | None,
        custom_storer: CustomStorerType | None,
        path: str,
    ):
        """Initialize a `Storer`."""
        super().__init__(path)
        self._filetype = filetype
        self._custom_storer = custom_storer
        self._filetype_to_storer: dict[Enum, SupportedStorerType] = {
            SupportedFiletype.JSON: cast(NativelySupportedJSONStorerType, JSONStorer(path).serialize_object),
        }

    def serialize_object(self, filename: str, obj: NativelySupportedObjectType, **kwargs: Any) -> dict[str, str]:
        """Store a single object."""
        storer = self._get_single_storer_from_filetype()
        return storer(filename, obj, **kwargs)  # type: ignore

    def _get_single_storer_from_filetype(self) -> SupportedStorerType:
        """Get an object storer from a given filetype or keep a custom storer."""
        if self._filetype is not None:
            return self._filetype_to_storer[self._filetype]

        if self._custom_storer is not None:  # pragma: no cover
            return self._custom_storer

        msg = "Please provide either a supported filetype or a custom storing function."
        raise ValueError(  # pragma: no cover
            msg
        )
