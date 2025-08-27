import os
import click

RENDER_API_BASE = "https://api.render.com/v1"

def require_api_key():
    key = os.getenv("RENDER_API_KEY")
    if not key:
        click.secho("❌ RENDER_API_KEY environment variable not set.", fg="red")
        raise SystemExit(1)
    return key