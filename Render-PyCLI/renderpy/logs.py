import asyncio
import typer
from textual.app import App, ComposeResult
from textual.scroll_view import ScrollView
from textual.reactive import static
from .client import get_async_client, api_request

logs = typer.Typer(help="Manage service logs (Textual TUI)")

class LogsApp(App):
    """Textual app that streams logs for a Render service."""

    CSS = """
    Screen {background: #1e1e2e; color: white;}
    ScrollView {border: round yellow;}
    """
    scroll_content: str = static("")

    def __init__(self, service_id: str, poll_interval: float = 2.0):
        super().__init__()
        self.service_id = service_id
        self.poll_interval = poll_interval

    def compose(self) -> ComposeResult:
        self.scroll = ScrollView()
        yield self.scroll

    async def on_mount(self):
        self.set_interval(self.poll_interval, self.fetch_and_append)

    async def fetch_and_append(self):
        try:
            async with get_async_client() as client:
                r = await client.get(f"services/{self.service_id}/logs")
                r.raise_for_status()
                data = await r.json()
        except Exception as e:
            self.scroll_content += f"[red]Error fetching logs: {e}[/red]\n"
            await self.scroll.update(self.scroll_content)
            return

        logs_list = data if isinstance(data, list) else data.get("logs", [])
        text = ""
        for entry in logs_list:
            ts = entry.get("timestamp") or entry.get("createdAt") or ""
            msg = entry.get("message") or entry.get("msg") or entry.get("text") or ""
            text += f"[cyan]{ts}[/cyan] {msg}\n"

        if text:
            self.scroll_content += text
            await self.scroll.update(self.scroll_content)
            await self.scroll.scroll_to_end()

@logs.command("view")
def view_logs(service_id: str, stream: bool = typer.Option(False, "--stream", help="Stream live logs")):
    """View logs for a service. Use --stream for live TUI."""
    if stream:
        LogsApp(service_id=service_id).run()
    else:
        try:
            data = api_request("GET", f"services/{service_id}/logs")
        except Exception as e:
            typer.echo(f"[red]Error fetching logs:[/red] {e}")
            raise typer.Exit(code=1)

        logs_list = data if isinstance(data, list) else data.get("logs", [])
        for entry in logs_list:
            ts = entry.get("timestamp") or entry.get("createdAt") or ""
            msg = entry.get("message") or entry.get("msg") or entry.get("text") or ""
            typer.echo(f"{ts} {msg}")