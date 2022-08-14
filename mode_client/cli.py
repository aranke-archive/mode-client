import typer
from dotenv import load_dotenv
from rich.console import Console

from mode_client import ModeClient

load_dotenv()
console = Console()
app = typer.Typer(no_args_is_help=True, rich_markup_mode="rich")


def account_callback():
    """\b
    [cyan bold]get[/cyan bold] --account <account>
    """


account_app = typer.Typer(no_args_is_help=True, rich_markup_mode="rich")
app.add_typer(account_app, name="account", callback=account_callback)


@account_app.command("get")
def account_get(
    account: str = typer.Option(..., prompt=True),
    workspace: str = typer.Option(
        ..., envvar="MODE_WORKSPACE", show_envvar=False, prompt=True
    ),
    token: str = typer.Option(..., envvar="MODE_TOKEN", show_envvar=False, prompt=True),
    password: str = typer.Option(
        ..., envvar="MODE_PASSWORD", show_envvar=False, prompt=True
    ),
):
    """--account <account>"""
    client = ModeClient(workspace, token, password)
    response = client.account.get(account)
    console.print_json(response.json())


def space_callback():
    """\b
    [cyan bold]get[/cyan bold] --space <space>
    [cyan bold]list[/cyan bold] [--filter <all|custom>]
    [cyan bold]create[/cyan bold] --name <name> --description <description>
    [cyan bold]update[/cyan bold] --space <space> --name <name> --description <description>
    [cyan bold]delete[/cyan bold] --space <space> [--force]
    """


space_app = typer.Typer(no_args_is_help=True, rich_markup_mode="rich")
app.add_typer(space_app, name="space", callback=space_callback)


@space_app.command("get")
def space_get(
    space: str = typer.Option(..., prompt=True),
    workspace: str = typer.Option(
        ..., envvar="MODE_WORKSPACE", show_envvar=False, prompt=True
    ),
    token: str = typer.Option(..., envvar="MODE_TOKEN", show_envvar=False, prompt=True),
    password: str = typer.Option(
        ..., envvar="MODE_PASSWORD", show_envvar=False, prompt=True
    ),
):
    """--space <space>"""
    client = ModeClient(workspace, token, password)
    response = client.space.get(space)
    console.print_json(response.json())


@space_app.command("list")
def space_list(
    filter_: str = typer.Option("custom"),
    workspace: str = typer.Option(
        ..., envvar="MODE_WORKSPACE", show_envvar=False, prompt=True
    ),
    token: str = typer.Option(..., envvar="MODE_TOKEN", show_envvar=False, prompt=True),
    password: str = typer.Option(
        ..., envvar="MODE_PASSWORD", show_envvar=False, prompt=True
    ),
):
    """[--filter <all|custom>]"""
    client = ModeClient(workspace, token, password)
    response = client.space.list(filter_)
    console.print_json(data=[s.dict() for s in response])


@space_app.command("create")
def space_create(
    name: str = typer.Option(..., prompt=True),
    description: str = typer.Option(..., prompt=True),
    workspace: str = typer.Option(
        ..., envvar="MODE_WORKSPACE", show_envvar=False, prompt=True
    ),
    token: str = typer.Option(..., envvar="MODE_TOKEN", show_envvar=False, prompt=True),
    password: str = typer.Option(
        ..., envvar="MODE_PASSWORD", show_envvar=False, prompt=True
    ),
):
    """--name <name> --description <description>"""
    client = ModeClient(workspace, token, password)
    response = client.space.create(name, description)
    console.print_json(response.json())


@space_app.command("update")
def space_update(
    space: str = typer.Option(..., prompt=True),
    name: str = typer.Option(..., prompt=True),
    description: str = typer.Option(..., prompt=True),
    workspace: str = typer.Option(
        ..., envvar="MODE_WORKSPACE", show_envvar=False, prompt=True
    ),
    token: str = typer.Option(..., envvar="MODE_TOKEN", show_envvar=False, prompt=True),
    password: str = typer.Option(
        ..., envvar="MODE_PASSWORD", show_envvar=False, prompt=True
    ),
):
    """--space <space> --name <name> --description <description>"""
    client = ModeClient(workspace, token, password)
    response = client.space.update(space, name, description)
    console.print_json(response.json())


@space_app.command("delete")
def space_delete(
    space: str = typer.Option(..., prompt=True),
    force: bool = typer.Option(False),
    workspace: str = typer.Option(
        ..., envvar="MODE_WORKSPACE", show_envvar=False, prompt=True
    ),
    token: str = typer.Option(..., envvar="MODE_TOKEN", show_envvar=False, prompt=True),
    password: str = typer.Option(
        ..., envvar="MODE_PASSWORD", show_envvar=False, prompt=True
    ),
):
    """--space <space> [--force]"""
    client = ModeClient(workspace, token, password)
    response = client.space.delete(space)
    console.print_json(response.json())


