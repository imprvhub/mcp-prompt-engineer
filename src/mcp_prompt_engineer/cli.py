#!/usr/bin/env python3

import sys
import json
import asyncio
from mcp_prompt_engineer.main import api_client

async def test_connection():
    try:
        result = await api_client.get("/health")
        return result
    except Exception as e:
        return {"error": str(e)}
    finally:
        await api_client.close()

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        print("Testing MCP Prompt Engineer connection...")
        result = asyncio.run(test_connection())
        print(json.dumps(result, indent=2))
    else:
        print("MCP Prompt Engineer CLI")
        print("Usage: mcp-prompt-engineer-cli test")
        print("This tool is designed to work as an MCP server, not as a standalone CLI.")
        print("Add it to your Claude Desktop configuration to use it.")

if __name__ == "__main__":
    main()
