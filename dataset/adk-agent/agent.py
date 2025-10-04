from google.adk.models.lite_llm import LiteLlm
from google.adk.agents.llm_agent import Agent
from google.adk.tools.mcp_tool.mcp_toolset import (
    MCPToolset
)
from google.adk.tools.mcp_tool.mcp_session_manager import SseServerParams
import asyncio
from dotenv import load_dotenv

load_dotenv()

async def get_tools_async():
    """Gets tools from the File System MCP Server."""
    tools, exit_stack = await MCPToolset.from_server(
        connection_params=SseServerParams(
            url="http://localhost:8002/sse",
        )
    )
    print("MCP Toolset created successfully.")
    return tools, exit_stack

async def get_open_model_agent_async():
    local_llama_model = LiteLlm(model="ollama_chat/llama3.2")
    """Creates an ADK Agent equipped with tools from the MCP Server."""
    tools, exit_stack = await get_tools_async()
    print(f"Fetched {len(tools)} tools from MCP server.")
    root_agent = Agent(
        model=local_llama_model,
        name="assistant",
        instruction="""Help user extract and summarize the article from wikipedia link.
        Use the following tools to extract wikipedia article:
        - extract_wikipedia_article

        Once you retrieve the article, always summarize it in a few sentences for the user.
        """,
        tools=tools,
    )
    return root_agent, exit_stack

# root_agent = get_open_model_agent_async()

server = MCPToolset(
    connection_params=SseServerParams(
        url="http://localhost:8002/sse",
    )
)


local_llama_model = LiteLlm(model="ollama_chat/llama3.2")
"""Creates an ADK Agent equipped with tools from the MCP Server."""
# tools, exit_stack = await get_tools_async()
# print(f"Fetched {len(tools)} tools from MCP server.")
root_agent = Agent(
    model=local_llama_model,
    name="assistant",
    instruction="""Help user extract and summarize the article from wikipedia link.
    Use the following tools to extract wikipedia article:
    - extract_wikipedia_article

    Once you retrieve the article, always summarize it in a few sentences for the user.
    """,
    tools=[server],
)

