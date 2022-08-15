import os

import pytest
from dotenv import load_dotenv

from mode_client import ModeClient


@pytest.fixture
def client():
    load_dotenv()
    return ModeClient(
        os.getenv("MODE_WORKSPACE"), os.getenv("MODE_TOKEN"), os.getenv("MODE_PASSWORD")
    )


def test_account(client):
    account = client.account.get("mode_client")
    assert account.username == "mode_client"


def test_space_list(client):
    custom_spaces = client.space.list()
    assert set(s.space_type for s in custom_spaces) == {"custom"}
    assert set(s.name for s in custom_spaces) == {"Mode Client"}

    all_spaces = client.space.list("all")
    assert set(s.space_type for s in all_spaces) == {"private", "custom"}
    assert set(s.name for s in all_spaces) == {"Mode Client", "Personal"}


def test_space_get(client):
    spaces = client.space.list()
    space = client.space.get(spaces[0].token)
    assert space.name == "Mode Client"


def test_report_list_space(client):
    spaces = client.space.list()
    space = spaces[0].token

    reports = client.report.list(space=space)
    assert set(r.token for r in reports) == {"8772ad79bc3f"}


def test_report_get(client):
    report = client.report.get("8772ad79bc3f")
    assert report.name == "Dunder Mifflin"
    assert report.description == "A dashboard showing Dunder Mifflin sales"
    assert report.type == "Report"
    assert report.account_username == "mode_client"
    assert report.chart_count == 2
    assert report.query_count == 1
    assert report.archived is False


def test_report_archive(client):
    report = client.report.get("8772ad79bc3f")
    assert report.archived is False

    client.report.archive("8772ad79bc3f")
    report = client.report.get("8772ad79bc3f")
    assert report.archived is True

    client.report.unarchive("8772ad79bc3f")
    report = client.report.get("8772ad79bc3f")
    assert report.archived is False
