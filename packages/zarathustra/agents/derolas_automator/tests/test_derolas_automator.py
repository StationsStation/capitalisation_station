# ------------------------------------------------------------------------------
#
#   Copyright 2025 zarathustra
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

"""Integration tests for the Derolas Automator agent."""

from pathlib import Path

import yaml
from aea.test_tools.test_cases import AEATestCaseMany


THIS_FILE = Path(__file__)
DEFAULT_LAUNCH_TIMEOUT = 10


class TestAgentLaunch(AEATestCaseMany):
    """Test that the agent launches."""

    IS_LOCAL = True
    capture_log = True
    cli_log_options = ["-v", "DEBUG"]
    package_registry_src_rel = Path(__file__).parent.parent.parent.parent.parent

    def install(self) -> None:
        """Install the agent."""

        aea_config = THIS_FILE.parent.parent / "aea-config.yaml"
        yamls = list(yaml.safe_load_all(aea_config.read_text()))
        agent_name = yamls[0]["agent_name"]
        author = yamls[0]["author"]
        version = yamls[0]["version"]

        self.fetch_agent(f"{author}/{agent_name}:{version}", agent_name, is_local=self.IS_LOCAL)
        self.set_agent_context(agent_name)
        self.generate_private_key("ethereum")
        self.add_private_key("ethereum", "ethereum_private_key.txt")
        self.invoke("issue-certificates")
        self.invoke("install")

    def test_run(self) -> None:
        """Run the agent."""

        self.install()
        process = self.run_agent()
        first_round = "AwaitTriggerRound"
        missing_strings = self.missing_from_output(
            process, (first_round,), DEFAULT_LAUNCH_TIMEOUT, is_terminating=False
        )
        assert not missing_strings
