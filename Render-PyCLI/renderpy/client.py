import httpx
from .utils import require_api_key, RENDER_API_BASE

def api_request(method: str, endpoint: str, **kwargs):
    """
    Synchronous helper for Typer commands.
    endpoint should NOT start with a slash, e.g. "services" or "services/{id}".
    """
    key = require_api_key()
    headers = {"Authorization": f"Bearer {key}"}
    url = f"{RENDER_API_BASE}/{endpoint}"
    try:
        with httpx.Client(timeout=30.0, headers=headers) as client:
            r = client.request(method, url, **kwargs)
            r.raise_for_status()
            # Some endpoints return empty body on success
            if r.content:
                return r.json()
            return {}
    except httpx.HTTPStatusError as e:
        msg = e.response.text if e.response is not None else str(e)
        raise RuntimeError(f"API error: {msg}") from e
    except httpx.RequestError as e:
        raise RuntimeError(f"Request error: {e}") from e

# Async client used by textual logs
def get_async_client():
    key = require_api_key()
    return httpx.AsyncClient(timeout=30.0, headers={"Authorization": f"Bearer {key}"})