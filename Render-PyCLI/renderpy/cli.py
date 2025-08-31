import typer
from .services import services
from .deploy import deploy
from .logs import logs
from .utils import save_api_key, require_api_key

app = typer.Typer(help="Render-PyCLI (Typer + Textual + httpx)")

# Add a login command to handle API key entry
@app.command("login")
def login_command():
    """Prompts for and saves your Render API key."""
    key = typer.prompt("🔑 Enter your Render API key:", hide_input=True)
    save_api_key(key)
    typer.echo("✅ API key saved successfully!")

app.add_typer(services, name="services")
app.add_typer(deploy, name="deploy")
app.add_typer(logs, name="logs")

if __name__ == "__main__":
    app()
