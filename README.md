# Connect MCP Server with ADK
Google ADK (Agent Development Kit) is is a flexible and modular framework for developing and deploying AI agents. While optimized for Gemini and the Google ecosystem, ADK is model-agnostic, deployment-agnostic, and is built for compatibility with other frameworks. ADK was designed to make agent development feel more like software development, to make it easier for developers to create, deploy, and orchestrate agentic architectures that range from simple tasks to complex workflows.

MCP (Model Context Protocol) is an open-source standard for connecting AI applications to external systems. MCP consist of MCP Client and MCP Server. MCP client acts as orchestrator to choose relevant query to your action.

## Tools need
### Starlette async web service [detail](https://www.starlette.dev/)
    Starlette used to publish MCP server 
### MCP Server
### Ollama
### ADK
### BeautifulSoup
### Html2Text


## [DRAFT] LlamaIndex
### Embedding 
```
# Install LlamaIndex
uv add llama-index-embeddings-ollama
```

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
