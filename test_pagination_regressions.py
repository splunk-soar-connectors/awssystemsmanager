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
