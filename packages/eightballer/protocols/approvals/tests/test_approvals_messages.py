#                                                                             --
#
#   Copyright 2025 eightballer
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
#                                                                             --

"""Test messages module for approvals protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
import os

import yaml
from aea.test_tools.test_protocol import BaseProtocolMessagesTestCase

from packages.eightballer.protocols.approvals.message import ApprovalsMessage
from packages.eightballer.protocols.approvals.custom_types import Approval, ErrorCode


def load_data(custom_type):
    """Load test data."""
    with open(f"{os.path.dirname(__file__)}/dummy_data.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)[custom_type]


class TestMessageApprovals(BaseProtocolMessagesTestCase):
    """Test for the 'approvals' protocol message."""

    MESSAGE_CLASS = ApprovalsMessage

    def build_messages(self) -> list[ApprovalsMessage]:  # type: ignore[override]
        """Build the messages to be used for testing."""
        return [
            ApprovalsMessage(
                performative=ApprovalsMessage.Performative.SET_APPROVAL,
                approval=Approval(**load_data("Approval")),  # check it please!
            ),
            ApprovalsMessage(
                performative=ApprovalsMessage.Performative.GET_APPROVAL,
                approval=Approval(**load_data("Approval")),  # check it please!
            ),
            ApprovalsMessage(
                performative=ApprovalsMessage.Performative.APPROVAL_RESPONSE,
                approval=Approval(**load_data("Approval")),  # check it please!
            ),
            ApprovalsMessage(
                performative=ApprovalsMessage.Performative.ERROR,
                error_code=ErrorCode(0),  # check it please!
                error_msg="some str",
                error_data={"some str": b"some_bytes"},
            ),
        ]

    def build_inconsistent(self):
        """Build inconsistent message."""
        return []
