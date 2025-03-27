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

"""This module contains all the interaction operations of the behaviours with IPFS."""

import os
from typing import Any

from packages.eightballer.skills.abstract_round_abci.io_.load import (
    Loader,
    CustomLoaderType,
    SupportedFiletype,
    SupportedObjectType,
)
from packages.eightballer.skills.abstract_round_abci.io_.store import (
    Storer,
    CustomStorerType,
)


class IPFSInteractionError(Exception):
    """A custom exception for IPFS interaction errors."""


class IPFSInteract:
    """Class for interacting with IPFS."""

    def __init__(self, loader_cls: type = Loader, storer_cls: type = Storer):
        """Initialize an `IPFSInteract` object."""
        # Set loader/storer class.
        self._loader_cls = loader_cls
        self._storer_cls = storer_cls

    def store(
        self,
        filepath: str,
        obj: SupportedObjectType,
        multiple: bool,
        filetype: SupportedFiletype | None = None,
        custom_storer: CustomStorerType | None = None,
        **kwargs: Any,
    ) -> dict[str, str]:
        """Temporarily store a file locally, in order to send it to IPFS and retrieve a hash, and then delete it."""
        filepath = os.path.normpath(filepath)
        if multiple:
            # Add trailing slash in order to treat path as a folder.
            filepath = os.path.join(filepath, "")
        storer = self._storer_cls(filetype, custom_storer, filepath)

        try:
            return storer.store(obj, multiple, **kwargs)
        except Exception as e:  # pylint: disable=broad-except
            raise IPFSInteractionError(str(e)) from e

    def load(  # pylint: disable=too-many-arguments
        self,
        serialized_objects: dict[str, str],
        filetype: SupportedFiletype | None = None,
        custom_loader: CustomLoaderType = None,
    ) -> SupportedObjectType:
        """Deserialize objects received via IPFS."""
        loader = self._loader_cls(filetype, custom_loader)
        try:
            return loader.load(serialized_objects)
        except Exception as e:  # pylint: disable=broad-except
            raise IPFSInteractionError(str(e)) from e
