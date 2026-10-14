"""Interactive example of the Claude Agent SDK's can_use_tool callback."""

import asyncio
from pathlib import Path
from typing import Any

from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, ClaudeSDKClient
from claude_agent_sdk.types import (
    PermissionResultAllow,
    PermissionResultDeny,
    TextBlock,
    ToolPermissionContext,
)
from dotenv import load_dotenv

if __package__:
    from .helper import MODEL_NAME
else:
    from helper import MODEL_NAME


async def approve_tool(
    tool_name: str,
    input_data: dict[str, Any],
    context: ToolPermissionContext,
) -> PermissionResultAllow | PermissionResultDeny:
    """Show each requested tool and let the user allow or deny it."""
    print(f"\nClaude wants to use: {tool_name}")
    print(f"Tool input: {input_data}")
    answer = input("Allow this tool call? (y/N): ").strip().casefold()

    if answer == "y":
        return PermissionResultAllow(behavior="allow")
    return PermissionResultDeny(
        behavior="deny",
        message="The user did not approve this tool call.",
    )


async def main() -> None:
    options = ClaudeAgentOptions(
        system_prompt="You are a helpful assistant. Use tools only when useful.",
        setting_sources=[],
        model=MODEL_NAME,
        max_turns=30,
        tools=["Read", "Glob", "PowerShell"],
        cwd=Path.cwd(),
        permission_mode="default",
        can_use_tool=approve_tool,
    )

    async with ClaudeSDKClient(options=options) as client:
        await client.query(input("What should Claude do in this folder? "))
        async for message in client.receive_messages():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(block.text)


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())