# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2024 eightballer
#   Copyright 2022-2023 Valory AG
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
# pylint: disable=unused-import
from pathlib import Path

import pytest

TARGET_AGENT = "eightballer/chained_dex_app:0.1.0"
TARGET_SKILL = "eightballer/chined_dex_app:0.1.0"
TIME_TO_FINISH = 60  # 1 minute


@pytest.mark.integration
@pytest.mark.skip(reason="Integration tests are not yet implemented.")
def test_integration():
    """Test the integration."""
    pytest.skip("Integration tests are not yet implemented.")

