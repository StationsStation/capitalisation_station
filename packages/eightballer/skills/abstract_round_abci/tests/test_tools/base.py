# ------------------------------------------------------------------------------
#
#   Copyright 2023 Valory AG
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

"""Tests for abstract_round_abci/test_tools/common.py."""

from typing import Any, cast
from pathlib import Path

from aea.helpers.base import cd
from aea.test_tools.utils import copy_class

from packages.eightballer.skills.abstract_round_abci.base import BaseTxPayload, _MetaPayload
from packages.eightballer.skills.abstract_round_abci.test_tools.base import (
    FSMBehaviourBaseCase,
)
from packages.eightballer.skills.abstract_round_abci.tests.data.dummy_abci import (
    PATH_TO_SKILL,
)


class FSMBehaviourTestToolSetup:
    """BaseRandomnessBehaviourTestSetup."""

    test_cls: type[FSMBehaviourBaseCase]
    __test_cls: type[FSMBehaviourBaseCase]
    __old_value: dict[str, type[BaseTxPayload]]

    @classmethod
    def setup_class(cls) -> None:
        """Setup class."""

        if not hasattr(cls, "test_cls"):
            msg = f"{cls} must set `test_cls`"
            raise AttributeError(msg)

        cls.__test_cls = cls.test_cls
        cls.__old_value = _MetaPayload.registry.copy()
        _MetaPayload.registry.clear()

    @classmethod
    def teardown_class(cls) -> None:
        """Teardown class."""
        _MetaPayload.registry = cls.__old_value

    def setup(self) -> None:
        """Setup test."""
        test_cls = copy_class(self.__test_cls)
        self.test_cls = cast(type[FSMBehaviourBaseCase], test_cls)

    def teardown(self) -> None:
        """Teardown test."""
        self.test_cls.teardown_class()

    def set_path_to_skill(self, path_to_skill: Path = PATH_TO_SKILL) -> None:
        """Set path_to_skill."""
        self.test_cls.path_to_skill = path_to_skill

    def setup_test_cls(self, **kwargs: Any) -> FSMBehaviourBaseCase:
        """Helper method to setup test to be tested."""

        # different test tools will require the setting of
        # different class attributes (such as path_to_skill).
        # One should write a test that sets these,
        # and subsequently invoke this method to test the setup.

        with cd(self.test_cls.path_to_skill):
            self.test_cls.setup_class(**kwargs)

        test_instance = self.test_cls()
        test_instance.setup()
        return test_instance
