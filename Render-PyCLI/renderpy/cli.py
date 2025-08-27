import typer
from .services import services
from .deploy import deploy
from .logs import logs

app = typer.Typer(help="Render-PyCLI (Typer + Textual + httpx)")

app.add_typer(services, name="services")
app.add_typer(deploy, name="deploy")
app.add_typer(logs, name="logs")

if __name__ == "__main__":
    app()