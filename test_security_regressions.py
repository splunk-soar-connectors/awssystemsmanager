# Copyright (c) 2026 Splunk Inc.
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
from pathlib import Path


CONNECTOR_SOURCE = Path("awssystemsmanager_connector.py").read_text()


def test_execute_program_waits_for_terminal_invocation_status():
    assert "get_command_invocation" in CONNECTOR_SOURCE
    assert 'status in {"Success", "Cancelled", "TimedOut", "Failed"}' in CONNECTOR_SOURCE
    assert 'invocation.get("Status") == "Success" and invocation.get("ResponseCode") == 0' in CONNECTOR_SOURCE
    assert "time.sleep(10)" not in CONNECTOR_SOURCE


def test_command_polling_has_a_hard_timeout():
    assert "SSM_COMMAND_POLL_MAX_TIMEOUT_SECONDS" in CONNECTOR_SOURCE
    assert "Timed out waiting for the SSM command invocation to finish" in CONNECTOR_SOURCE
