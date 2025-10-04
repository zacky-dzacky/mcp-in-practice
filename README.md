# Connect MCP Server with ADK

## Tools need
### Starlette async web service (detail)[https://www.starlette.dev/]
    Starlette used to publish MCP server 
### MCP Server
### Ollama
### ADK
### BeautifulSoup
### Html2Text

## Installation
```
uv add "mcp[cli]"
uv add google-adk
```

## Run
```
# How to run our server
uv run mcp dev mcp_server.py

# How to run our client
uv run adk web
```