def query_callback():
    """\b
    [cyan bold]get[/cyan bold] --report <report> --query <query>
    [cyan bold]list[/cyan bold] --report <report>
    [cyan bold]create[/cyan bold] --report <report> --raw-query <raw_query> --data-source-id <data_source_id> --name <name>
    [cyan bold]update[/cyan bold] --report <report> --query <query> --raw-query <raw_query> --data-source_id <data_source_id> --name <name>
    """


query_app = typer.Typer(no_args_is_help=True, rich_markup_mode="rich")
app.add_typer(query_app, name="query", callback=query_callback)


@query_app.command("get")
def query_get(
    report: str = typer.Option(..., prompt=True, help="--report <report>"),
    query: str = typer.Option(..., prompt=True, help="--query <query>"),
    workspace: str = typer.Option(
        ..., envvar="MODE_WORKSPACE", show_envvar=False, prompt=True
    ),
    token: str = typer.Option(..., envvar="MODE_TOKEN", show_envvar=False, prompt=True),
    password: str = typer.Option(
        ..., envvar="MODE_PASSWORD", show_envvar=False, prompt=True
    ),
):
    """--report <report> --query <query>"""
    client = ModeClient(workspace, token, password)
    response = client.query.get(report, query)
    console.print_json(response.json())


@query_app.command("list")
def query_list(
    report: str = typer.Option(..., prompt=True),
    workspace: str = typer.Option(
        ..., envvar="MODE_WORKSPACE", show_envvar=False, prompt=True
    ),
    token: str = typer.Option(..., envvar="MODE_TOKEN", show_envvar=False, prompt=True),
    password: str = typer.Option(
        ..., envvar="MODE_PASSWORD", show_envvar=False, prompt=True
    ),
):
    """--report <report>"""
    client = ModeClient(workspace, token, password)
    response = client.query.list(report)
    console.print_json(data=[q.dict() for q in response])


@query_app.command("create")
def query_create(
    report: str = typer.Option(..., prompt=True),
    raw_query: str = typer.Option(..., prompt=True),
    data_source_id: int = typer.Option(..., prompt=True),
    name: str = typer.Option(..., prompt=True),
    workspace: str = typer.Option(
        ..., envvar="MODE_WORKSPACE", show_envvar=False, prompt=True
    ),
    token: str = typer.Option(..., envvar="MODE_TOKEN", show_envvar=False, prompt=True),
    password: str = typer.Option(
        ..., envvar="MODE_PASSWORD", show_envvar=False, prompt=True
    ),
):
    """--report <report> --raw-query <raw_query> --data-source-id <data_source_id> --name <name>"""
    client = ModeClient(workspace, token, password)
    response = client.query.create(report, raw_query, data_source_id, name)
    console.print_json(response.json())


@query_app.command("update")
def query_update(
    report: str = typer.Option(..., prompt=True),
    query: str = typer.Option(..., prompt=True),
    raw_query: str = typer.Option(..., prompt=True),
    data_source_id: int = typer.Option(..., prompt=True),
    name: str = typer.Option(..., prompt=True),
    workspace: str = typer.Option(
        ..., envvar="MODE_WORKSPACE", show_envvar=False, prompt=True
    ),
    token: str = typer.Option(..., envvar="MODE_TOKEN", show_envvar=False, prompt=True),
    password: str = typer.Option(
        ..., envvar="MODE_PASSWORD", show_envvar=False, prompt=True
    ),
):
    """--report <report> --query <query> --raw-query <raw_query> --data-source_id <data_source_id> --name <name>"""
    client = ModeClient(workspace, token, password)
    response = client.query.update(report, query, raw_query, data_source_id, name)
    console.print_json(response.json())


@query_app.command("delete")
def query_delete(
    report: str = typer.Option(..., prompt=True),
    query: str = typer.Option(..., prompt=True),
    force: bool = typer.Option(False),
    workspace: str = typer.Option(
        ..., envvar="MODE_WORKSPACE", show_envvar=False, prompt=True
    ),
    token: str = typer.Option(..., envvar="MODE_TOKEN", show_envvar=False, prompt=True),
    password: str = typer.Option(
        ..., envvar="MODE_PASSWORD", show_envvar=False, prompt=True
    ),
):
    if force or typer.confirm(f"Are you sure you want to delete query {query}?"):
        client = ModeClient(workspace, token, password)
        client.query.delete(report, query)
        console.print(f"[yellow]Query {query} deleted.[/yellow]")
    else:
        raise typer.Abort()


def main():
    app()


if __name__ == "__main__":
    app()
