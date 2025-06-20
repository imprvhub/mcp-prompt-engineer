# MCP Prompt Engineer

> [!NOTE]
> This project is currently under active development. While the uvx package is functional and ready for use with Claude Desktop, features and documentation are being continuously improved.

A Model Context Protocol (MCP) integration that provides Claude Desktop with access to AI prompts, tools, and configurations from AI major platforms. This tool enables developers and AI engineers to explore, compare, and analyze prompt engineering strategies across different AI services.

### Features

- **Multi-Platform Prompt Access**
  - Access prompts from Cursor, Windsurf, Replit, and other major AI platforms
  - Retrieve tool configurations and system prompts
  - Compare prompt strategies across different services
  - Search through thousands of professionally crafted prompts

- **Advanced Search Capabilities**
  - Full-text search across all prompt files and configurations
  - Filter by file type (.txt, .json, .md) and service
  - Targeted searches for specific functionality (agents, chat, tools)
  - Bulk comparison and analysis tools

- **Professional Analysis Tools**
  - Service-to-service comparison functionality
  - Statistical analysis of prompt patterns and configurations
  - Tool configuration inspection and validation
  - Cross-platform compatibility insights

- **MCP Integration**
  - Seamless integration with Claude Desktop
  - Real-time data access through authenticated backend
  - Performance optimized for rapid prompt exploration
  - Professional-grade API with session management

### Requirements

