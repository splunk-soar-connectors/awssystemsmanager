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
CONSTANTS_SOURCE = Path("awssystemsmanager_consts.py").read_text()


def test_pagination_has_page_and_item_limits():
    assert "SSM_MAX_PAGINATION_PAGES = 1000" in CONSTANTS_SOURCE
    assert "SSM_MAX_PAGINATION_ITEMS = 100000" in CONSTANTS_SOURCE
    assert CONNECTOR_SOURCE.count("page_count >= SSM_MAX_PAGINATION_PAGES") == 2
    assert CONNECTOR_SOURCE.count("in seen_tokens") == 2


def test_pagination_does_not_mutate_action_parameters():
    assert 'param["next_token"] =' not in CONNECTOR_SOURCE
