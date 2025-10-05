from google.adk.tools.mcp_tool.mcp_toolset import (
    MCPToolset,
    StdioConnectionParams,
    StdioServerParameters,
)
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents.llm_agent import Agent
from dotenv import load_dotenv
import os

load_dotenv()

def setup_mcp_server():
    print("home: "+os.getenv("MCP_HOME"))
    server = MCPToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command='uv',
                args=[
                    "run",
                    "--with",
                    "mcp",
                    "mcp",
                    "run",
                    "server/mcp_server.py"
                ],
                env={
                    "HOME": os.getenv("MCP_HOME"),
                    "LOGNAME": os.getenv("MCP_LOGNAME"),
                    "PATH": os.getenv("MCP_PATH"),
                    "SHELL": os.getenv("MCP_SHELL"),
                    "TERM": os.getenv("MCP_TERM"),
                    "USER": os.getenv("MCP_USER")
                }
            )
        )
    )
    return server


local_llama_model = LiteLlm(model="ollama_chat/llama3.2")
"""Creates an ADK Agent equipped with tools from the MCP Server."""

root_agent = Agent(
    model=local_llama_model,
    name="assistant",
    instruction="""Help user extract and summarize the article from wikipedia link.
    Use the following tools to extract wikipedia article:
    - extract_wikipedia_article

    Once you retrieve the article, always summarize it in a few sentences for the user.
    """,
    tools=[setup_mcp_server()],
)