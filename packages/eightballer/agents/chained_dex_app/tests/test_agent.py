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
"""Test the agent."""

import subprocess
from pathlib import Path

import pytest
from aea.test_tools.test_cases import AEATestCaseMany
from aea_test_autonomy.configurations import ANY_ADDRESS, DEFAULT_REQUESTS_TIMEOUT


AGENT_NAME = "chained_dex_app"
AUTHOR = "eightballer"
VERSION = "0.1.0"
DEFAULT_LAUNCH_TIMEOUT = 10
LAUNCH_SUCCEED_MESSAGE = "Start processing"


class TestAgentLaunch(
    AEATestCaseMany,
):
    """Test that the Agent launches."""

    IS_LOCAL = True
    capture_log = True
    cli_log_options = ["-v", "DEBUG"]
    package_registry_src_rel = Path(__file__).parent.parent.parent.parent.parent

    def test_run(self) -> None:
        """Run the ABCI skill."""
        agent_name = "base"
        self.fetch_agent(f"{AUTHOR}/{AGENT_NAME}:{VERSION}", agent_name, is_local=self.IS_LOCAL)
        self.set_agent_context(agent_name)
        self.generate_private_key("ethereum")
        self.generate_private_key("cosmos")
        self.add_private_key("ethereum", "ethereum_private_key.txt")
        self.add_private_key("cosmos", "cosmos_private_key.txt")
        self.invoke(
            "issue-certificates",
        )
        process = self.run_agent()
        is_running = self.is_running(process)
        assert is_running, "AEA not running within timeout!"

    @classmethod
    def is_running(cls, process: subprocess.Popen, timeout: int = DEFAULT_LAUNCH_TIMEOUT) -> bool:
        """
        Check if the AEA is launched and running (ready to process messages).

        :param process: agent subprocess.
        :param timeout: the timeout to wait for launch to complete
        :return: bool indicating status
        """
        missing_strings = cls.missing_from_output(process, (LAUNCH_SUCCEED_MESSAGE,), timeout, is_terminating=False)

        return missing_strings == []
