import asyncio
import httpx
import typer
from textual.app import App, ComposeResult
from textual.scroll_view import ScrollView
from textual.reactive import var
from .client import get_async_client

logs = typer.Typer(help="Service logs (Textual TUI)")

class LogsApp(App):
    """Textual app that streams logs for a Render service."""

    CSS = "Screen {background: black; color: white;}"
    scroll_content = var("")

    def __init__(self, service_id: str, poll_interval: float = 2.0):
        super().__init__()
        self.service_id = service_id
        self.poll_interval = poll_interval
        self.scroll = ScrollView()

    def compose(self) -> ComposeResult:
        yield self.scroll

    async def on_mount(self) -> None:
        # Start background task
        self.set_interval(self.poll_interval, self.fetch_and_append)

    async def fetch_and_append(self) -> None:
        async with get_async_client() as client:
            try:
                r = await client.get(f"https://api.render.com/v1/services/{self.service_id}/logs")
                r.raise_for_status()
                data = r.json()
            except Exception as e:
                # Show error once and stop polling
                await self.scroll.update(f"[red]Error fetching logs: {e}[/red]\n")
                self.exit()
                return

            # data can be list or dict with 'logs'
            logs_list = data if isinstance(data, list) else data.get("logs", [])
            # append logs to the scroll view
            text = ""
            for entry in logs_list:
                ts = entry.get("timestamp") or entry.get("createdAt") or ""
                msg = entry.get("message") or entry.get("msg") or entry.get("text") or ""
                text += f"[cyan]{ts}[/cyan] {msg}\n"
            if text:
                await self.scroll.update(text)

@logs.command("stream")
def stream_logs(service_id: str):
    """Stream live logs for a service in a TUI."""
    app = LogsApp(service_id=service_id)
    app.run()
