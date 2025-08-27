import typer
from rich.console import Console
from rich.table import Table
from .client import api_request

services = typer.Typer(help="Manage Render services")
console = Console()

@services.command("list")
def list_services():
    """List Render services"""
    try:
        data = api_request("GET", "services")
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(code=1)

    if not isinstance(data, list):
        console.print(data)
        return

    t = Table(title="Render Services")
    t.add_column("ID", style="cyan", no_wrap=True)
    t.add_column("Name", style="green")
    t.add_column("Type", style="magenta")
    t.add_column("Status", style="yellow")

    for s in data:
        sid = s.get("id", "")
        sdetails = s.get("serviceDetails", {}) or {}
        name = sdetails.get("name") or s.get("name") or ""
        stype = sdetails.get("type") or s.get("type") or ""
        status = s.get("status", "")
        t.add_row(sid, name, stype, status)

    console.print(t)

@services.command("info")
def service_info(service_id: str):
    """Show service info"""
    try:
        d = api_request("GET", f"services/{service_id}")
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(code=1)

    console.print(d)