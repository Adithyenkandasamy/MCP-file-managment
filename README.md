# MCP File Manager

A local file management MCP server built with Python and the official `mcp` library (FastMCP).

## Features

- **List Files**: List contents of directories.
- **Read Files**: Read content of text files.
- **File Info**: Get metadata (size, modification time) of files.
- **Search**: Recursively search for files by name.

## Dependencies

- Python 3.10+
- `uv` (recommended) or `pip`

## Quick Start

1.  **Install dependencies**:
    ```bash
    uv sync
    ```

2.  **Run the server**:
    ```bash
    uv run main.py
    ```

## Claude Desktop Configuration

Add the following to your Claude Desktop config file:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

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
      ]
    }
  }
}
```

**Note**: Replace `/ABSOLUTE/PATH/TO/MCP-file-managment` with the actual absolute path to the directory where you cloned this repository.

## Available Tools

- `list_files(directory)`: List files and directories in the specified path (defaults to current directory).
- `read_file(file_path)`: Read the content of a text file.
- `file_info(file_path)`: Get file size, type, and modification time.
- `search_files(keyword)`: Recursively search for filenames containing a keyword in the current working directory.