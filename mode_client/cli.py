import typer
from environs import Env
from rich.console import Console

from mode_client import ModeClient

env = Env()
env.read_env()
workspace = env("MODE_WORKSPACE")
token = env("MODE_TOKEN")
password = env("MODE_PASSWORD")
client = ModeClient(workspace, token, password)

app = typer.Typer()
console = Console()

account_app = typer.Typer()
app.add_typer(account_app, name="account")


@account_app.command("get")
def account_get(account: str = typer.Option(workspace)):
    response = client.account.get(account)
    console.print_json(response.json())


query_app = typer.Typer()
app.add_typer(query_app, name="query")


@query_app.command("get")
def get(report: str = typer.Option(...), query: str = typer.Option(...)):
    response = client.query.get(report, query)
    console.print_json(response.json())


@query_app.command("list")
def list_(report: str = typer.Option(...)):
    response = client.query.list(report)
    console.print_json(data=[q.dict() for q in response])


@query_app.command("create")
def create(
    report: str = typer.Option(...),
    raw_query: str = typer.Option(...),
    data_source_id: int = typer.Option(...),
    name: str = typer.Option(...),
):
    response = client.query.create(report, raw_query, data_source_id, name)
    console.print_json(response.json())


@query_app.command("update")
def update(
    report: str = typer.Option(...),
    query: str = typer.Option(...),
    raw_query: str = typer.Option(...),
    data_source_id: int = typer.Option(...),
    name: str = typer.Option(...),
):
    response = client.query.update(report, query, raw_query, data_source_id, name)
    console.print_json(response.json())


@query_app.command("delete")
def delete(
    report: str = typer.Option(...),
    query: str = typer.Option(...),
    force: bool = typer.Option(False),
):
    if force or typer.confirm(f"Are you sure you want to delete query {query}?"):
        client.query.delete(report, query)
        console.print(f"[yellow]Query {query} deleted.[/yellow]")
    else:
        raise typer.Abort()


def main():
    app()


if __name__ == "__main__":
    app()
