# MCP File Server

A local file management MCP server built with Python and the official `mcp` library.

## Dependencies

- Python 3.10+
- `uv` (recommended) or `pip`

## Quick Start

1.  **Install dependencies**:
    ```bash
    uv sync
    ```

2.  **Create workspace directory**:
    The server restricts file operations to a `./workspace` directory in the project root.
    ```bash
    mkdir -p workspace
    ```

3.  **Run the server**:
    ```bash
    uv run main.py
    ```

## Claude Desktop Configuration

Add the following to your Claude Desktop config file (usually `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS or `%APPDATA%\Claude\claude_desktop_config.json` on Windows):

```json
{
  "mcpServers": {
    "file-manager": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/MCP-file-managment",
        "run",
        "main.py"
      ],
       "env": {}
    }
  }
}
```
**Note**: Replace `/ABSOLUTE/PATH/TO/MCP-file-managment` with the actual absolute path to this directory.

## Available Tools

- `list_files(directory)`: List files and directories in the workspace.
- `read_file(file_path)`: Read the content of a text file.
- `file_info(file_path)`: Get file size, type, and modification time.
- `search_files(keyword)`: Search for filenames containing a keyword.