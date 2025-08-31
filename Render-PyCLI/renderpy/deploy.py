import typer
from rich.console import Console
from .client import api_request

deploy = typer.Typer(help="Manage deployments")
console = Console()

@deploy.command("create")
def create(service_id: str, branch: str = "main", clear_cache: bool = False):
    """Trigger a new deployment for a service"""
    body = {"branch": branch, "clearCache": clear_cache}
    try:
        result = api_request("POST", f"services/{service_id}/deploys", json=body)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(code=1)

    deploy_id = result.get("id", "<unknown>")
    console.print(f"[green]Deploy started[/green] id={deploy_id}")

@deploy.command("list")
def list_deploys(service_id: str):
    """List deploys for a service"""
    try:
        data = api_request("GET", f"services/{service_id}/deploys")
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(code=1)

    for d in data:
        console.print(f"{d.get('id')}  {d.get('status')}  {d.get('createdAt')}")

@app.command("create")
def create_deploy(
    service_id: str,
    branch: str = typer.Option("main", "--branch", help="Git branch"),
    clear_cache: bool = typer.Option(False, "--clear-cache", help="Clear build cache"),
    json: bool = typer.Option(False, "--json", help="Output JSON"),
):
    """Trigger a new deploy for a service"""
    payload = {"branch": branch, "clearCache": clear_cache}
    data = api_request("POST", f"/services/{service_id}/deploys", json=payload)

    if json:
        console.print_json(data)
        return

    table = Table(show_header=True, header_style="bold cyan", title="Deploy Created", show_lines=True)
    table.add_column("Field", style="bold magenta")
    table.add_column("Value", style="white")
    for k, v in data.items():
        table.add_row(str(k), str(v))
    console.print(table)