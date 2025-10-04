from google.adk.models.lite_llm import LiteLlm
from google.adk.agents.llm_agent import Agent
from google.adk.tools.mcp_tool.mcp_toolset import (
    MCPToolset,
    StdioConnectionParams,
    StdioServerParameters,
)
from google.adk.tools.mcp_tool.mcp_session_manager import SseServerParams
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
                "HOME": "/Users/zackysyarief",
                "LOGNAME": "zackysyarief",
                "PATH": "/Users/zackysyarief/.npm/_npx/5a9d879542beca3a/node_modules/.bin:/Users/zackysyarief/Zac.Document/mcp/dataset/node_modules/.bin:/Users/zackysyarief/Zac.Document/mcp/node_modules/.bin:/Users/zackysyarief/Zac.Document/node_modules/.bin:/Users/zackysyarief/node_modules/.bin:/Users/node_modules/.bin:/node_modules/.bin:/usr/local/lib/node_modules/npm/node_modules/@npmcli/run-script/lib/node-gyp-bin:/Users/zackysyarief/Zac.Document/mcp/dataset/.venv/bin:/opt/homebrew/opt/ruby/bin:/opt/homebrew/bin:/usr/local/bin:/System/Cryptexes/App/usr/bin:/usr/bin:/bin:/usr/sbin:/sbin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/local/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/appleinternal/bin:/Library/Apple/usr/bin:/opt/homebrew/opt/ruby/bin:/opt/homebrew/bin:/Users/zackysyarief/.cargo/bin:/Users/zackysyarief/Library/Android/sdk/emulator:/Users/zackysyarief/Library/Android/sdk/tools:/Users/zackysyarief/Library/Android/sdk/platform-tools:/Users/zackysyarief/development/flutter/bin:/Users/zackysyarief/.lmstudio/bin:/Users/zackysyarief/.vscode/extensions/ms-python.debugpy-2025.10.0-darwin-arm64/bundled/scripts/noConfigScripts:/Users/zackysyarief/Library/Application Support/Code/User/globalStorage/github.copilot-chat/debugCommand:/Users/zackysyarief/Library/Android/sdk/emulator:/Users/zackysyarief/Library/Android/sdk/tools:/Users/zackysyarief/Library/Android/sdk/platform-tools:/Users/zackysyarief/development/flutter/bin:/Users/zackysyarief/.lmstudio/bin",
                "SHELL": "/bin/zsh",
                "TERM": "xterm-256color",
                "USER": "zackysyarief"
            }
        )
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

