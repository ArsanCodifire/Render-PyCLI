import typer
from rich.console import Console
from .client import api_request

deploy = typer.Typer(help="Manage deployments")
console = Console()

@deploy.command("create")
def create(service_id: str, branch: str = "main", clear_cache: bool = False, json: bool = False):
    """Trigger a new deployment for a service"""
    body = {"branch": branch, "clearCache": clear_cache}
    try:
        result = api_request("POST", f"services/{service_id}/deploys", json=body)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(code=1)
    
    if json:
        console.print_json(data)
        return
        
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
