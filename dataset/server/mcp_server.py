from typing import Any
import httpx
import requests
from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from mcp.shared.exceptions import McpError
from mcp.types import ErrorData, INTERNAL_ERROR, INVALID_PARAMS
import uvicorn

from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.requests import Request

from bs4 import BeautifulSoup
from html2text import html2text

# Initialize FastMCP server
mcp = FastMCP("weather")

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
        Event: {props.get('event', 'Unknown')}
        Area: {props.get('areaDesc', 'Unknown')}
        Severity: {props.get('severity', 'Unknown')}
        Description: {props.get('description', 'No description available')}
        Instructions: {props.get('instruction', 'No specific instructions provided')}
    """

@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)

@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # First get the forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data for this location."

    # Get the forecast URL from the points response
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # Only show next 5 periods
        forecast = f"""
            {period['name']}:
            Temperature: {period['temperature']}°{period['temperatureUnit']}
            Wind: {period['windSpeed']} {period['windDirection']}
            Forecast: {period['detailedForecast']}
        """
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)

@mcp.tool()
async def get_random_joke() -> str:
    """Get a random joke."""
    url = "https://official-joke-api.appspot.com/random_joke"
    data = await make_nws_request(url)

    if not data:
        return "Unable to fetch a joke at this time."

    return f"{data['setup']} - {data['punchline']}"

@mcp.tool()
def extract_wikipedia_article(url: str) -> str:
    """
    Retrieves and processes a Wikipedia article from the given URL, extracting
    the main content and converting it to Markdown format.

    Usage:
        extract_wikipedia_article("https://en.wikipedia.org/wiki/Gemini_(chatbot)")
    """
    try:
        if not url.startswith("http"):
            raise ValueError("URL must begin with http or https protocol.")

        response = requests.get(url, timeout=8)
        if response.status_code != 200:
            raise McpError(
                ErrorData(
                    code=INTERNAL_ERROR,
                    message=f"Unable to access the article. Server returned status: {response.status_code}"
                )
            )
        soup = BeautifulSoup(response.text, "html.parser")
        content_div = soup.find("div", {"id": "mw-content-text"})
        if not content_div:
            raise McpError(
                ErrorData(
                    code=INVALID_PARAMS,
                    message="The main article content section was not found at the specified Wikipedia URL."
                )
            )
        markdown_text = html2text(str(content_div))
        return markdown_text

    except Exception as e:
        raise McpError(ErrorData(code=INTERNAL_ERROR, message=f"An unexpected error occurred: {str(e)}")) from e


sse = SseServerTransport("/message/")

async def handle_sse(request: Request) -> None:
    _server = mcp._mcp_server
    async with sse.connect_sse(
        request.scope,
        request.receive,
        request._send
    ) as (reader, writer): await _server.run(
        reader,
        writer,
        _server.handle_request(request)
    )

app = Starlette(
    debug=True,
    routes=[
        Route("/sse", endpoint=handle_sse),
        Mount("/message", app=sse.handle_post_message)
    ]
)

if __name__ == "__main__":
    print("MCP Server running...")
    # Initialize and run the server
    # mcp.run(transport='stdio')
    uvicorn.run(app, host="localhost", port=8002)