import click
import typer
import os

RENDER_API_BASE = "https://api.render.com/v1"
API_KEY_FILE = os.path.expanduser("~/.renderpy_api_key")

def save_api_key(key: str):
    """Saves the API key to a file."""
    with open(API_KEY_FILE, "w") as f:
        f.write(key)

def load_api_key():
    """Loads the API key from a file."""
    if os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, "r") as f:
            return f.read().strip()
    return None

def require_api_key():
    """Ensures an API key is available."""
    api_key = load_api_key()
    if not api_key:
        click.secho("❌ No API key found. Please run 'renderpy login' to set your key.", fg="red")
        raise typer.Exit(code=1)
    return api_key
