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

"""This package contains payload tests for the AbciApp."""

from dataclasses import dataclass
from collections.abc import Hashable

import pytest

from packages.eightballer.skills.dex_data_retrieval.payloads import BaseTxPayload


@dataclass
class PayloadTestCase:
    """PayloadTestCase."""

    name: str
    payload_cls: type[BaseTxPayload]
    content: Hashable


@pytest.mark.parametrize("test_case", [])
def test_payloads(test_case: PayloadTestCase) -> None:
    """Tests for AbciApp payloads."""

    payload = test_case.payload_cls(sender="sender", content=test_case.content)
    assert payload.sender == "sender"
    assert payload.from_json(payload.json) == payload