- Python 3.10 or higher
- Claude Desktop
- [uv](https://docs.astral.sh/uv/) package manager

#### Dependencies Installation

Install uv package manager using one of these methods:

**Official installer (recommended):**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Homebrew (macOS/Linux):**
```bash
brew install uv
```

**Install Homebrew (if needed):**
- Visit [https://brew.sh](https://brew.sh) for installation instructions on all operating systems
- Or run: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

The MCP server automatically manages Python dependencies through uvx.

### Installation

#### Zero-Clone Installation (Recommended)

The MCP Prompt Engineer supports direct installation without cloning repositories, using uvx for package management.

#### Configuration

The Claude Desktop configuration file is located at:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

Edit this file to add the MCP Prompt Engineer configuration:

```json
{
  "mcpServers": {
    "mcp-prompt-engineer": {
      "command": "uvx",
      "args": [
        "--python=3.10",
        "--from",
        "git+https://github.com/imprvhub/mcp-prompt-engineer",
        "mcp-prompt-engineer"
      ]
    }
  }
}
```

If you already have other MCPs configured, simply add the "mcp-prompt-engineer" section inside the "mcpServers" object:

```json
{
  "mcpServers": {
    "otherMcp": {
      "command": "...",
      "args": ["..."]
    },
    "mcp-prompt-engineer": {
      "command": "uvx",
      "args": [
        "--python=3.10",
        "--from",
        "git+https://github.com/imprvhub/mcp-prompt-engineer",
        "mcp-prompt-engineer"
      ]
    }
  }
}
```

#### Manual Installation

For development or local testing:

1. Clone the repository:
```bash
git clone https://github.com/imprvhub/mcp-prompt-engineer
cd mcp-prompt-engineer
```

2. Install dependencies:
```bash
uv sync
```

3. Run locally:
```bash
uv run src/mcp_prompt_engineer/main.py
```

### How It Works

The MCP Prompt Engineer connects to a secure backend service through authenticated API calls to access curated prompt databases from major AI platforms. The system uses session-based authentication to ensure reliable access while maintaining data integrity and security.

The tool aggregates prompts and configurations from various sources, providing a unified interface for prompt exploration and analysis. This approach enables comprehensive comparison and study of prompt engineering techniques across different platforms, helping users identify best practices and optimization strategies.

### Available Tools

#### Core Functionality

| Tool Name | Description | Usage |
|-----------|-------------|-------|
| `get_all_services` | List all available AI services | Get overview of supported platforms |
| `get_service_details` | Get detailed service information | Explore specific platform configurations |
| `search_content` | Search across all prompts and tools | Find specific patterns or techniques |
| `get_file_content` | Retrieve specific file content | Access individual prompts or configs |

#### Specialized Searches

| Tool Name | Description | Usage |
|-----------|-------------|-------|
| `get_all_prompts` | Get all prompt files (.txt) | Access complete prompt library |
| `get_all_tools` | Get all tool configurations (.json) | Review tool setups and parameters |
| `search_prompts_only` | Search specifically in prompt files | Target prompt-specific searches |
| `search_tools_only` | Search in tool configuration files | Find tool-related configurations |

#### Platform-Specific Access

| Tool Name | Description | Usage |
|-----------|-------------|-------|
| `get_cursor_prompts` | Access Cursor platform prompts | Explore Cursor-specific strategies |
| `get_windsurf_config` | Access Windsurf configurations | Review Windsurf prompt patterns |
| `get_replit_config` | Access Replit prompts and tools | Study Replit's approach |
| `get_open_source_prompts` | Access open source AI prompts | Explore community-driven prompts |

#### Analysis and Comparison

| Tool Name | Description | Usage |
|-----------|-------------|-------|
| `compare_services` | Compare two AI services | Analyze differences between platforms |
| `get_api_statistics` | Get comprehensive statistics | Review data distribution and metrics |
| `find_agent_prompts` | Find agent-related prompts | Focus on agent-specific techniques |
| `find_chat_prompts` | Find chat-related prompts | Explore conversational AI patterns |

### Supported Platforms

The MCP Prompt Engineer provides access to prompts and configurations from:

#### Commercial Platforms
- **Cursor**: Professional code editor with AI integration
- **Windsurf**: Advanced AI development environment
- **Replit**: Cloud-based development platform

#### Open Source Projects
- **Bolt**: Open source AI coding assistant
- **Cline**: AI pair programming tool
- **Codex CLI**: Command-line AI interface
- **Roo Code**: AI development utilities

### Example Usage

Here are examples of how to use the MCP Prompt Engineer with Claude:

#### Explore Available Services

```
Show me all available AI services and their statistics
```

#### Search for Specific Techniques

```
Search for prompts related to "code review" across all platforms
```

#### Compare Platform Approaches

```
Compare Cursor and Windsurf prompt strategies for code generation
```

#### Access Specific Configurations

```
Get the main system prompt from Cursor and analyze its structure
```

### Output Format

The tool provides structured results including:

- **Service Information**: Platform details, file counts, and supported formats
- **Prompt Content**: Complete prompt text with metadata and context
- **Tool Configurations**: JSON configurations with parameter explanations
- **Search Results**: Ranked results with relevance scores and context
- **Comparison Analysis**: Side-by-side platform comparisons with insights
- **Statistics**: Usage patterns, file distributions, and trend analysis

### Troubleshooting

#### "Server disconnected" error
If you see connection errors in Claude Desktop:

1. **Verify uvx installation**:
   - Run `uvx --version` to ensure uvx is properly installed
   - Reinstall uv if necessary: `curl -LsSf https://astral.sh/uv/install.sh | sh`

2. **Check Python version**:
   - Ensure Python 3.10+ is available: `python3 --version`

#### Authentication issues
If the MCP server reports authentication problems:

1. **Network connectivity**:
   - Verify internet connection is stable
   - Check if the backend service is accessible

2. **Session management**:
   - The tool automatically handles session renewal
   - Use `verify_authentication` tool to check connection status

#### Configuration issues
If the MCP server isn't starting:

1. **Verify configuration syntax**:
   - Ensure JSON syntax is valid in `claude_desktop_config.json`
   - Check that all brackets and quotes are properly matched

2. **Restart Claude Desktop**:
   - Close and restart Claude Desktop after configuration changes

### Development

#### Project Structure

- `main.py`: Main MCP server with tool definitions and API client
- `cli.py`: Command-line interface for testing and validation
- Authentication system with automatic session management
- Async API client with retry logic and error handling

#### Local Development

```bash
uv run src/mcp_prompt_engineer/main.py
```


### Security Considerations

The MCP Prompt Engineer uses authenticated API access to retrieve prompt data. Security features include:

- Session-based authentication with automatic token renewal
- Machine-specific identification for session tracking
- No storage of sensitive authentication data
- Read-only access to prompt repositories
- All communications over HTTPS with the backend service

### Future Development

As this project continues development, planned features include:

- Enhanced prompt analysis and comparison tools
- AI-powered prompt optimization suggestions
- Integration with additional AI platforms and services
- Advanced search capabilities with semantic matching
- Prompt versioning and historical analysis
- Community-driven prompt sharing and collaboration

The authentication system connects to a backend service that will help refine and improve prompts based on the highest standards from AI platforms, ensuring users have access to the most effective prompt engineering techniques.

### Contributing

Contributions are welcome! Areas for improvement include:

- Adding support for additional AI platforms
- Enhancing search and analysis capabilities
- Improving prompt categorization and tagging
- Developing prompt effectiveness metrics
- Creating visualization tools for prompt comparison

### License

This project is licensed under the Mozilla Public License 2.0 - see the [LICENSE](https://github.com/imprvhub/mcp-prompt-engineer/blob/main/LICENSE) file for details.

## Related Links

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Claude Desktop](https://claude.ai/download)
- [uv Package Manager](https://docs.astral.sh/uv/)
- [MCP Series](https://github.com/mcp-series)

