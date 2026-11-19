"""
Call the MCP server by hand, the way an editor or agent.py does: it starts server.py,
calls one tool and prints what the model would receive.

    uv run python try_server.py tools
    uv run python try_server.py search "cuántos días de vacaciones tengo"
    uv run python try_server.py add path/to/file.pdf
"""

import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER = "server.py"


async def run(command: str, argument: str | None) -> None:
    params = StdioServerParameters(command=sys.executable, args=[SERVER])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            if command == "tools":
                for tool in (await session.list_tools()).tools:
                    print(f"=== {tool.name}  (required: {tool.input_schema.get('required')})\n{tool.description}\n")
                return
            name, key = {"search": ("search", "query"), "add": ("add_document", "path")}[command]
            result = await session.call_tool(name, {key: argument})
            print("\n".join(getattr(c, "text", "") for c in result.content))


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("tools", "search", "add") or (
            sys.argv[1] != "tools" and len(sys.argv) < 3):
        sys.exit(__doc__)
    asyncio.run(run(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None))
