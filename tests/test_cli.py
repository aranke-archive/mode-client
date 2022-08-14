import json

import pytest
from dotenv import load_dotenv
from typer.testing import CliRunner

from mode_client.cli import app

runner = CliRunner()


@pytest.fixture
def dotenv():
    load_dotenv()


def test_account(dotenv):
    r1 = runner.invoke(app, ["account", "get", "--account", "mode_client"])
    assert r1.exit_code == 0

    o1 = json.loads(r1.output)
    assert o1["username"] == "mode_client"


def test_space(dotenv):
    r1 = runner.invoke(app, ["space", "list"])
    assert r1.exit_code == 0

    o1 = json.loads(r1.output)
    assert len(o1) == 1
    assert o1[0]["name"] == "Mode Client"

    r2 = runner.invoke(app, ["space", "get", "--space", o1[0]["token"]])
    assert r2.exit_code == 0

    o2 = json.loads(r2.output)
    assert o2["name"] == "Mode Client"
