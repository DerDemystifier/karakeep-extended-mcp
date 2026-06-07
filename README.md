# Karakeep MCP Server

A Model Context Protocol (MCP) server that provides an interface to the Karakeep API, allowing LLMs (like Claude) to manage bookmarks, lists, and tags.

This server is built using `FastMCP` and dynamically generates tools based on the Karakeep OpenAPI specification.

## Features

- **Bookmarks Management**: Create, retrieve, update, and delete bookmarks.
- **Lists Management**: Organize bookmarks into lists.
- **Tags Management**: Categorize bookmarks using tags.
- **OpenAPI Driven**: Automatically maps API endpoints to MCP tools.

## Prerequisites

- Python 3.10 or higher
- A Karakeep account and API token

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/DerDemystifier/karakeep-extended-mcp.git
    cd karakeep-extended-mcp
    ```

2. **Install dependencies**:
   It is recommended to use a virtual environment:

    ```bash
    pip install fastmcp httpx
    ```

## Configuration

The server requires the following environment variables to function:

| Variable               | Description                                                                                         | Example                                     |
| ---------------------- | --------------------------------------------------------------------------------------------------- | ------------------------------------------- |
| `KARAKEEP_URL`         | The base URL of your Karakeep instance                                                              | `https://karakeep.example.com`              |
| `KARAKEEP_TOKEN`       | Your personal API access token                                                                      | `your_secret_token_here`                    |
| `KARAKEEP_OPENAPI_URL` | (Optional) URL to the OpenAPI spec. If not provided, it uses the local `karakeep-openapi-spec-v0.32.0.json` | `https://karakeep.example.com/openapi.json` |

## Claude Desktop Configuration

To use this MCP server with Claude Desktop, add the following configuration to your `claude_desktop_config.json` file.

### File Location:

- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

### Configuration:

Replace the placeholders with your actual paths and credentials.

```json
{
    "mcpServers": {
        "karakeep": {
            "command": "python",
            "args": [".../karakeep-extended-mcp/karakeep-extended-mcp.py"],
            "env": {
                "KARAKEEP_URL": "https://your-karakeep-instance.com",
                "KARAKEEP_TOKEN": "your_api_token_here"
            }
        }
    }
}
```

_Note: Ensure you use absolute paths for the script location._

## Development

To run the server locally for testing:

```bash
export KARAKEEP_URL="https://your-karakeep-instance.com"
export KARAKEEP_TOKEN="your_api_token_here"
python karakeep-extended-mcp.py
```

## License

[Specify your license, e.g., MIT]
