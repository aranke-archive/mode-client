import os

import pytest

from mode_client import ModeClient


@pytest.fixture
def mode_client():
    workspace = "modeanalytics"
    token = os.getenv("MODE_TOKEN")
    password = os.getenv("MODE_PASSWORD")
    return ModeClient(workspace, token, password)


@pytest.fixture()
def report_id():
    return "1a11685d6ab2"


def test_account_organization(mode_client):
    user = mode_client.account.get("modeanalytics")
    assert user.user is False
    assert user.token == '22aa79951300'


def test_account_user(mode_client):
    user = mode_client.account.get("benn")
    assert user.user is True
    assert user.token == '5ab1de2572d6'


def test_space(mode_client):
    spaces = mode_client.space.list()
    assert len(spaces) == 1
    assert spaces[0].token == "dc62aa50fae5"


def test_report(mode_client, report_id):
    report = mode_client.report.get(report_id)
    assert report.account_username == "modeanalytics"


def test_report_run(mode_client, report_id):
    report_runs = mode_client.report_run.list(report_id)
    assert report_runs.report_runs[0].is_latest_report_run is True


def test_query(mode_client, report_id):
    queries = mode_client.query.list(report_id)
    assert len(queries) == 1
    assert queries[0].token == '48062b54257b'


def test_query_run(mode_client, report_id):
    report_run = mode_client.report.get(report_id).last_successful_run_token

    query_runs = mode_client.query_run.list(report_id, report_run)
    assert len(query_runs) == 1
    assert query_runs[0].raw_source == query_runs[0].rendered_source
