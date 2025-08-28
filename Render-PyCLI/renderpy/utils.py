import click, typer

RENDER_API_BASE = "https://api.render.com/v1"
_api_key = None

def require_api_key():
    global _api_key
    if not _api_key:
        _api_key = typer.prompt("🔑 Enter your Render API key")
        if not _api_key:
            click.secho("❌ No API key provided.", fg="red")
            raise SystemExit(1)
    return _api_key
